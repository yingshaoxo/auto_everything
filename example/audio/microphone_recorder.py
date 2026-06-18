import pyaudio
import wave
import struct
import sys
import argparse
from multiprocessing import Process, Queue

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

def real_audio_processor(input_queue, sample_rate=8000):
    audio_data = []
    #recording = False
    threshold = 200

    while not input_queue.empty():
        input_queue.get()

    while True:
        data = input_queue.get()  # 阻塞等待数据
        if type(data) == str:
            if data.startswith("end"):
                path = data.split(":")[1]
                save_audio(audio_data, path)
                break
        audio_data.extend(data)
        ## 检测声音
        #volume = max(abs(x) for x in data)
        #if volume >= threshold and not recording:
        #    print("has sound, start recording... (press enter to stop)")
        #    recording = True

        #if recording:
        #    #print(len(data))
        #    audio_data.extend(data)

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
        input("\nwant to start a new record?")
        a_process = Process(
            target=real_audio_processor,
            args=(input_queue,)
        )
        a_process.start()
        input("want to stop?")
        input_queue.put("end:" + folder_name+str(index)+".wav")
        a_process.join()
        index += 1


if __name__ == "__main__":
    input_queue = Queue()
    pyaudio_main_process(input_queue)
