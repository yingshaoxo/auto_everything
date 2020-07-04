from auto_everything.gui import GUI
gui = GUI()

while 1:
    the_name = input("\n\nWhat the picture name? ").strip()
    gui.delay(5000)
    gui.screen_capture(the_name)
