from auto_everything.audio import AudioAnalyzer
from fastapi import APIRouter
from typing import Any, Dict, List, Union
import numpy as np

from py_backend.store.globalVariables import GlobalStore
from py_backend.database.sqlite import MyDatabase

from py_backend.tools.diskTool import getFilePathByProjectID

from auto_everything.video import Video
video = Video()

audioAnalyzer = AudioAnalyzer()


globalStore = GlobalStore()
myDatabase = MyDatabase(globalStore.DATABASE_URL)

router = APIRouter(
    responses={404: {"error": "Not found"}},
)


@ router.on_event("startup")
async def startup():
    await myDatabase.database.connect()


@ router.on_event("shutdown")
async def shutdown():
    await myDatabase.database.disconnect()


@router.get("/", tags=["video"])
async def obsHomePage():
    return {"message": "Welcome to the Video API"}

# @ app.post("/upload_file/", response_model=Dict[str, str])
# async def upload_file(projectID: int, file: UploadFile = File(...)):


@router.post("/getAudioVolumeData", tags=["video"], response_model=Dict)
async def getAudioVolumeData(projectID: int):
    filePath = getFilePathByProjectID(projectID)
    audioData = audioAnalyzer.get_audio_loudness_per_x_millisecond(filePath, 500)
    audioData /= np.max(np.abs(audioData), axis=0)
    audioData = 1 - (-audioData)
    return {"data": audioData.tolist()}


@router.post("/getSilenceData", tags=["video"], response_model=Dict)
async def getSilenceData(projectID: int, targetDB: int):
    filePath = getFilePathByProjectID(projectID)
    data = video._get_voice_and_silence_parts(filePath, top_db=targetDB)
    # print(data)
    return {"data": data}
