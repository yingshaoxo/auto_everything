#from machine import Pin, Timer
#
#led = Pin("LED", Pin.OUT)
#global_timer = Timer()
#def tick(timer):
#    global led
#    led.toggle()
#
#global_timer.init(period=1000, mode=Timer.PERIODIC, callback=tick)
##in ms

try:
    import pico_main
except Exception as e:
    import esp32_main
