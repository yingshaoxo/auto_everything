from time import sleep

from auto_everything.base import Terminal
t = Terminal()

from auto_everything.gui import GUI
gui = GUI()
pyautogui = gui.autogui


print("You have to make sure you got chrome and terminator installed. (Press enter to continue)")


# 1. start chrome
t.kill("chrome")
t.run_program("google-chrome-stable")
sleep(2)
pyautogui.press("f11")
pyautogui.moveTo(0,0)
while 1:
    if gui.exists("chrome_new_tab"):
        gui.click_after_exists("chrome_new_tab")
        break
    if gui.exists("chrome_untitled"):
        gui.click_after_exists("chrome_untitled")
        break
pyautogui.typewrite("https://google.com")
pyautogui.press("enter")
if gui.exists("chrome_x"):
    gui.click_after_exists("chrome_x")


# 2. run terminator
t.run_program("terminator", cwd=t.fix_path("~"))
pyautogui.press("f11")


print("Done!")
