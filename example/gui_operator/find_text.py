from auto_everything.gui_operator import GUI

gui = GUI()
points = gui.find_text("yingshaoxo")

if points:
    x, y = points[0]
    gui.autogui.moveTo(x,y)
    print(points)
else:
    print("Can't find anything | 没找到")
