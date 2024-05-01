"""
Notes from yingshaoxo:

Do you know what is speaker? I mean a device, not people.
It is a device that takes two current line to make some sound to the air. The two line means a positive current line and a negative current line. (You may buy some speakers that do not provide two lines, you'd better return it, because you can't use it later freely. They are decreasing your power.)
The positive line carrys the audio signal, while the negative line always keeps 0 voltage.

Then, let's talk about sound data in your computers.
A general sound file is end up with ".wav". Sound inside is saved as a sine wave. But it is not a perfect sine wave.
Sometimes, if the sound volumn go up, the absolute height of the signal graph goes up, if the sound volumn go down, the absolute height of the signal graph goes down. When you meet silence of a sound, you will see a stright horizontal line in 0dB.
As you know, in computer, a line is composed with points. Sound wave is also made by points. For example, in 8K Hz audio, there could have 8k points per second. If you use a 0~5V microcontroller to drive a speaker, each point would be a value between 0 and 5.
But so far, what I have mentioned is mono audio, which just have one channel, one sound. You may also see people record two channels, one for left ear, another for right ear, they call it stereo. How to represente and play the two channel data?
Just think about a list: [left_data_0, right_data_1, left_data_2, right_data_3, ...]
When you hear a two channel audio, what the speaker really does is play right data after it play the left data, so on and so on. Because the switch speed is very quick, so you think the left and right channel is playing at the same time, but that's not true. It is just a sequence playing.
Maybe I was wrong, they can use two speakers to play different channels for better experimence.

Then let's talk about headphone audio jack data or the data that come from your old mp3 device audio output line, normally it is a green line.
You can simplely connect the ground to your microcontroller ground, and connect the signal line to your microcontroller analog line, so you can get the audio data by using microcontroller.
"""


