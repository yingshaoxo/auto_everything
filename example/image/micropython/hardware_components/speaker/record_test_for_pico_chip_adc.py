from machine import freq
# 载波频率：设为 125kHz
#freq(168000000)
freq(240000000)

from machine import Pin, PWM, Timer
import time

# 喇叭两根线：一根接 GP5，一根接 GND
# 注意：如果声音小，可以加个 8050 三极管放大，或者接功放模块
audio_pin = Pin(22)
pwm = PWM(audio_pin)

pwm.freq(125000)

class PWM_Audio:
    def __init__(self, pwm_obj):
        self.pwm = pwm_obj

    def play_bytes(self, data):
        for byte in data:
            # 0-255 映射到 0-65535
            # 使用左移 8 位比乘法快
            self.pwm.duty_u16(byte << 8)
            # 8000Hz = 每 125 微秒一个点. 考虑到代码执行耗时，大约延时 110-120us
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
                    chunk = f.read(16000)
                    if not chunk:
                        break
                    
                    for byte in chunk:
                        # 0-255 映射到 0-65535
                        self.pwm.duty_u16(byte << 8)
                        
                        # 8000Hz = 每 125 微秒一个点
                        # 考虑到代码执行耗时，大约延时 110-120us
                        time.sleep_us(rate) 
                
                self.pwm.duty_u16(0)
                print("播放结束")
        except Exception as e:
            print("错误:", e)


player = PWM_Audio(pwm)

#method 2, works even when the frequency change
from machine import ADC, Pin
import time

sample_rate = 11000 # 11khz
delay_time = int((1000 * 1000) / sample_rate)
print("delay time:", delay_time)

def record_sound():
    adc = ADC(Pin(26))          # create ADC object on ADC pin
    record_length_in_second = 5
    bytes_length = sample_rate * record_length_in_second
    temp_bytes = bytearray(1)
    index = 0
    # read value, 0-65535 across voltage range 0.0v - 3.3v, then to 0~255
    with open("tmp/temp_wav.binary", "wb") as f:
        f.write(b"")
    with open("tmp/temp_wav.binary", "ab") as f:
        for _ in range(bytes_length):
            last_time = time.ticks_us()
            temp_bytes[0] = adc.read_u16() >> 8
            f.write(temp_bytes)
            time.sleep_us(delay_time - (time.ticks_us() - last_time))
            index += 1
            if index > bytes_length:
                break

def replay_sound():
    player.play_file("tmp/temp_wav.binary", delay_time)

#if get_value_by_key_("recorded") == "true":
#    real_print_("replay start...")
#    replay_sound()
#    set_value_by_key_("recorded", "false")
#    real_print_("replay end.")
#else:
#    real_print_("record start...")
#    record_sound()
#    set_value_by_key_("recorded", "true")
#    real_print_("record end.")

def real_print_(a_text):
    print(a_text)

real_print_("record start...")
record_sound()
real_print_("record end.")

real_print_("replay start...")
replay_sound()
real_print_("replay end.")
