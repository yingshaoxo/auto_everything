from auto_everything.gui_operator import GUI
gui = GUI()

while 1:
    the_name = input("\n\nWhat the picture name? ").strip()
    gui.delay(5000)
    gui.capture_screen_manually(the_name)
