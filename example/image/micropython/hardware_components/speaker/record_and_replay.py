from gc import mem_free
print("current memory: ", mem_free()/1024, "KB.")


from machine import freq
freq(240000000) # higher frequency will help you get better record sound
from machine import Pin, PWM
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
            # 8000Hz = 每 125 微秒一个点
            time.sleep_us(125)

    def play_raw_data(self, data):
        for byte in data:
            # 0-65535
            self.pwm.duty_u16(byte)
            time.sleep_us(125)

    def play_end(self):
        self.pwm.duty_u16(0)

    def play_file(self, filename, rate=125):
        """
        建议将歌曲转换成 raw 二进制格式（每个字节代表一个采样点值 0-255）
        """
        try:
            with open(filename, "rb") as f:
                print("开始播放...")
                while True:
                    chunk = f.read(8000)
                    if not chunk:
                        break

                    for byte in chunk:
                        # 0-255 映射到 0-65535
                        self.pwm.duty_u16(byte << 8)
                        # 8000Hz = 每 125 微秒一个点
                        time.sleep_us(rate)
                self.pwm.duty_u16(0)
                print("播放结束")
        except Exception as e:
            print("错误:", e)

# ======================
# 3. 播放
# ======================
player = PWM_Audio(pwm)
#player.play_file("song_mini_small.binary")

# record and replay
from machine import ADC, Pin
adc = ADC(Pin(26)) # record microphone positive pin connect to pin 26

record_length_in_second = 2
sample_rate = 8000 #8khz
sample_bytes_array = [255] * (sample_rate * record_length_in_second)
print("start record...")
for i in range(len(sample_bytes_array)):
    sample_bytes_array[i] = adc.read_u16() >> 8  # read value, 0-65535 across voltage range 0.0v - 3.3v, then convert to 0~255
    time.sleep_us(125)
print("play record...")
player.play_raw_data([one << 8 for one in sample_bytes_array])
print("done")


from gc import mem_free
print("current memory: ", mem_free()/1024, "KB.")
"""
## method 1, should work when time will not change when frequency change
#from machine import ADC, Pin
#adc = ADC(Pin(26))          # create ADC object on ADC pin
#record_length_in_second = 5
#sample_rate = 8000 #8khz
#sample_bytes_array = bytearray(sample_rate)
#index = 0
#with open("temp_wav.binary", "wb") as f:
#    f.write(b"")
#while True:
#    for i in range(sample_rate):
#        sample_bytes_array[i] = adc.read_u16() >> 8 # read value, 0-65535 across voltage range 0.0v - 3.3v, then to 0~255
#        time.sleep_us(125)
#    index += 1
#    with open("temp_wav.binary", "ab") as f:
#        f.write(sample_bytes_array)
#    if index > record_length_in_second:
#        break
#print("done")
#player.play_file("temp_wav.binary")


#method 2, works even when the frequency change
from machine import ADC, Pin
import time
adc = ADC(Pin(26))          # create ADC object on ADC pin

record_length_in_second = 5
sample_rate = 5555 #5.555khz
sample_bytes_array = bytearray(sample_rate)
index = 0
with open("temp_wav.binary", "wb") as f:
    f.write(b"")
while True:
    last_time = time.ticks_us()
    for i in range(sample_rate):
        last_time = time.ticks_us()
        sample_bytes_array[i] = adc.read_u16() >> 8 # read value, 0-65535 across voltage range 0.0v - 3.3v, then to 0~255
        time.sleep_us(180 - (time.ticks_us() - last_time))
    index += 1
    with open("temp_wav.binary", "ab") as f:
        f.write(sample_bytes_array)
    if index > record_length_in_second:
        break
print("done")
player.play_file("temp_wav.binary", 180)


#method 3, small steps to gain best quality
from machine import ADC, Pin
import time
adc = ADC(Pin(26))          # create ADC object on ADC pin

record_length_in_second = 10
sample_rate = 11000 # 11khz
delay_time = int((1000 * 1000) / sample_rate)
print("delay time:", delay_time)
bytes_length = sample_rate * record_length_in_second
temp_bytes = bytearray(1)
index = 0
# read value, 0-65535 across voltage range 0.0v - 3.3v, then to 0~255
with open("temp_wav.binary", "wb") as f:
    f.write(b"")
with open("temp_wav.binary", "ab") as f:
    for _ in range(bytes_length):
        last_time = time.ticks_us()
        temp_bytes[0] = adc.read_u16() >> 8
        f.write(temp_bytes)
        time.sleep_us(delay_time - (time.ticks_us() - last_time))
        index += 1
        if index > bytes_length:
            break
print("done")
player.play_file("temp_wav.binary", delay_time)
"""
