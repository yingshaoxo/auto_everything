from machine import Pin, PWM
import time

servo = PWM(Pin(2))
servo.freq(50) #50hz

def set_angle(angle):
    # 0 to 180 degree
    # for loop servo: 0->forward, 90->stop, 180->back
    pulse = int(1000000 + (angle / 180) * 1000000)
    servo.duty_ns(pulse)

def servo_360_speed_change(speed):
    #speed: -100 to 100, set 0 to stop
    if speed == 0:
        set_angle(90)
    if speed < 0:
        new_speed = int((abs(speed) / 100) * 90)
        set_angle(90 + new_speed)
    if speed > 0:
        new_speed = int(90 - ((speed/100)*90))
        set_angle(new_speed)

def test():
    set_angle(90)
    time.sleep(3)

    set_angle(180)
    time.sleep(3)

    set_angle(0)
    time.sleep(3)

    for _ in range(3):
        speed = 0
        for i in range(5):
            speed += 20
            servo_360_speed_change(speed)
            time.sleep(1)
        servo_360_speed_change(speed)
        time.sleep(1)
        speed = 0
        for i in range(5):
            speed -= 20
            servo_360_speed_change(speed)
            time.sleep(1)


servo_360_speed_change(38)