class Audio():
    def __init__(self):
        try:
            import wave
            self.wave_module = wave
        except Exception as e:
            print(e)
            self.wave_module = None

    def set_raw_data(self, raw_data, sample_rate=44100):
        """
        raw_data: list of list
            [[channel1_data_list], [channel2_data_list], ...]
            normally, if it has 1 list inside, it is a mono audio, if it has 2 list inside, it is a stereo audio
            left ear first, right ear second
        sample_rate: int
            (len(mono_raw_data) / sample_rate) == n_samples per second
        """
        self.sample_rate = sample_rate
        self.raw_data = raw_data

    def get_shape(self):
        """
        return (channels_number, channel_length)
        """
        channel_number = len(self.raw_data)
        if channel_number == 0:
            return 0, 0
        else:
            return channel_number, len(self.raw_data[0])

    def copy(self):
        another_audio = Audio()

        channel_number = len(self.raw_data)
        new_data = [None] * channel_number
        for index in range(channel_number):
            new_data[index] = self.raw_data[index].copy()

        another_audio.set_raw_data(new_data, self.sample_rate)

        return another_audio

    def resize(self, x_size, y_size=None, adds=0):
        if x_size != None:
            x_size = int(x_size)

        channels_number, one_channel_length = self.get_shape()

        ratio = one_channel_length / x_size
        part_width = int(ratio)
        #if ratio != part_width:
        #    print("We recommand you use a x_size that could make: " + str(one_channel_length) + " / x_size" + " == " + str(int(part_width)))
        sample_rate = int(round(self.sample_rate/ratio))

        for channel_index in range(channels_number):
            new_list = [None] * x_size
            index = 0
            index2 = 0
            #max_value = -32768
            while True:
                signal = self.raw_data[channel_index][index]
                if index2 >= x_size:
                    break
                new_list[index2] = signal
                #if signal > max_value:
                #    max_value = signal
                index += part_width
                index2 += 1
                if index >= one_channel_length:
                    break
            for index in range(index2, x_size):
                new_list[index] = 0
            self.raw_data[channel_index] = new_list

        self.sample_rate = sample_rate

        return self

    def merge_to_mono(self):
        a_audio = self.copy()
        channels_number, one_channel_length = a_audio.get_shape()

        new_data = [None] * one_channel_length
        for index in range(one_channel_length):
            a_list = []
            for channel_index in range(channels_number):
                value = a_audio.raw_data[channel_index][index]
                a_list.append(value)
            new_data[index] = int(sum(a_list)/channels_number)

        a_audio.raw_data = [new_data]

        return a_audio

    def change_volume(self, scale=1.0):
        channels_number, one_channel_length = self.get_shape()
        for channel_index in range(channels_number):
            for x in range(one_channel_length):
                signal = self.raw_data[channel_index][x]
                self.raw_data[channel_index][x] = int(self.raw_data[channel_index][x] * scale)
        return self

    def read_wav_file(self, wav_file_path):
        if self.wave_module == None:
            return None

        wav_object = self.wave_module.open(wav_file_path)
        int_width = wav_object.getsampwidth() #they save int differently, maybe two int as one int
        channels = wav_object.getnchannels()
        frame_rate = wav_object.getframerate() #44100
        number_of_frames = wav_object.getnframes() * 2 * channels
        signal_list = wav_object.readframes(number_of_frames)

        raw_data = []
        one_channel_number = int(number_of_frames/channels/2)
        for _ in range(channels):
            raw_data.append([None] * one_channel_number)
        second_index_list = []
        for _ in range(channels):
            second_index_list.append(0)

        signal_index = 0
        index = 0
        while True:
            signal_int16_list = signal_list[signal_index: signal_index + int_width]
            signal = int.from_bytes(signal_int16_list, byteorder='little', signed=True)
            #signal = struct.unpack("<" + "h" * int(len(signal_int16_list) / int_width), signal_int16_list)[0]
            # signal is a number between -32767 and 32767

            raw_data[index][second_index_list[index]] = signal
            second_index_list[index] += 1
            index += 1
            if index >= channels:
                index = 0

            signal_index += int_width
            if signal_index >= number_of_frames:
                break

        self.set_raw_data(raw_data, frame_rate)

        wav_object.close()
        return self

    def write_wav_file(self, wav_file_path):
        import struct
        sample_rate = self.sample_rate
        channels_number, one_channel_length = self.get_shape()

        wav_object = self.wave_module.open(wav_file_path, 'w')
        wav_object.setnchannels(channels_number)
        wav_object.setsampwidth(2)
        wav_object.setframerate(sample_rate)

        for index in range(one_channel_length):
            for channel_index in range(channels_number):
                value = self.raw_data[channel_index][index]
                value = max(min(value, 32767), -32767)
                data = struct.pack('<h', value)
                wav_object.writeframesraw(data)

        wav_object.close()

    def save_to_file(self, file_path):
        sample_rate = self.sample_rate
        channels_number, one_channel_length = self.get_shape()

        text_data = "sample_rate," + str(sample_rate) + ",channels_number," + str(channels_number) + ",one_channel_length," + str(one_channel_length)
        text_data += "\n_______\n\n"
        for channel_index in range(channels_number):
            last_value = 0
            for index in range(one_channel_length):
                real_value = self.raw_data[channel_index][index]
                value = real_value - last_value
                last_value = value
                text_data += str(value) + ","
            text_data += "\n_______\n\n"

        file = open(file_path, "w", encoding="utf-8")
        file.write(text_data)
        file.close()

    def get_smooth_audio(self):
        a_audio = self.copy()
        channels_number, one_channel_length = a_audio.get_shape()

        for channel_index in range(channels_number):
            last_value = 0
            for index in range(one_channel_length):
                real_value = a_audio.raw_data[channel_index][index]
                value = real_value - last_value
                value = max(min(value, 32767), -32767)
                last_value = value
                a_audio.raw_data[channel_index][index] = value

        return a_audio

    def get_simplified_audio(self, ratio=0.7):
        """
        a_audio = self.copy()
        channels_number, one_channel_length = a_audio.get_shape()

        for channel_index in range(channels_number):
            new_data_list = []
            for index in range(one_channel_length):
                signal = a_audio.raw_data[channel_index][index]
                if signal >= 0:
                    new_data_list.append(signal)
            a_audio.raw_data[channel_index] = new_data_list
        a_audio.sample_rate = int(a_audio.sample_rate/2)

        _, max_length = a_audio.get_shape()
        for channel_index in range(channels_number):
            length = len(a_audio.raw_data[channel_index])
            if length > max_length:
                max_length = length

        for channel_index in range(channels_number):
            new_data_list = [None] * max_length
            old_length = len(a_audio.raw_data[channel_index])
            for index in range(max_length):
                if index >= old_length:
                    signal = 0
                else:
                    signal = a_audio.raw_data[channel_index][index]
                new_data_list[index] = signal
            a_audio.raw_data[channel_index] = new_data_list

        return a_audio
        """
        ratio = 1 - ratio
        audio = self.copy()
        channels_number, one_channel_length = audio.get_shape()
        audio = audio.resize(one_channel_length * ratio, adds=6277)
        audio = audio.merge_to_mono()
        #audio = audio.get_smooth_audio()
        audio = audio.change_volume(1.5)
        return audio

    def print(self, save_to_png_file_path=None):
        from auto_everything.image import Image
        a_image = Image()

        a_audio = self.copy()
        channels_number, one_channel_length = a_audio.get_shape()

        one_audio_height = 480
        half_of_one_audio_height = int(one_audio_height / 2)

        height = one_audio_height * channels_number
        width = 854
        a_image = a_image.create_an_image(height, width)

        line_length = 10
        a_audio.resize(x_size=int(width/line_length))
        channels_number, one_channel_length = a_audio.get_shape()

        for channel_index in range(channels_number):
            last_y = channel_index * one_audio_height
            last_x = 0
            for x in range(one_channel_length):
                signal = a_audio.raw_data[channel_index][x]
                small_signal_in_y = abs(signal / 32767) * half_of_one_audio_height
                if signal > 0:
                    y = small_signal_in_y + half_of_one_audio_height
                elif signal <= 0:
                    y = half_of_one_audio_height - small_signal_in_y
                y = int(y)
                if y >= one_audio_height:
                    continue
                y += channel_index * one_audio_height
                x *= line_length

                horizontal_line = False
                vertical_line = False
                normal_line = False
                upper_part = y - last_y
                lower_part = x - last_x
                if upper_part == 0:
                    horizontal_line = True
                elif lower_part == 0:
                    vertical_line = True
                else:
                    normal_line = True
                    slop = upper_part / lower_part
                    for x_index in range(last_x, x):
                        y_index = int(slop*(x_index-last_x) + last_y)
                        a_image.raw_data[y_index][x_index] = [0,255,0,255]
                        try:
                            a_image.raw_data[y_index][x_index+1] = [0,255,0,255]
                            a_image.raw_data[y_index][x_index-1] = [0,255,0,255]
                            a_image.raw_data[y_index+1][x_index] = [0,255,0,255]
                            a_image.raw_data[y_index-1][x_index] = [0,255,0,255]
                        except Exception as e:
                            pass

                last_y = y
                last_x = x

        a_image.print(100)
        return a_image


if __name__ == "__main__":
    audio = Audio()
    audio = audio.read_wav_file("/home/yingshaoxo/Downloads/handclap.wav")
    channels_number, one_channel_length = audio.get_shape()
    #audio.resize(one_channel_length * 0.2)
    audio = audio.get_simplified_audio()
    #audio.change_volume(0.5)
    #audio = audio.merge_to_mono()
    #audio = audio.get_smooth_audio()
    #a_image = audio.print()
    #a_image.save_image_to_file_path("/home/yingshaoxo/Downloads/handclap2.png")
    audio.write_wav_file("/home/yingshaoxo/Downloads/test_smooth.wav")
    #audio.save_to_file("/home/yingshaoxo/Downloads/handclap2.wav.txt")
