import pyaudio
import wave
import struct
import sys
import argparse
from multiprocessing import Process, Queue
from auto_everything.audio_ import Audio

def int_or_str(text):
    """Helper function for argument parsing."""
    try:
        return int(text)
    except ValueError:
        return text

def list_devices():
    """列出所有音频设备"""
    p = pyaudio.PyAudio()
    for i in range(p.get_device_count()):
        dev = p.get_device_info_by_index(i)
        print("Device {}: {} (输入通道: {})".format(i, dev['name'], dev['maxInputChannels']))
    p.terminate()

def save_audio(audio_data, path):
    """保存音频数据为WAV文件"""
    if audio_data:
        print("正在保存 {} 个样本...".format(len(audio_data)))
        with wave.open(path, "wb") as wav:
            wav.setnchannels(1)
            wav.setsampwidth(2)  # 16-bit = 2 bytes
            wav.setframerate(8000)
            wav.writeframes(struct.pack('<{}h'.format(len(audio_data)), *audio_data))
        print("音频已保存为 {}".format(path))

def count_wave_as_frequency(data):
    count_wave = 0
    index = 0
    while index < len(data):
        a_byte = data[index]
        if a_byte < 0:
            while index < len(data):
                a_byte = data[index]
                if a_byte > 0:
                    while index < len(data):
                        a_byte = data[index]
                        if a_byte < 0:
                            count_wave += 1
                            index -= 1
                            break
                        index += 1
                    break
                index += 1
        index += 1
    return count_wave

def parse_audio(audio_data):
    a_audio = Audio()
    a_audio.set_raw_data(audio_data, sample_rate=8000)
    return a_audio.to_hash()

def parse_audio_4(audio_data):
    # record when volume and frequency both change, in sliding window or gate
    a_audio = Audio()
    a_audio.set_raw_data(audio_data, sample_rate=8000)
    a_audio = a_audio.reduce_noise_by_subtraction(use_global_value=True, global_value=0.1)
    has_sound_list = []
    audio_data = list(a_audio.raw_data[0])
    audio_data_absolute = list([abs(one) for one in a_audio.raw_data[0]])
    length = len(audio_data_absolute)
    time_range_length = 1600
    for index in range(time_range_length, length):
        left_part = audio_data_absolute[index-time_range_length:index]
        if len(left_part) < time_range_length:
            continue
        left_sum = sum(left_part)
        left_average_value = left_sum / time_range_length

        right_part = audio_data_absolute[index:index+time_range_length]
        if len(right_part) < time_range_length:
            continue
        right_sum = sum(right_part)
        right_average_value = right_sum / time_range_length

        if (right_average_value > (left_average_value * 1.1)):
            left_raw_part = audio_data[index-time_range_length:index]
            left_frequency = count_wave_as_frequency(left_raw_part)
            right_raw_part = audio_data[index:index+time_range_length]
            right_frequency = count_wave_as_frequency(right_raw_part)
            if (abs(left_frequency-right_frequency) > 15):
                has_sound_list.append(str(index/length)[:4])
    new_fucking_index = []
    last_index = None
    for one in has_sound_list:
        if one[:3] != last_index:
            new_fucking_index.append(float(one))
        last_index = one[:3]
    #return new_fucking_index
    data_part_list = []
    for one in new_fucking_index:
        temp_index = int(length * one)
        temp_data = a_audio.raw_data[0][temp_index: temp_index+1600]
        data_part_list.append(temp_data)
    final_data_list = []
    for one in data_part_list:
        final_data_list.append(count_wave_as_frequency(one))
    if len(final_data_list) > 0:
        max_value = max(final_data_list)
        final_data_list = [int(one/max_value*5) for one in final_data_list]
    return final_data_list

