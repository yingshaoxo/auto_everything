from obswebsocket import obsws, requests
from fastapi import APIRouter
from time import sleep
import threading
import os

from auto_everything import Terminal

t = Terminal()


router = APIRouter(
    responses={404: {"error": "Not found"}},
)


def myOBScall(theRequest):
    host = "localhost"
    port = 4444
    password = "highhighlife"
    ws = obsws(host, port, password)
    ws.connect()
    ws.call(theRequest)
    ws.disconnect()
    return ws


theScriptProcess = None


@router.get("/", tags=["obs"])
async def obsHomePage():
    return {"message": "Welcome to the OBS API"}


@router.get("/start", tags=["obs"])
async def start():
    myOBScall(requests.StartRecording())
    return {"message": "done"}


@router.get("/stop", tags=["obs"])
async def stop():
    myOBScall(requests.StopRecording())
    return {"message": "done"}


@router.get("/pause", tags=["obs"])
async def pause():
    myOBScall(requests.PauseRecording())
    return {"message": "done"}


@router.get("/resume", tags=["obs"])
async def resume():
    myOBScall(requests.ResumeRecording())
    return {"message": "done"}


@router.get("/start_script", tags=["obs"])
async def startScript():
    global theScriptProcess
    myOBScall(requests.ResumeRecording())
    path = os.path.join(
        os.path.dirname(os.path.realpath(__file__)),
        "autoPauseOrResumeTheOBSrecording.py",
    )
    if not t.is_running("autoPauseOrResumeTheOBSrecording.py"):
        theScriptProcess = t.run_program(f"python3 '{path}'")


@router.get("/stop_script", tags=["obs"])
async def stopScript():
    global theScriptProcess
    t.kill("autoPauseOrResumeTheOBSrecording.py")
    if theScriptProcess is not None:
        theScriptProcess.kill()
        myOBScall(requests.PauseRecording())
