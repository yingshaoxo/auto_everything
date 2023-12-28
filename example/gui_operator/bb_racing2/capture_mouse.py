from auto_everything.gui_operator import GUI, Controller
gui = GUI()
controller = Controller()

while 1:
    the_name = input("\n\nDo a capture? ").strip()
    gui.delay(5000)
    print(gui.pyautogui.position())