def real_audio_processing_function(input_queue, sample_rate=8000):
    audio_data = []
    recording = False
    threshold = 200

    while not input_queue.empty():
        input_queue.get()

    has_sound_counting = 0
    no_sound_counting = 0
    while True:
        data = input_queue.get()  # 阻塞等待数据
        if type(data) == str:
            if data.startswith("end"):
                path = data.split(":")[1]
                #save_audio(audio_data, path)
                break

        volume = max(abs(x) for x in data)
        if volume >= threshold and not recording:
            has_sound_counting += 1
            if has_sound_counting > 10:
                recording = True
                print("has sound, start recording... (press enter to stop)")
        else:
            has_sound_counting = 0

        if recording:
            #print(len(data))
            audio_data.extend(data)
            if volume < threshold:
                no_sound_counting += 1
            if volume >= threshold:
                no_sound_counting = 0
            if no_sound_counting >= 100:
                # half second
                #save_audio(audio_data[:-70*80], "./output.wav")
                result = parse_audio(audio_data[:-70*80])
                print(result)
                break

def pyaudio_main_process(input_queue, sample_rate=8000):
    """PyAudio 主进程"""
    parser = argparse.ArgumentParser(add_help=False)
    parser.add_argument(
        "-l", "--list-devices", action="store_true",
        help="显示音频设备列表并退出")
    args, remaining = parser.parse_known_args()

    if args.list_devices:
        list_devices()
        parser.exit(0)

    parser = argparse.ArgumentParser(
        description="实时麦克风音频录制",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        parents=[parser])
    parser.add_argument(
        "-d", "--device", type=int_or_str,
        help="输入设备（ID或名称子串）")
    parser.add_argument(
        "-r", "--samplerate", type=int, default=sample_rate,
        help="采样率（默认8000Hz）")
    args = parser.parse_args(remaining)

    # PyAudio 配置
    p = pyaudio.PyAudio()

    # 选择设备
    device_index = None
    if args.device is not None:
        for i in range(p.get_device_count()):
            dev = p.get_device_info_by_index(i)
            if str(args.device) in dev["name"]:
                device_index = i
                break
        if device_index is None:
            print("未找到指定设备，使用默认设备")
    else:
        # 使用默认输入设备
        device_info = p.get_default_input_device_info()
        if device_info is None:
            print("未找到默认输入设备")
            p.terminate()
            sys.exit(1)
        device_index = device_info["index"]

    # 计算每次回调的样本数（10ms = 80个样本 @8000Hz）
    frames_per_buffer = int(args.samplerate * 0.01)  # 10ms

    def callback(in_data, frame_count, time_info, status):
        """PyAudio 回调函数（每10ms调用一次）"""
        #if status:
        #    print("回调状态: {}".format(status), file=sys.stderr)
        # 将原始字节数据转换为整数列表（16-bit PCM）
        audio_data = list(struct.unpack('<{}h'.format(frame_count), in_data))
        input_queue.put(audio_data)
        return (None, pyaudio.paContinue)

    # 打开音频流
    stream = p.open(
        format=pyaudio.paInt16,  # 16-bit PCM
        channels=1,              # 单声道
        rate=args.samplerate,    # 采样率
        input=True,              # 输入模式
        input_device_index=device_index,
        frames_per_buffer=frames_per_buffer,
        stream_callback=callback
    )

    stream.start_stream()

    folder_name = "./"
    #folder_name = "/home/yingshaoxo/Downloads/audio_test_data/music/"
    index = 0
    while True:
        #input("\nwant to start a new record?")
        a_process = Process(
            target=real_audio_processing_function,
            args=(input_queue,)
        )
        a_process.start()
        #input("want to stop?")
        #input_queue.put("end:" + folder_name+str(index)+".wav")
        a_process.join()
        index += 1


if __name__ == "__main__":
    input_queue = Queue()
    pyaudio_main_process(input_queue)
    # 1. try to parse the audio input in real time, which is only parse audio that has sound, ignore silence
    # 2. do real time wave counting, so that we could get frequency number
