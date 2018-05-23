from auto_everything.base import Python
py = Python()

i = 0

@py.loop
def count():
    global i
    i += 1
    print(i)

count()
