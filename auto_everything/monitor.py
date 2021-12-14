import os
import time

from auto_everything.base import Terminal

t = Terminal(debug=True)


class KeyboardAndMouseMonitor:
    def __init__(self):
        try:
            from pynput import mouse, keyboard
            self.mouse = mouse
            self.keyboard = keyboard
        except Exception as e:
            print("python3 -m pip install pynput")
            raise e
        #
        # self.keyboard_callback_function = None
        # self.mouse_callback_function = None

if __name__ == "__main__":
    pass
    # keyboardAndMouseMonitor = KeyboardAndMouseMonitor()
    #
    # mouse = keyboardAndMouseMonitor.mouse
    # keyboard = keyboardAndMouseMonitor.keyboard
    #
    # def on_move(x, y):
    #     print('Pointer moved to {0}'.format(
    #         (x, y)))
    #
    # def on_click(x, y, button, pressed):
    #     print(f"{button}:")
    #     print('{0} at {1}'.format(
    #         'Pressed' if pressed else 'Released',
    #         (x, y)))
    #     # if not pressed:
    #     #     # Stop listener
    #     #     return False
    #
    # def on_scroll(x, y, dx, dy):
    #     print('Scrolled {0} at {1}'.format(
    #         'down' if dy < 0 else 'up',
    #         (x, y)))
    #
    # # Collect events until released
    # with mouse.Listener(
    #         on_move=on_move,
    #         on_click=on_click,
    #         on_scroll=on_scroll) as listener:
    #     listener.join()
    #
    #
    # def on_press(key):
    #     try:
    #         print('alphanumeric key {0} pressed'.format(
    #             key.char))
    #     except AttributeError:
    #         print('special key {0} pressed'.format(
    #             key))
    #
    #
    # def on_release(key):
    #     print('{0} released'.format(
    #         key))
    #     if key == keyboard.Key.esc:
    #         # Stop listener
    #         return False
    #
    #
    # # Collect events until released
    # with keyboard.Listener(
    #         on_press=on_press,
    #         on_release=on_release) as listener:
    #     listener.join()
    #
    # # # ...or, in a non-blocking fashion:
    # # listener = mouse.Listener(
    # #     on_move=on_move,
    # #     on_click=on_click,
    # #     on_scroll=on_scroll)
    # # listener.start()
