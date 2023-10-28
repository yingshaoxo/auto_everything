from auto_everything.python import Python

py = Python()

class Tools():
    yingshaoxo = 2

    def _init__(self):
        print("initilized")

    def hi(self):
        print('hi, yingshaoxo.')

    def hi_you(self, you:str):
        print(f"Hi, {you}")

    def hi_yingshaoxo(self, you: str = "yingshaoxo"):
        print(f"Hi, yingshaoxo")

    def add(self, a: int, b :int = 100):
        print(a + b)

    def fuck(self, a1: str = "yingshaoxo", b2: str="yingshaoxo2"):
        print(a1 + b2)

py.fire2(Tools)
