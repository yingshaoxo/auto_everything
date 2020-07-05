from auto_everything.gui import GUI, Controller
gui = GUI(time_takes_for_one_click=0.5, grayscale=True)
controller = Controller()

sleep_time = 200
while 1:
    if gui.exists("time-jump"):
        gui.hide_mouse()

        if gui.exists("no-button"):
            gui.click("time-jump")
            gui.delay(sleep_time)
            gui.click("green-button")
            gui.delay(sleep_time)
            for i in range(5):
                controller.mouse_click(x=443, y=947, button='left', interval=0.1, game=True)
            gui.delay(sleep_time*1.5)
            continue
        else:
            gui.click("green-button")
            gui.delay(sleep_time)
            for i in range(5):
                controller.mouse_click(x=443, y=947, button='left', interval=0.1, game=True)
            gui.delay(sleep_time*1.5)

        if gui.exists("retry"):
            gui.click("retry")
    """
    if gui.exists("time-jump"):
        gui.hide_mouse()

        if gui.exists("no-button"):
            gui.click("time-jump")
        else:
            if gui.exists("green-button"):
                gui.click("green-button")
            else:
                for i in range(6):
                    controller.mouse_click(x=443, y=947, button='left', game=True)
                gui.delay(1000)

        if gui.exists("retry"):
            gui.click("retry")
    """
