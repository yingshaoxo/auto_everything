from enum import Enum
from typing import NewType, TypeVar
import os
from auto_everything.video import Video
from auto_everything.disk import Disk

from typing import Dict, List, Optional, Union

import asyncio
import sys
import uvicorn

from fastapi import BackgroundTasks, Header

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi import File, UploadFile
from fastapi.responses import FileResponse
from fastapi.responses import StreamingResponse


from py_backend.store.globalVariables import GlobalStore

from py_backend.tools.networkTool import is_port_in_use
from py_backend.tools.stringTool import myPrint
from py_backend.database.sqlite import MyDatabase
from service.py_backend.database.sqlite import (
    ErrorOutput,
    ProjectIDInput,
    ProjectInput,
    ProjectOutput,
    StartProcessInput,
    SuccessOutput,
)

from py_backend.tools.diskTool import getFilePathByProjectID
from py_backend.routers import test, obs
from py_backend.routers import video as videoRouter


disk = Disk()
video = Video()


globalStore = GlobalStore()
myDatabase = MyDatabase(globalStore.DATABASE_URL)


app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(
    test.router,
    prefix="/test",
    tags=["test"],
)
app.include_router(
    obs.router,
    prefix="/obs",
    tags=["obs"],
)

app.include_router(
    videoRouter.router,
    prefix="/video",
    tags=["video"],
)


def deleteCorrespondingFileOfAProject(projectID: int) -> None:
    filePath = getFilePathByProjectID(projectID)
    if disk.exists(filePath):
        disk.remove_a_file(filePath)

    outputPath = filePath + ".output.mp4"
    if disk.exists(outputPath):
        disk.remove_a_file(outputPath)


async def async_func(project_id: int, job: str):
    project = await myDatabase.getAProjectByID(project_id)
    if project is None:
        await myDatabase.setStatusOfAProject(project_id, -1)
        return

    inputPath = project.input
    outputPath = getFilePathByProjectID(project_id) + ".output.mp4"

    await myDatabase.setStatusOfAProject(project_id, 1)

    try:
        if job == "speedupSilence":
            video.speedup_silence_parts_in_video(inputPath, outputPath, 30, speed=30)
        elif job == "removeSilence":
            video.remove_silence_parts_from_video(inputPath, outputPath, 40, 1.7)
    except Exception as e:
        await myDatabase.setStatusOfAProject(project_id, -1)
        raise e

    await myDatabase.updateOutputOfAProject(project_id, outputPath)
    await myDatabase.setStatusOfAProject(project_id, 2)


def startToWorkOnAProject(project_id: int, job: str):
    # loop = asyncio.get_event_loop()
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(async_func(project_id, job))


@app.on_event("startup")
async def startup():
    await myDatabase.database.connect()


@app.on_event("shutdown")
async def shutdown():
    await myDatabase.database.disconnect()


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.post("/upload_file/", response_model=Dict[str, str])
async def upload_file(projectID: int, file: UploadFile = File(...)):
    print(globalStore.tempFolder)
    print(file)

    if myDatabase.checkIfProjectExistByID(projectID) is False:
        return {"error": "Project ID not exist"}

    filePath = getFilePathByProjectID(projectID)

    contents = await file.read()
    contents_bytes_io = disk.convert_bytes_to_bytesio(contents)  # type: ignore
    disk.save_bytesio_to_file(contents_bytes_io, filePath)

    query = (
        myDatabase.projects.update()
        .where(myDatabase.projects.c.id == projectID)
        .values(input=filePath)
    )
    await myDatabase.database.execute(query)

    return {"message": "success"}


CONTENT_CHUNK_SIZE = 100 * 1024


@app.get("/stream_file/")
async def stream_file(filePath: str, range: Optional[str] = Header(None)):
    def get_file():
        f = open(filePath, "rb")
        return f, os.path.getsize(filePath)

    def chunk_generator_from_stream(stream, chunk_size, start, size):
        bytes_read = 0
        stream.seek(start)
        while bytes_read < size:
            bytes_to_read = min(chunk_size, size - bytes_read)
            yield stream.read(bytes_to_read)
            bytes_read = bytes_read + bytes_to_read
        stream.close()

    asked = range or "bytes=0-"
    # print(asked)
    stream, total_size = get_file()
    start_byte = int(asked.split("=")[-1].split("-")[0])

    return StreamingResponse(
        chunk_generator_from_stream(
            stream, start=start_byte, chunk_size=CONTENT_CHUNK_SIZE, size=total_size
        ),
        headers={
            "Accept-Ranges": "bytes",
            "Content-Range": f"bytes {start_byte}-{start_byte+CONTENT_CHUNK_SIZE}/{total_size}",
            "Content-Type": "video/mp4",
        },
        status_code=206,
    )


@app.get("/download_file/")
async def download_file(filePath: str):
    project = await myDatabase.getProjectByInputOrOutputFilePath(filePath)
    print(filePath)
    return FileResponse(
        path=filePath,
        media_type="application/octet-stream",
        filename=project.title + ".mp4",
    )


@app.get("/projects/", response_model=List[ProjectOutput])
async def read_projects():
    query = myDatabase.projects.select()
    return await myDatabase.database.fetch_all(query)


# class ProjectOutputOrErrorOutput(Enum):
#     project: ProjectOutput
#     err: ErrorOutput

# @ app.post("/get_project/", response_model=ProjectOutputOrErrorOutput)
# async def read_project(projectIDInput: ProjectIDInput):
#     record = await myDatabase.getAProjectByID(projectIDInput.project_id)

#     if record is None:
#         return ErrorOutput.parse_obj({"error": "Not found"})
#     else:
#         return record


@app.post(
    "/get_project/", response_model=Union[ProjectOutput, ErrorOutput]
)  # type: ignore
async def read_project(projectIDInput: ProjectIDInput):
    record = await myDatabase.getAProjectByID(projectIDInput.project_id)

    if record is None:
        return ErrorOutput.parse_obj({"error": "Not found"})
    else:
        return record


@app.post("/create_project/", response_model=ProjectOutput)
async def create_project(project: ProjectInput):
    query = myDatabase.projects.insert().values(**project.dict())
    last_record_id = await myDatabase.database.execute(query)
    return {**project.dict(), "id": last_record_id, "output": ""}


@app.post("/delete_project/", response_model=Dict[str, str])
async def delete_project(projectIDInput: ProjectIDInput):
    if myDatabase.checkIfProjectExistByID(projectIDInput.project_id) is False:
        return {"error": "Project ID not exist"}

    query = myDatabase.projects.delete().where(
        myDatabase.projects.c.id == projectIDInput.project_id
    )
    await myDatabase.database.execute(query)

    deleteCorrespondingFileOfAProject(projectIDInput.project_id)

    return {"success": "Deleted"}


@app.post(
    "/start_process_for_a_project/", response_model=Union[SuccessOutput, ErrorOutput]
)  # type: ignore
async def start_process_for_a_project(
    StartProcessInput: StartProcessInput, background_tasks: BackgroundTasks
):
    if myDatabase.checkIfProjectExistByID(StartProcessInput.project_id) is False:
        return {"error": "Project ID not exist"}

    background_tasks.add_task(
        startToWorkOnAProject,
        project_id=StartProcessInput.project_id,
        job=StartProcessInput.job,
    )

    return {"success": "Process started"}


def start():
    port = 8765

    myPrint(f"The service is running on: http://localhost:{port}")

    uvicorn.run(
        "main:app", host="0.0.0.0", port=port, debug=True, reload=True, workers=1
    )
