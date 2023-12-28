from auto_everything.gui_operator import GUI, Controller
gui = GUI(time_takes_for_one_click=0.5, grayscale=True)
controller = Controller()

sleep_time = 200
while 1:
    if gui.exists("scrcpy", confidence=0.8):
        x, y = gui.get_center_point_of("money", confidence=0.7)
        if x != None:
            while True:
                x, y = gui.get_center_point_of("money")
                if x != None:
                    for i in range(200):
                        controller.mouse_click(x=x, y=y, button='left', interval=0.1, game=True)
                if gui.exists("retry", confidence=0.7):
                    gui.click("retry")
    """
    if gui.exists("scrcpy"):
        if gui.exists("box"):
            gui.click("box")
            gui.delay(sleep_time)
            gui.click("2200")
            gui.delay(sleep_time)
            for i in range(9):
                controller.mouse_click(x=443, y=947, button='left', interval=0.1, game=True)
            gui.delay(sleep_time)
            continue
        elif gui.exists("2200"):
            gui.click("2200")
            gui.delay(sleep_time)
            for i in range(9):
                controller.mouse_click(x=1545, y=379, button='left', interval=0.1, game=True)
            gui.delay(sleep_time)
            continue
        elif gui.exists("retry", confidence=0.7):
            gui.click("retry")
        elif gui.exists("ok"):
            gui.click("ok")
        else:
            controller.mouse_click(x=1545, y=379, button='left', interval=0.1, game=True)
            gui.delay(sleep_time)

    """
    """
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
