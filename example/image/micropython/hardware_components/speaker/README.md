# yingshaoxo speaker

## play music note
```
# made by doubao AI
from machine import Pin, PWM
from time import sleep

# 定义C调7个基础音阶对应的频率 (哆 唻 咪 发 嗦 啦 西)
tones = [262, 294, 330, 349, 392, 440, 494]
# 定义每个音的播放时长（秒）和音之间的间隔（秒）
note_duration = 0.5
note_interval = 0.1

# 创建PWM对象，引脚5
buzzer = PWM(Pin(5))
# 初始占空比设为0（静音）
buzzer.duty_u16(0)

try:
    while True:
        # 依次播放7个音阶
        for tone in tones:
            # 设置当前音阶的频率
            buzzer.freq(tone)
            # 设置占空比（音量，范围0-65535，32768是50%）
            buzzer.duty_u16(32768)
            # 播放当前音符
            sleep(note_duration)
            # 关闭声音（间隔）
            buzzer.duty_u16(0)
            sleep(note_interval)
        # 7个音播放完后停顿一下再循环
        sleep(1)
except KeyboardInterrupt:
    # 捕获中断，程序结束时关闭PWM
    buzzer.deinit()
    print("程序已停止")
```

## play local sound

> the chip time may not accurate, cause it sounds bad.

```
# made by gemini AI
from machine import Pin, PWM, Timer
import time

# ======================
# 1. 硬件配置
# ======================
# 喇叭两根线：一根接 GP5，一根接 GND
# 注意：如果声音小，可以加个 8050 三极管放大，或者接功放模块
audio_pin = Pin(5)
pwm = PWM(audio_pin)

# 载波频率：设为 125kHz
pwm.freq(125000)

# ======================
# 2. 播放逻辑
# ======================
class PWM_Audio:
    def __init__(self, pwm_obj):
        self.pwm = pwm_obj
    
    def play_bytes(self, data):
        for byte in data:
            # 0-255 映射到 0-65535
            # 使用左移 8 位比乘法快
            self.pwm.duty_u16(byte << 8)
            # 8000Hz = 每 125 微秒一个点. 考虑到代码执行耗时，大约延时 110-120us
            time.sleep_us(120)
    
    def play_end(self):
        self.pwm.duty_u16(0)

    def play_file(self, filename):
        """
        建议将歌曲转换成 raw 二进制格式（每个字节代表一个采样点值 0-255）
        """
        try:
            with open(filename, "rb") as f:
                print("开始播放...")
                while True:
                    chunk = f.read(512)
                    if not chunk:
                        break
                    
                    for byte in chunk:
                        # 0-255 映射到 0-65535
                        self.pwm.duty_u16(byte << 8)
                        
                        # 8000Hz = 每 125 微秒一个点
                        # 考虑到代码执行耗时，大约延时 110-120us
                        time.sleep_us(120) 
                
                self.pwm.duty_u16(0)
                print("播放结束")
        except Exception as e:
            print("错误:", e)

# ======================
# 3. 播放
# ======================
player = PWM_Audio(pwm)
player.play_file("song_mini_small.binary")
```

## play remote music

> made by yingshaoxo. best quality so far. the outside timer is accurate.
> pi pico thread has bugs, when you run loop in thread while using UART, bug will happen, it will break or not working properly. 
> currently, the wrong sound may come from broken transfer or python speed is slow. the same logic works fine for pure c quick speed.

computer:
"""
import time

from auto_everything.disk import Disk
disk = Disk()

from auto_everything.audio_ import Audio
audio = Audio()

if not disk.exists("/home/yingshaoxo/Downloads/song_small.binary"):
    audio = audio.read_from_file("/home/yingshaoxo/Downloads/song.wav")
    audio.save_to_simple_binary_audio("/home/yingshaoxo/Downloads/song_small.binary")

import serial
usb_serial = serial.Serial("/dev/ttyUSB0", baudrate=115200)

# it plays with stable speed, 8k/s.
start_time = time.time()
point_counting = 0
with open("/home/yingshaoxo/Downloads/song_small.binary", "rb") as f:
    while True:
        data = f.read(1)
        point_counting += 1
        if not data:
            break
        time_use = time.time() - start_time
        time_should_use = point_counting / 8000
        while time_use < time_should_use:
            time_use = time.time() - start_time
        usb_serial.write(data)

print("done")
"""

micro_controller:
```
from machine import Pin, PWM, UART

audio_pin = Pin(5)
pwm = PWM(audio_pin)
pwm.freq(125000)

uart1 = UART(1, baudrate=115200, tx=Pin(20), rx=Pin(21), timeout=0)

def stream_audio():
    print("waiting...")
    set_duty = pwm.duty_u16
    try:
        while True:
            if uart1.any():
                chunk = uart1.read(1)
                if chunk:
                    for byte in chunk:
                        # 0-255 map to 0-65535
                        set_duty(byte << 8)
    except KeyboardInterrupt:
        pwm.duty_u16(0)

stream_audio()
```

## safe volumn increase

```
三极管的声音放大连线方式:

电阻：1kΩ (不加电阻会让单片机重启)
三极管：1=Emitter(ground)，2=Collector(positive)，3=Base(signal)

Pico Pin5 -> 1kΩ 电阻 -> 三极管B基极
三极管E发射极 -> Ground
Pico 3.3V -> 喇叭正极
喇叭负极 -> 三极管C集电极

> 在base signal pin与emitter ground之间并联一个无极性0.47uf电容能让音质变好。
```
