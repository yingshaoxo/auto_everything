from auto_everything.gui import GUI
gui = GUI(time_takes_for_one_click=0.5)

while 1:
    #gui.hide_mouse()

    if gui.exists("marble-icon"):
        gui.click("marble-icon")
        while not gui.exists("旅游大亨"):
            gui.delay(1)
        gui.click("旅游大亨")

    gui.click("通过")
    gui.click("开始旅程")
    gui.click("经济舱")
    gui.click('网络不稳定')
    gui.click('取消聊天')

    if gui.exists("冠军联赛"):
        x,y = gui.get_center_xy("冠军联赛")
        gui.autogui.dragTo(x - 300, y+3)
        gui.autogui.moveTo(x - 210, y+55)
        gui.autogui.moveTo(x - 140, y-51)
        gui.autogui.moveTo(x - 130, y+52)
        gui.autogui.moveTo(x - 120, y+52)
        gui.autogui.dragRel(x, y)
        gui.autogui.mouseUp()

    gui.click('立即开始')
    gui.click('个人赛')
    gui.click('2P')
    gui.click('确定')

    gui.click('准备开始')
    gui.click('开始游戏')
    gui.click('推荐游戏挑战')

    gui.click('取消')
    gui.click('红色宝箱')

    if gui.exists('单打'):
        gui.click('x')

    while gui.exists("笑脸"):
        gui.delay(1)
