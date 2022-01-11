
from obswebsocket import obsws, requests
from fastapi import APIRouter
from time import sleep
import threading

from auto_everything import Terminal
t = Terminal()


router = APIRouter(
    responses={404: {"error": "Not found"}},
)


host = "localhost"
port = 4444
password = "highhighlife"

ws = obsws(host, port, password)
theScriptProcess = None


def alwaysConnectToOBS():
    while True:
        try:
            # print("connected")
            # ws.call(requests.GetSceneList())
            ws.connect()
        except Exception as e:
            print(e)
        sleep(5)


@ router.on_event("startup")
async def startup():
    th = threading.Thread(target=alwaysConnectToOBS)
    th.start()


@ router.on_event("shutdown")
async def shutdown():
    pass


@ router.get("/", tags=["obs"])
async def obsHomePage():
    return {"message": "Welcome to the OBS API"}


@ router.get("/start", tags=["obs"])
async def start():
    ws.call(requests.StartRecording())
    return {"message": "done"}


@ router.get("/stop", tags=["obs"])
async def stop():
    ws.call(requests.StopRecording())
    return {"message": "done"}


@ router.get("/pause", tags=["obs"])
async def pause():
    ws.call(requests.PauseRecording())
    return {"message": "done"}


@ router.get("/resume", tags=["obs"])
async def resume():
    ws.call(requests.ResumeRecording())
    return {"message": "done"}


@router.get("/start_script", tags="obs")
async def startScript():
    global theScriptProcess
    ws.call(requests.ResumeRecording())
    theScriptProcess = t.run_program(
        "python3 /Users/yingshaoxo/CS/auto_everything/example/monitor/autoPauseOrResumeTheOBSrecording.py")


@router.get("/stop_script", tags="obs")
async def stopScript():
    global theScriptProcess
    t.kill("autoPauseOrResumeTheOBSrecording.py")
    if theScriptProcess is not None:
        theScriptProcess.kill()
        ws.call(requests.PauseRecording())
