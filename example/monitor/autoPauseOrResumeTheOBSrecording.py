from auto_everything.monitor import Keyboard_And_Mouse_Monitor
from collections import deque
import time
from threading import Timer

import sys
import time

from obswebsocket import obsws, requests

host = "localhost"
port = 4444
password = "highhighlife"

ws = obsws(host, port, password)
ws.connect()

keyboardAndMouseMonitor = Keyboard_And_Mouse_Monitor()

mouse = keyboardAndMouseMonitor.mouse
keyboard = keyboardAndMouseMonitor.keyboard

d = deque([time.time()], maxlen=1)
isInMoving = False
# t = Timer(3.0, lambda : print("okok"), ())
# t.start()


def checkIfDequeTimeLargerThanCurrentTimeBy(seconds):
    return time.time() - d[0] > seconds


def get_current_time_in_seconds():
    return time.time()


def add_time_to_deque():
    d.append(get_current_time_in_seconds())


def on_move(x, y):
    add_time_to_deque()


def on_click(x, y, button, pressed):
    add_time_to_deque()


def on_scroll(x, y, dx, dy):
    add_time_to_deque()


mouse_listener = mouse.Listener(
    on_move=on_move, on_click=on_click, on_scroll=on_scroll)
mouse_listener.start()


def on_press(key):
    add_time_to_deque()


def on_release(key):
    add_time_to_deque()


keyboard_listener = keyboard.Listener(on_press=on_press, on_release=on_release)
keyboard_listener.start()


if __name__ == "__main__":
    ws.call(requests.StartRecording())

    while True:
        time.sleep(1)
        if checkIfDequeTimeLargerThanCurrentTimeBy(5):
            isInMoving = False
        else:
            isInMoving = True

        print(isInMoving)

        if isInMoving:
            ws.call(requests.ResumeRecording())
        else:
            ws.call(requests.PauseRecording())

    # ws.call(requests.StopRecording())
