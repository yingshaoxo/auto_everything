from auto_everything.gui import GUI, Controller
gui = GUI(time_takes_for_one_click=0.5, grayscale=True)
controller = Controller()

while 1:
    if gui.exists("time-jump"):
        gui.hide_mouse()

        if gui.exists("retry"):
            gui.click("retry")

        if gui.exists("no-button"):
            gui.click("time-jump")
        else:
            if gui.exists("green-button"):
                gui.click("green-button")
            else:
                while 1:
                    controller.mouse_click(x=443, y=947, button='left', game=True)
                    controller.mouse_click(x=443, y=947, button='left', game=True)
                    controller.mouse_click(x=443, y=947, button='left', game=True)
                    controller.mouse_click(x=443, y=947, button='left', game=True)
                    controller.mouse_click(x=443, y=947, button='left', game=True)
                    controller.mouse_click(x=443, y=947, button='left', game=True)

                    gui.hide_mouse()
                    if gui.exists("no-button"):
                        break
                    if not gui.exists("time-jump"):
                        break
                    if gui.exists("retry"):
                        break

    gui.delay(10)  # milliseconds
