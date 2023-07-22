from cgi import test
from time import sleep
from auto_everything.time import Time
time_ = Time()

def test_1():
    def ok():
        print("no")
    print("yes")
    time_.run_a_function_after_x_seconds(ok, 5)

def test_2():
    def ok():
        print("no")
    print("yes")
    return time_.run_a_function_every_x_seconds(ok, 3, wait=False)


def test_3():
    def ok():
        print("no")
    print("yes")
    return time_.run_a_function_at_a_certain_time(ok, the_time="2023-07-7 00:49:50")

#test_1()

p = test_2()
sleep(10)
p.terminate()
print("terminated")
sleep(10)
print("Done")

# test_3()