import databases
from auto_everything.video import Video
from typing import Dict, List, Union

import asyncio

from fastapi.param_functions import Query
from fastapi import BackgroundTasks

from py_backend.store.globalVariables import GlobalStore
import sys
import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi import File, UploadFile

from py_backend.tools.networkTool import is_port_in_use
from py_backend.tools.stringTool import myPrint
from py_backend.database.sqlite import MyDatabase
from service.py_backend.database.sqlite import ErrorOutput, ProjectIDInput, ProjectInput, ProjectOutput, StartProcessInput, SuccessOutput

from auto_everything.disk import Disk
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


def getFilePathByProjectID(projectID: int) -> str:
    return globalStore.tempFolder + "/" + str(projectID) + ".mp4"


def deleteCorrespondingFileOfAProject(projectID: int) -> None:
    filePath = getFilePathByProjectID(projectID)
    if disk.exists(filePath):
        disk.removeAFile(filePath)

    outputPath = filePath + ".output.mp4"
    if disk.exists(outputPath):
        disk.removeAFile(outputPath)


async def async_func(project_id: int, job: str):
    if (job == "speedupSilence"):
        project = await myDatabase.getAProjectByID(project_id)

        inputPath = project.input
        outputPath = getFilePathByProjectID(project_id) + ".output.mp4"

        await myDatabase.setStatusOfAProject(project_id, 1)
        video.speedup_silence_parts_in_video(
            inputPath, outputPath, 21, speed=30)

        await myDatabase.updateOutputOfAProject(project_id, outputPath)

        await myDatabase.setStatusOfAProject(project_id, 2)


def startToWorkOnAProject(project_id: int, job: str):
    # loop = asyncio.get_event_loop()
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(async_func(project_id, job))


@ app.on_event("startup")
async def startup():
    await myDatabase.database.connect()


@ app.on_event("shutdown")
async def shutdown():
    await myDatabase.database.disconnect()


@ app.get("/")
async def root():
    return {"message": "Hello World"}


@ app.post("/upload_file/", response_model=Dict[str, str])
async def upload_file(projectID: int, file: UploadFile = File(...)):
    print(globalStore.tempFolder)
    print(file)

    if (myDatabase.checkIfProjectExistByID(projectID) == False):
        return {"error": "Project ID not exist"}

    filePath = getFilePathByProjectID(projectID)

    contents = await file.read()
    contents_bytes_io = disk.convertBytesToBytesIO(contents)
    disk.save_bytesio_to_file(contents_bytes_io, filePath)

    query = myDatabase.projects.update().where(
        myDatabase.projects.c.id == projectID).values(input=filePath)
    await myDatabase.database.execute(query)

    return {"message": "success"}


@ app.get("/projects/", response_model=List[ProjectOutput])
async def read_projects():
    query = myDatabase.projects.select()
    return await myDatabase.database.fetch_all(query)


@ app.post("/get_project/", response_model=Union[ProjectOutput,  ErrorOutput])
async def read_project(projectIDInput: ProjectIDInput):
    record = await myDatabase.getProjectByID(projectIDInput.projectID)

    if record is None:
        return {"error": "Not found"}
    else:
        return record


@ app.post("/create_project/", response_model=ProjectOutput)
async def create_project(project: ProjectInput):
    query = myDatabase.projects.insert().values(**project.dict())
    last_record_id = await myDatabase.database.execute(query)
    return {**project.dict(), "id": last_record_id, "output": ""}


@ app.post("/delete_project/", response_model=Dict[str, str])
async def delete_project(projectIDInput: ProjectIDInput):
    if (myDatabase.checkIfProjectExistByID(projectIDInput.project_id) == False):
        return {"error": "Project ID not exist"}

    query = myDatabase.projects.delete().where(
        myDatabase.projects.c.id == projectIDInput.project_id)
    await myDatabase.database.execute(query)

    deleteCorrespondingFileOfAProject(projectIDInput.project_id)

    return {"success": "Deleted"}


@ app.post("/start_process_for_a_project/", response_model=Union[SuccessOutput, ErrorOutput])
async def start_process_for_a_project(StartProcessInput: StartProcessInput, background_tasks: BackgroundTasks):
    if (myDatabase.checkIfProjectExistByID(StartProcessInput.project_id) == False):
        return {"error": "Project ID not exist"}

    background_tasks.add_task(
        startToWorkOnAProject, project_id=StartProcessInput.project_id, job=StartProcessInput.job)

    return {"success": "Process started"}


def start():
    # launch with: poetry run dev

    port = sys.argv[-1]
    if port.isdigit():
        port = int(port)
    else:
        port = 8000

    while is_port_in_use(port):
        port += 1

    myPrint(f"The service is running on: http://localhost:{port}")

    uvicorn.run("main:app", host="0.0.0.0",
                port=port, debug=True, reload=True)
