"""
Notes from yingshaoxo:

Do you know what is speaker? I mean a device, not people.
It is a device that takes two current line to make some sound to the air. The two line means a positive current line and a negative current line. (You may buy some speakers that do not provide two lines, you'd better return it, because you can't use it later freely. They are decreasing your power.)
The positive line carrys the audio signal, while the negative line always keeps 0 voltage.

Then, let's talk about sound data in your computers.
A general sound file is end up with ".wav". Sound inside is saved as a sine wave. But it is not a perfect sine wave.
Sometimes, if the sound volumn go up, the absolute height of the signal graph goes up, if the sound volumn go down, the absolute height of the signal graph goes down. When you meet silence of a sound, you will see a stright horizontal line in 0dB.
As you know, in computer, a line is composed with points. Sound wave is also made by points. For example, in 8K Hz audio, there could have 8k points per second. If you use a 0~5V microcontroller to drive a speaker, each point would be a value between 0 and 5. (the speaker here can be the type that can put into your ear)
But so far, what I have mentioned is mono audio, which just have one channel, one sound. You may also see people record two channels, one for left ear, another for right ear, they call it stereo. How to represente and play the two channel data?
Just think about a list: [left_data_0, right_data_1, left_data_2, right_data_3, ...]
When you hear a two channel audio, what the speaker really does is play right data after it play the left data, so on and so on. Because the switch speed is very quick, so you think the left and right channel is playing at the same time, but that's not true. It is just a sequence playing.
Maybe I was wrong, they can use two speakers to play different channels for better experimence.

Then let's talk about headphone audio jack data or the data that come from your old mp3 device audio output line, normally it is a green line.
You can simplely connect the ground to your microcontroller ground, and connect the signal line to your microcontroller analog line, so you can get the audio data by using microcontroller.

Here is an example I copied from internet that shows you how to use microcontroller to play music:
    It plays 8-bit PCM audio on pin 11 using pulse-width modulation (PWM). It uses two timers. The first changes the sample value 8000 times a second. The second holds pin 11 high for 0-255 ticks out of a 256-tick cycle, depending on the sample value. The second timer repeats 62500 times per second (16000000 / 256), which is much faster than the playback rate (8000 Hz), so it almost sounds halfway decent.
    https://docs.arduino.cc/learn/programming/audio
In other words, it uses two line to connect speaker, one is ground, another is 0 to 5v analog line, the audio data will be converted into (0, 5)v, the change speed for the red line is 8000 times per second, which means 8kHz.

As for dB unit, 0dB means full volume and positive numbers means a boost in volume, while negative numbers mean a dedrease in volume. dB = 20*log10(abs(value)/32768). abs(value) = 10^(db/20)*32768.

The funny part about audio is that for same volume, some sound may sounds like bass, another may sounds like gutar. The low_pass or high_pass audio filter is not simply rely on volume. It depends on repeating time and vibration frequency.
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
            (len(mono_raw_data) / sample_rate) == audio seconds
        """
        self.sample_rate = sample_rate # one second play sample_rate number of data
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

    def get_samples_number_per_second(self):
        return self.sample_rate

    def get_audio_length_in_second(self):
        channels_number, one_channel_length = self.get_shape()
        return one_channel_length / self.sample_rate

    def copy(self):
        another_audio = Audio()

        channel_number = len(self.raw_data)
        new_data = [None] * channel_number
        for index in range(channel_number):
            new_data[index] = self.raw_data[index].copy()

        another_audio.set_raw_data(new_data, self.sample_rate)

        return another_audio

    def change_sample_rate(self, sample_rate, speed_mode=False):
        """
        sample_rate: int
            can be 8000, 16000, and so on
        """
        # we can scale it up first, then scale it down
        old_sample_rate = self.sample_rate
        channels_number, one_channel_length = self.get_shape()
        if (sample_rate >= old_sample_rate):
            return self

        ratio = old_sample_rate / sample_rate

        if speed_mode == True:
            part_width = int(round(ratio))
            x_size = int(round(one_channel_length / ratio))

            for channel_index in range(channels_number):
                new_list = [None] * x_size
                index = 0
                index2 = 0
                while True:
                    last_index = index - part_width
                    if last_index >= 0:
                        signal_list = self.raw_data[channel_index][last_index:index]
                        signal = int(round(sum(signal_list) / part_width))
                    else:
                        signal = self.raw_data[channel_index][index]
                    if index2 >= x_size:
                        break
                    new_list[index2] = signal
                    index += part_width
                    index2 += 1
                    if index >= one_channel_length:
                        break
                for index in range(index2, x_size):
                    new_list[index] = 0
                self.raw_data[channel_index] = new_list
        else:
            part_width = ratio
            x_size = int(round(one_channel_length / ratio))

            for channel_index in range(channels_number):
                new_list = [None] * x_size
                index = 0
                index2 = 0
                while True:
                    last_index = round(index - part_width)
                    if last_index >= 0:
                        signal_list = self.raw_data[channel_index][last_index:round(index)]
                        signal = int(round(sum(signal_list) / part_width))
                    else:
                        signal = self.raw_data[channel_index][round(index)]
                    if index2 >= x_size:
                        break
                    new_list[index2] = signal
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
            new_data[index] = int(round(sum(a_list)/channels_number))

        a_audio.raw_data = [new_data]

        return a_audio

    def change_volume(self, scale=1.0):
        channels_number, one_channel_length = self.get_shape()
        for channel_index in range(channels_number):
            for x in range(one_channel_length):
                signal = self.raw_data[channel_index][x]
                self.raw_data[channel_index][x] = int(round(self.raw_data[channel_index][x] * scale))
        return self

    def get_simplified_audio(self, ratio=0.7, extreme=False):
        ratio = 1 - ratio
        audio = self.copy()
        channels_number, one_channel_length = audio.get_shape()
        audio = audio.change_sample_rate(8000)
        audio = audio.merge_to_mono()
        audio = audio.reduce_noise_by_counting(ratio)
        audio = audio.change_volume(1.5)
        if extreme == True:
            audio = audio.range_map_with_bug(-32767, 32767, 0, 32767)
            audio = audio.change_volume(1.5)
        return audio

    def reduce_noise_by_frequency(self):
        """
        garbage code, won't work
        """
        def high_pass_filter(data_list, sample_rate, high_pass_frequency):
            import math
            dt = 1/sample_rate
            RC = 1/(2*3.14159265358979323846*high_pass_frequency)
            alpha = RC / (RC + dt)

            filtered_data = [0] * len(data_list)
            for i in range(1, len(data_list)):
                filtered_data[i] = round(alpha * filtered_data[i-1] + alpha * (data_list[i] - data_list[i-1]))

            return filtered_data

        channels_number, one_channel_length = self.get_shape()
        for channel_index in range(channels_number):
            new_data_list = high_pass_filter(self.raw_data[channel_index].copy(), self.sample_rate, 8500)
            self.raw_data[channel_index] = new_data_list
        self.change_volume(7)
        return self

    def reduce_noise_by_counting(self, ratio=0.7):
        """
        One way is to count sound frequency, cut low frequency stuff, or save middle frequency stuff
        Another way is to use OBS noise reducing tech, rnn noise
        Maybe cubic smoothing splines also works
        """
        ratio = 1 - ratio
        signal_dict = {}

        channels_number, one_channel_length = self.get_shape()
        for channel_index in range(channels_number):
            for index in range(one_channel_length):
                signal = self.raw_data[channel_index][index]
                if signal in signal_dict:
                    signal_dict[signal] += 1
                else:
                    signal_dict[signal] = 1

        signal_item_list = list(signal_dict.items())
        signal_item_list.sort(key=lambda x: -x[1])
        remain_number = int(ratio * len(signal_item_list))
        remain_signal_item_list = signal_item_list[:remain_number]
        new_signal_dict = {}
        for key, value in remain_signal_item_list:
            new_signal_dict[key] = 0

        cache_dict = {}
        for channel_index in range(channels_number):
            for index in range(one_channel_length):
                signal = self.raw_data[channel_index][index]
                if signal in new_signal_dict:
                    pass
                else:
                    if signal not in cache_dict:
                        min_distance = 999999
                        target_signal = 0
                        for one in new_signal_dict.keys():
                            distance = abs(one - signal)
                            if distance < min_distance:
                                min_distance = distance
                                target_signal = one
                        cache_dict[signal] = target_signal
                    else:
                        target_signal = cache_dict[signal]
                    self.raw_data[channel_index][index] = target_signal
        return self

    def reduce_noise_by_value(self, noise_audio=None, reducing_factor=0.5, kernel=1):
        """
        noise_audio: Audio
            the audio that only contains noise

        Just like adobe audition, you can filter out those noise by give a a list of noise sample data
        """
        a_audio = self.copy()

        noise_raw_data = noise_audio.raw_data[0]
        noise_data_dict = {}
        for one in noise_raw_data:
            noise_data_dict[one] = 0

        channels_number, one_channel_length = a_audio.get_shape()
        for channel_index in range(channels_number):
            new_data_list = a_audio.raw_data[channel_index].copy()
            for index in range(one_channel_length):
                signal = a_audio.raw_data[channel_index][index]
                if signal in noise_data_dict:
                    new_value = round(signal * reducing_factor)
                    a_audio.raw_data[channel_index][index] = new_value
                    if kernel > 0:
                        for i in range(index-kernel, index+kernel):
                            if i>=0 and i < one_channel_length:
                                new_data_list[i] = new_value
            if kernel > 0:
                a_audio.raw_data[channel_index] = new_data_list

        self.raw_data = a_audio.raw_data
        return self

    def reduce_noise_by_subtraction(self, noise_audio=None, threshold=None, use_first_x_second_noise=0.048, ratio=6):
        """
        useless
        """
        a_audio = self.copy()

        if threshold == None:
            if noise_audio == None:
                noise_numbers = round(a_audio.sample_rate*use_first_x_second_noise)
                noise_audio = Audio()
                noise_audio.raw_data = [a_audio.raw_data[0][:noise_numbers]]
            threshold = round(sum([abs(one) for one in noise_audio.raw_data[0]]) / len(noise_audio.raw_data[0]) * ratio)
        threshold = round(threshold)

        channels_number, one_channel_length = self.get_shape()
        for channel_index in range(channels_number):
            for index in range(one_channel_length):
                signal = self.raw_data[channel_index][index]
                absolute_signal = abs(signal)
                new_absolute_signal = absolute_signal - threshold
                if new_absolute_signal < 0:
                    new_absolute_signal = 0
                if signal >= 0:
                    self.raw_data[channel_index][index] = new_absolute_signal
                else:
                    self.raw_data[channel_index][index] = -new_absolute_signal

        return self

    def reduce_noise_by_gate(self, threshold=None, noise_audio=None, use_first_x_second_noise=0.048, kernel=105, top_noise_ratio=0.001, less_broken=True):
        """
        threshold: int
            1424, the mean value of noise, just signal number, no dB need
        noise_audio: Audio
            the audio that only contains noise

        This works better in pure human voice data.

        Then I get the volume of noise, for each 0.2 second, if the volume of it less or equal to noise volume, we set it to 0. Some people call this method "noise gate"
        When you use noise gate, if you think it is noise, you can get more noise data. for data you think is not noise by noise gate, you can still do volume decreseing on those noise inside by checking noise dict. then for those you think it is noise by using noise gate, you directly set it to 0.
        """
        a_audio = self.copy()

        if threshold == None:
            if noise_audio == None:
                noise_numbers = round(a_audio.sample_rate*use_first_x_second_noise)
                noise_audio = Audio()
                noise_audio.raw_data = [a_audio.raw_data[0][:noise_numbers]]
            threshold = sum([abs(one) for one in noise_audio.raw_data[0]]) / len(noise_audio.raw_data[0]) * 3

        noise_dict = {}
        channels_number, one_channel_length = a_audio.get_shape()
        for channel_index in range(channels_number):
            index = 0
            while True:
                signal = a_audio.raw_data[channel_index][index]
                end_index = index + kernel
                if end_index < one_channel_length:
                    raw_range_data = a_audio.raw_data[channel_index][index: end_index]
                    range_data = [abs(one) for one in raw_range_data]
                    average_value = sum(range_data) / len(range_data)
                    if average_value < threshold:
                        # silent the range
                        for i in range(index, end_index):
                            a_audio.raw_data[channel_index][i] = 0
                        index += kernel
                        for one in raw_range_data:
                            if one in noise_dict:
                                noise_dict[one] += 1
                            else:
                                noise_dict[one] = 1
                index += 1
                if index >= one_channel_length:
                    break

        signal_item_list = list(noise_dict.items())
        signal_item_list.sort(key=lambda x: -x[1])
        remain_number = round(top_noise_ratio * len(signal_item_list))
        remain_number = max(5, remain_number)
        remain_signal_item_list = signal_item_list[:remain_number]
        #print("It has " + str(remain_number) + " noise points.")
        new_noise_dict = {}
        for key, value in remain_signal_item_list:
            new_noise_dict[key] = 0

        for channel_index in range(channels_number):
            for index in range(one_channel_length):
                signal = a_audio.raw_data[channel_index][index]
                if signal in new_noise_dict:
                    a_audio.raw_data[channel_index][index] = round(signal/2)
                    #a_audio.raw_data[channel_index][index] = 0

        if less_broken == True:
            self.change_volume(0.1)
            a_audio.raw_data = a_audio.raw_data + self.raw_data
            self = a_audio.merge_to_mono()
        else:
            self.raw_data = a_audio.raw_data

        return self

    def reduce_noise_by_using_yingshaoxo_method(self, threshold=None, noise_audio=None, use_first_x_second_noise=0.048, kernel=100, less_broken=True):
        """
        threshold: int
            1424, the mean value of noise, just signal number, no dB need
        noise_audio: Audio
            the audio that only contains noise

        This works better in pure human voice data.
        """
        a_audio_backup = self.copy()
        a_audio = self.copy()

        if threshold == None:
            if noise_audio == None:
                noise_numbers = round(a_audio.sample_rate*use_first_x_second_noise)
                noise_audio = Audio()
                noise_audio.raw_data = [a_audio.raw_data[0][:noise_numbers]]
            threshold = sum([abs(one) for one in noise_audio.raw_data[0]]) / len(noise_audio.raw_data[0]) * 2.0

        channels_number, one_channel_length = a_audio.get_shape()
        for channel_index in range(channels_number):
            new_signal_list = [None] * one_channel_length
            index = 0
            while True:
                signal = a_audio.raw_data[channel_index][index]

                start_index = index - kernel
                end_index = index + kernel
                if start_index < 0:
                    start_index = 0
                if end_index > one_channel_length:
                    end_index = one_channel_length

                raw_range_data = a_audio.raw_data[channel_index][start_index: end_index]
                range_data = [abs(one) for one in raw_range_data]
                average_value = sum(range_data) / len(range_data)

                if average_value < threshold:
                    # silent the range
                    new_signal_list[index] = 0
                else:
                    # ignore sound
                    if abs(signal) < threshold:
                        new_signal_list[index] = round(signal / 2)
                    else:
                        new_signal_list[index] = signal
                index += 1
                if index >= one_channel_length:
                    break
            a_audio.raw_data[channel_index] = new_signal_list

        #a_audio.reduce_noise_by_value(noise_audio, reducing_factor=0.5, kernel=1)
        #need to find a way to mimic the audacity noise supression algorithm

        if less_broken == True:
            """
            new_audio = self.copy()
            new_audio.reduce_noise_by_gate()
            self.change_volume(0.1)
            a_audio.raw_data = a_audio.raw_data + new_audio.raw_data + self.raw_data
            self.raw_data = a_audio.merge_to_mono().raw_data
            self.change_volume(1.5)
            self.volume_db_limiter(-11, 0.7)
            """
            new_audio2 = self.copy()
            new_audio2.reduce_noise_by_subtraction()
            new_audio = self.copy()
            new_audio.reduce_noise_by_gate()
            self.change_volume(0.1)
            a_audio.raw_data = a_audio.raw_data + new_audio.raw_data + self.raw_data + new_audio2.raw_data
            self.raw_data = a_audio.merge_to_mono().raw_data
            self.change_volume(1.5)
            self.volume_db_limiter(-11, 0.7)

            a_audio_backup.change_volume(0.1)
            a_audio_backup.raw_data = a_audio_backup.raw_data + self.raw_data
            self.raw_data = a_audio_backup.merge_to_mono().raw_data
            self.change_volume(1.5)
            self.reduce_noise_by_subtraction(ratio=2)
        else:
            self.raw_data = a_audio.raw_data

        return self

    def volume_db_limiter(self, db=-13, reducing_factor=0.7):
        """
        db: int
            -90 means silence, 0 means full volume, >0 means strong sound that should get limited
        """
        max_absolute_signal = 10**(db/20) * 32768

        channels_number, one_channel_length = self.get_shape()
        for channel_index in range(channels_number):
            for index in range(one_channel_length):
                signal = self.raw_data[channel_index][index]
                absolute_signal = abs(signal)
                if absolute_signal > max_absolute_signal:
                    self.raw_data[channel_index][index] = round(signal*reducing_factor)

        return self

    def range_map_with_bug(self, original_min_value, original_max_value, min_value, max_value, use_int=True):
        """
        use_int: bool
            will make sure all result is integer
        has_negative_number: bool
            default True for wav, because it has negative numbers.
            if you want to convert range from (0,255) to (-32767, 32767), you have to set this to False

        You can use this function to convert self.raw_data into data that in range of (0, 3.3) or (0, 5) or (-32767, 32767), or (0, 1024) or (0, 255)
        """
        if original_min_value < 0:
            has_negative_number=True
        else:
            has_negative_number=False

        new_data_dict = {}
        #original_max_value = -999999
        #original_min_value = 999999
        channels_number, one_channel_length = self.get_shape()
        for channel_index in range(channels_number):
            for index in range(one_channel_length):
                signal = self.raw_data[channel_index][index]
                new_data_dict[signal] = signal
                #if signal > original_max_value:
                #    original_max_value = signal
                #if signal < original_min_value:
                #    original_min_value = signal

        original_range = original_max_value - original_min_value
        if original_range == 0:
            return self
        new_range = max_value - min_value
        half_new_range = new_range/2
        if new_range == 0:
            return self
        for key in new_data_dict.keys():
            value = new_data_dict[key]
            new_value = (value / original_range) * new_range
            if has_negative_number == True:
                if new_value >= 0:
                    new_value += half_new_range
                else:
                    new_value = half_new_range + new_value
            else:
                new_data_dict[key] = new_value

            if use_int == True:
                new_data_dict[key] = int(round(new_value))
            else:
                new_data_dict[key] = new_value

        for channel_index in range(channels_number):
            for index in range(one_channel_length):
                signal = self.raw_data[channel_index][index]
                self.raw_data[channel_index][index] = new_data_dict[signal]

        return self

    def range_map(self, original_min_value, original_max_value, min_value, max_value, use_int=True):
        """
        use_int: bool
            will make sure all result is integer
        has_negative_number: bool
            default True for wav, because it has negative numbers.
            if you want to convert range from (0,255) to (-32767, 32767), you have to set this to False

        You can use this function to convert self.raw_data into data that in range of (0, 3.3) or (0, 5) or (-32767, 32767), or (0, 1024) or (0, 255)
        """
        if original_min_value < 0:
            original_has_negative_number=True
        else:
            original_has_negative_number=False

        if min_value < 0:
            target_has_negative_number = True
        else:
            target_has_negative_number = False

        new_data_dict = {}
        #original_max_value = -999999
        #original_min_value = 999999
        channels_number, one_channel_length = self.get_shape()
        for channel_index in range(channels_number):
            for index in range(one_channel_length):
                signal = self.raw_data[channel_index][index]
                new_data_dict[signal] = signal
                #if signal > original_max_value:
                #    original_max_value = signal
                #if signal < original_min_value:
                #    original_min_value = signal

        original_range = original_max_value - original_min_value
        half_original_range = original_range/2
        if original_range == 0:
            return self
        new_range = max_value - min_value
        half_new_range = new_range/2
        if new_range == 0:
            return self
        for key in new_data_dict.keys():
            value = new_data_dict[key]

            if original_has_negative_number == True:
                if value >= 0:
                    value += half_original_range
                else:
                    value = half_original_range - abs(new_value)

            new_value = (value / original_range) * new_range

            if target_has_negative_number == True:
                new_value = new_value - half_new_range

            if use_int == True:
                new_data_dict[key] = int(round(new_value))
            else:
                new_data_dict[key] = new_value

        for channel_index in range(channels_number):
            for index in range(one_channel_length):
                signal = self.raw_data[channel_index][index]
                self.raw_data[channel_index][index] = new_data_dict[signal]

        return self

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

    def resize(self, x_size, y_size=None, adds=1327):
        if x_size != None:
            x_size = int(x_size)

        channels_number, one_channel_length = self.get_shape()
        if (x_size >= one_channel_length):
            return self

        ratio = one_channel_length / x_size
        part_width = int(round(ratio))
        sample_rate = int(round(self.sample_rate/ratio)) + adds

        for channel_index in range(channels_number):
            new_list = [None] * x_size
            index = 0
            index2 = 0
            #max_value = -32768
            while True:
                last_index = index - part_width
                if last_index >= 0:
                    signal_list = self.raw_data[channel_index][last_index:index]
                    signal = int(round(sum(signal_list) / part_width))
                else:
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

        signal_dict = {}
        for channel_index in range(channels_number):
            for index in range(one_channel_length):
                signal = self.raw_data[channel_index][index]
                if signal in signal_dict:
                    signal_dict[signal] += 1
                else:
                    signal_dict[signal] = 1
        signal_item_list = list(signal_dict.items())
        signal_item_list.sort(key=lambda x: -x[1])

        the_real_signal_dict = dict()
        index = 0
        for key, _ in signal_item_list:
            the_real_signal_dict[key] = str(index)
            index += 1

        text_data = "format: yingshaoxo_audio; version: 2024; help: the third part contains a dict, you have to convert it into a dict where value is what you get by using space split, index start from 0. then start from part 4, they are real data, each one represent a channel, from left ear to right ear, you have to use the dict you got before to convert those index number into real signal."
        text_data += "\n_______\n\n"
        text_data += "sample_rate," + str(sample_rate) + ",channels_number," + str(channels_number) + ",one_channel_length," + str(one_channel_length)
        text_data += "\n_______\n\n"
        for key in the_real_signal_dict.keys():
                text_data += str(key) + " "
        text_data += "\n_______\n\n"
        for channel_index in range(channels_number):
            for index in range(one_channel_length):
                signal = self.raw_data[channel_index][index]
                text_data += str(the_real_signal_dict[signal]) + " "
            text_data += "\n_______\n\n"

        text_data = text_data[:-len("\n_______\n\n")]

        file = open(file_path, "w", encoding="utf-8")
        file.write(text_data)
        file.close()

    def read_from_file(self, file_path):
        a_file = open(file_path, "r", encoding="utf-8")
        raw_text = a_file.read()
        a_file.close()

        splits = raw_text.split("\n_______\n")
        head_line = splits[0].strip()
        size_info = splits[1].strip()
        dict_text = splits[2].strip()
        the_text_data_list = [one.strip() for one in splits[3:]]

        info_splits = size_info.split(",")
        sample_rate = int(info_splits[1])
        channels_number = int(info_splits[3])
        one_channel_length = int(info_splits[5])
        self.sample_rate = sample_rate

        the_signal_dict = dict()
        for index, value in enumerate(dict_text.split(" ")):
            the_signal_dict[str(index)] = int(value)

        raw_data = []
        for channel_index, the_text_data in enumerate(the_text_data_list):
            a_list = [None] * one_channel_length
            for index, signal_index in enumerate(the_text_data.split(" ")):
                real_value = the_signal_dict[signal_index]
                a_list[index] = real_value
            raw_data.append(a_list)

        self.raw_data = raw_data


if __name__ == "__main__":
    audio = Audio()
    #audio.read_from_file("/home/yingshaoxo/Downloads/handclap2.wav.txt")
    audio = audio.read_wav_file("/home/yingshaoxo/Downloads/noise.wav")
    #channels_number, one_channel_length = audio.get_shape()
    #print(channels_number, one_channel_length)
    #audio = audio.reduce_noise_by_gate()
    audio = audio.reduce_noise_by_using_yingshaoxo_method()
    #audio = audio.reduce_noise_by_frequency()
    #audio = audio.reduce_noise_by_subtraction()
    #audio = audio.get_simplified_audio()
    #audio.save_to_file("/home/yingshaoxo/Downloads/handclap2.wav.txt")
    #audio = audio.change_sample_rate(8000)
    #audio.change_volume(0.5)
    #audio = audio.merge_to_mono()
    #a_image = audio.print()
    #a_image.save_image_to_file_path("/home/yingshaoxo/Downloads/handclap2.png")
    audio.write_wav_file("/home/yingshaoxo/Downloads/no_noise.wav")
