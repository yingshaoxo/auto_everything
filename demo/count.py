from auto_everything.base import Python
py = Python()

i = 0

@py.loop(new_thread=False)
def count():
    global i
    i += 1
    print(i)

count()

print("Welcome to my world!")
