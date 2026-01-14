#from machine import Pin, Timer
#
#led = Pin("LED", Pin.OUT)
#global_timer = Timer()
#def tick(timer):
#    global led
#    led.toggle()
#
#global_timer.init(period=1000, mode=Timer.PERIODIC, callback=tick)

#led = Pin("LED", Pin.OUT)
#led.on()
#sleep(1)
#led.off()

try:
    #import pico_main
    import system_launcher
except Exception as e:
    import esp32_main
