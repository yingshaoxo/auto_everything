from auto_everything.gui_operator import AndroidGUI

scrcpy_window_name, project_name = "pixel", "test"
gui = AndroidGUI(scrcpy_window_name, project_name)

while 1:
    the_name = input("\n\nWhat the picture name? ").strip()
    gui.delay(5000)
    gui.capture_screen_manually(the_name)
