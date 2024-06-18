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


"""
Then what is low base sound, what is high frequency sound? The bass is low frequency sound, the high pitch piano sound is high frequency sound, the man voice is low frequency sound, the woman voice is high frequency sound.

What is high frequency sound? what is low frequency sound? Suppose you have 1 second sound, a signal appears a lot of times, it is high frequency sound.

High frequency is like: _|_|_|_|_|_, low frequency is like: ___|___|____, you see, for same period of time, low frequency has less signal, high frequency has more signals.

It seems like we distingush voice by frequency than pure signal volume. This makes audio process hard.

But I can guess, human or animal uses a counting dict for signals, in one second, same volume signal will become a counting number, for next second, if that sound do not exists anymore, we will delete that signal from our counting dict. So that we can do frequency analyze in real time for what we hear. The counting data is what we called "sound fingerprint".
"""

"""
But overall, audio is a low efficiency information saving format. Because for one second, it has 8000 integers, which takes 8KB. But if you use pure ASCII character to save information, 8KB could save 8000 characters. Can you speak 8000 character per second? Audio is 8000 times low efficiency than pure text. Because it uses "frequency modulation (FM)", which scales up pure data about 8000 times, generate 7999 garbage information.
"""


class Audio():
    """
    author: yingshaoxo

    normally, wav file value is in range of (-32768, 32768), but you can convert it into (0, 1023) to let micropython to use two analog pin to drive a speaker to play sound.
    the convertion function is self.range_map(-32767, 32767, 0, 1023, loudness_match=True)
    """
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

    def change_sample_rate(self, sample_rate, speed_mode=False, accurate_mode=False):
        """
        sample_rate: int
            can be 8000, 16000, and so on
        speed_mode: bool
            if you set it to true, the process speed would be quicker, but audio quality will be lower
        """
        # we can scale it up first, then scale it down
        old_sample_rate = self.sample_rate
        channels_number, one_channel_length = self.get_shape()
        if (sample_rate >= old_sample_rate):
            return self

        ratio = old_sample_rate / sample_rate

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
                    if speed_mode == True:
                        middle_index = last_index + int((round(index) - last_index) / 2)
                        signal = self.raw_data[channel_index][middle_index]
                    else:
                        if accurate_mode == False:
                            signal = int(round(sum(signal_list) / part_width))
                        else:
                            common_signals_list_in_horizontal = []
                            sub_window_dict = dict()
                            for signal in signal_list:
                                if signal in sub_window_dict:
                                    sub_window_dict[signal] += 1
                                else:
                                    sub_window_dict[signal] = 1
                            sub_window_signal_frequency_dict_items = list(sub_window_dict.items())
                            sub_window_signal_frequency_dict_items.sort(key=lambda one: -one[1])
                            signal = sub_window_signal_frequency_dict_items[0][0]
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
            the_average_value = sum(a_list)/channels_number
            new_data[index] = int(round(the_average_value))

        a_audio.raw_data = [new_data]

        return a_audio

    def to_stereo(self):
        a_audio = self.copy()
        channels_number, one_channel_length = a_audio.get_shape()

        if channels_number == 1:
            a_audio.raw_data = [a_audio.raw_data[0], a_audio.raw_data[0].copy()]

        return a_audio

    def change_volume(self, scale=1.0):
        channels_number, one_channel_length = self.get_shape()
        for channel_index in range(channels_number):
            for x in range(one_channel_length):
                signal = self.raw_data[channel_index][x]
                self.raw_data[channel_index][x] = int(round(self.raw_data[channel_index][x] * scale))
        return self

    def get_simplified_audio(self, sample_rate=8000, extreme=False, accurate_mode=False):
        audio = self.copy()
        channels_number, one_channel_length = audio.get_shape()
        audio = audio.change_sample_rate(sample_rate, accurate_mode=accurate_mode)
        audio = audio.merge_to_mono()
        audio = audio.change_volume(1.2)
        if extreme == True:
            audio = audio.range_map(-32767, 32767, 0, 1024, loudness_match=False)
        return audio

    def get_extreme_simplified_audio(self, sample_rate=8000, max_signal_value=9, raw=False):
        """
        If the max_signal_value is less than 128, use ascii char to represent 3 numbers is better than directly use 3 numbers in storage. It saves 3 times of storage.
        """
        audio = self.copy()
        channels_number, one_channel_length = audio.get_shape()
        audio = audio.change_sample_rate(sample_rate)
        audio = audio.merge_to_mono()
        audio = audio.range_map(-32767, 32767, -max_signal_value, max_signal_value, loudness_match=True)
        if raw == False:
            audio = audio.range_map(-max_signal_value, max_signal_value, -32767, 32767, loudness_match=False)
        return audio

    def get_simplified_audio_by_using_balance_sample(self, sample_rate=8000, max_signal_number=30):
        """
        Two balance method is a method that considers horizontal and vertical level of data sampling.
        It first sample data sub part evenly by using step number to get partly most frequent data.
        Then at global level, it do a frequent sort again to get most frequent data, so those small data type can represent the whole data. So at the beginning, the data type is 32700, not it becomes 'max_signal_number' types, which is 30. The compression level is 1000.
        Why this method not working perfect in mutiple_track_mixed audio? because those data does not belong to one track, the frequency detection may not work well on it. But if you do process for each track, then merge all of them after process, it would be perfect.
        Author: yingshaoxo
        """
        audio = self.copy()
        channels_number, one_channel_length = audio.get_shape()
        audio = audio.change_sample_rate(sample_rate, accurate_mode=True)
        audio = audio.merge_to_mono()

        step_number = int((500/8000) * sample_rate)

        common_signals_list_in_horizontal = []
        channels_number, one_channel_length = audio.get_shape()
        for channel_index in range(channels_number):
            for x in range(0, one_channel_length, step_number):
                #signal = audio.raw_data[channel_index][x]
                #common_signals_list_in_horizontal.append(signal)
                sub_window_dict = dict()
                for signal in audio.raw_data[channel_index][x: x+step_number]:
                    if signal in sub_window_dict:
                        sub_window_dict[signal] += 1
                    else:
                        sub_window_dict[signal] = 1
                sub_window_signal_frequency_dict_items = list(sub_window_dict.items())
                sub_window_signal_frequency_dict_items.sort(key=lambda one: -one[1]) #positive first, big first, then smaller number
                # we need to get a most frequent positive one and negative one
                sign_flag = None
                for target_signal_item in sub_window_signal_frequency_dict_items:
                    target_signal = target_signal_item[0]
                    if target_signal == 0:
                        common_signals_list_in_horizontal.append(target_signal)
                        break
                    if sign_flag == None:
                        if target_signal > 0:
                            sign_flag = True
                        elif target_signal < 0:
                            sign_flag = False
                        common_signals_list_in_horizontal.append(target_signal)
                    else:
                        if sign_flag == True:
                            if target_signal > 0:
                                continue
                        else:
                            if target_signal < 0:
                                continue
                        common_signals_list_in_horizontal.append(target_signal)
                        break

        signal_frequency_dict = {}
        for signal in common_signals_list_in_horizontal:
            if signal in signal_frequency_dict:
                signal_frequency_dict[signal] += 1
            else:
                signal_frequency_dict[signal] = 1
        signal_frequency_dict_items = list(signal_frequency_dict.items())
        signal_frequency_dict_items.sort(key=lambda one: one[1]) #negative first, small first, then bigger number

        signal_frequency_dict_items = signal_frequency_dict_items[-max_signal_number:]
        common_signals = [one[0] for one in signal_frequency_dict_items]

        channels_number, one_channel_length = audio.get_shape()
        cache_dict = {}
        for channel_index in range(channels_number):
            for x in range(0, one_channel_length):
                signal = audio.raw_data[channel_index][x]
                target_signal = signal
                if signal in cache_dict:
                    target_signal = cache_dict[signal]
                else:
                    minimum_distance = 999999
                    for safe_signal in common_signals:
                        distance = abs(safe_signal - signal)
                        if distance < minimum_distance:
                            minimum_distance = distance
                            target_signal = safe_signal
                    cache_dict[signal] = target_signal
                audio.raw_data[channel_index][x] = target_signal

        return audio

    def range_map(self, original_min_value, original_max_value, min_value, max_value, use_int=True, loudness_match=True):
        """
        original_min_value, original_max_value, min_value, max_value: int
            -32767, 32767, 0, 1023 for micropython
            -32767, 32767, 0, 254 for arduino
        use_int: bool
            will make sure all result is integer
        loudness_match: bool
            will make sure the sound has a volume you can hear

        By default wav audio has negative numbers. It is in range of (-32767, 32767)

        You can use this function to do convertion between (0, 3.3) and (0, 5) and (-32767, 32767) and (0, 1024) and (0, 255)

        If you want float number, you have to set use_int==False
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
        real_original_max_value = -999999
        real_original_min_value = 999999
        channels_number, one_channel_length = self.get_shape()
        for channel_index in range(channels_number):
            for index in range(one_channel_length):
                signal = self.raw_data[channel_index][index]
                new_data_dict[signal] = signal

                if signal > real_original_max_value:
                    real_original_max_value = signal
                if signal < real_original_min_value:
                    real_original_min_value = signal

        if loudness_match == True:
            original_range = real_original_max_value - real_original_min_value
        else:
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
                    value = half_original_range - abs(value)

            new_value = (value / original_range) * new_range

            if target_has_negative_number == True:
                new_value = new_value - half_new_range
            else:
                new_value = abs(new_value) # may have a bug in here, there should not have a negative number

            if use_int == True:
                new_data_dict[key] = int(new_value)
            else:
                new_data_dict[key] = new_value

        for channel_index in range(channels_number):
            for index in range(one_channel_length):
                signal = self.raw_data[channel_index][index]
                new_signal = new_data_dict[signal]
                if new_signal > max_value:
                    new_signal = max_value
                elif new_signal < min_value:
                    new_signal = min_value
                self.raw_data[channel_index][index] = new_signal

        return self

    def resize(self, new_audio_length_in_seconds, keep_pitch=False):
        """
        keep_pitch: bool
            Default False
            How to change length without change pitch? for example, make the length twice:
                old_signal: _|_|_\_\
                new_signal: _|_|_|_|_\_\_\_\
            What I did is to repeat every 2 signal twice, then use mean value to connect them to make the audio line smooth.

        This function works better in single channel audio, for example, only have human voice, or only have piano sound.
        This function can get improved by split the whole audio to 20ms parts, only repeat those part that already repeated 2+ times.
        I think you could split the audio to multiple tracks by frequency, then do process for each track, because that will reduce collision.
        """
        a_audio = self.copy()
        new_audio_data_length = round(a_audio.sample_rate * new_audio_length_in_seconds)

        if keep_pitch == False:
            channels_number, one_channel_length = a_audio.get_shape()
            for channel_index in range(channels_number):
                old_audio_data = a_audio.raw_data[channel_index]
                old_audio_data_length = len(old_audio_data)
                new_audio_data = [None] * new_audio_data_length
                if new_audio_data_length == old_audio_data_length:
                    continue
                elif new_audio_data_length < old_audio_data_length:
                    kernel = old_audio_data_length / new_audio_data_length
                    for x in range(new_audio_data_length):
                        old_x = x
                        x = int(x*kernel)
                        if x >= old_audio_data_length:
                            x = old_audio_data_length - 1
                        new_audio_data[old_x] = old_audio_data[x]
                    a_audio.raw_data[channel_index] = new_audio_data
                elif new_audio_data_length > old_audio_data_length:
                    kernel = new_audio_data_length / old_audio_data_length
                    for x in range(new_audio_data_length):
                        old_x = x
                        x = int(x/kernel)
                        if x >= old_audio_data_length:
                            x = old_audio_data_length - 1
                        new_audio_data[old_x] = old_audio_data[x]
                    a_audio.raw_data[channel_index] = new_audio_data
            return a_audio
        else:
            channels_number, one_channel_length = a_audio.get_shape()
            for channel_index in range(channels_number):
                old_audio_data = a_audio.raw_data[channel_index]
                old_audio_data_length = len(old_audio_data)
                kernel = int(a_audio.sample_rate * 0.02) #160ms
                if new_audio_data_length == old_audio_data_length:
                    continue
                elif new_audio_data_length < old_audio_data_length:
                    old_audio_part_length = old_audio_data_length / kernel
                    new_audio_part_length = new_audio_data_length / kernel
                    scale_ratio = old_audio_part_length / new_audio_part_length
                    new_data = []
                    for i in range(int(new_audio_part_length)):
                        old_part_index = i * scale_ratio
                        old_audio_index = int(old_part_index * kernel)
                        old_audio_part = old_audio_data[old_audio_index: old_audio_index+kernel]
                        new_data += old_audio_part
                    if len(new_data) < new_audio_data_length:
                        new_data += [0] * (new_audio_data_length-len(new_data))
                    new_data = new_data[:new_audio_data_length]
                    a_audio.raw_data[channel_index] = new_data
                elif new_audio_data_length > old_audio_data_length:
                    new_length_ratio = (new_audio_data_length / old_audio_data_length)
                    new_length_ratio_int = int(new_length_ratio)+1
                    real_part_length = round(kernel*new_length_ratio)
                    new_data = []
                    x = 0
                    index = 0
                    join_point_index_list = []
                    while True:
                        part = old_audio_data[x: x+kernel]
                        mean_value = round((part[0] + part[-1])/2)
                        part[0] = mean_value
                        part[-1] = mean_value
                        part_data = (part*new_length_ratio_int)[:real_part_length]
                        index += len(part_data)
                        new_data += part_data
                        x += kernel
                        if x >= old_audio_data_length:
                            break
                        join_point_index_list.append(index)

                    if len(new_data) < new_audio_data_length:
                        new_data += [0] * (new_audio_data_length-len(new_data))
                    new_data = new_data[:new_audio_data_length]

                    #smooth_kernel = int(kernel/16)
                    #for index in join_point_index_list:
                    #    if index >= new_audio_data_length:
                    #        break
                    #    start_index = index-smooth_kernel
                    #    end_index = index+smooth_kernel
                    #    for smooth_index in range(start_index, end_index):
                    #        if smooth_index < 0 or smooth_index >= new_audio_data_length:
                    #            continue
                    #        diff = abs(smooth_index - index)
                    #        decrease_ratio = diff/smooth_kernel
                    #        new_data[smooth_index] = round(new_data[smooth_index] * decrease_ratio)

                    a_audio.raw_data[channel_index] = new_data
            return a_audio

    def split_audio_by_frequency(self, audio_numbers=3, sub_list_length_in_second=0.005, just_return_frequency_info_dict=False, raw_data=False):
        """
        Audio frequency is not all about single signal value or volume, is not about signal index. It is about the how many closed wave in one second. In other words, how many continues_positive_signals and continues_negative_signals wave in one second. Or how many shake in one second. Here the 'shake' means magnet move up and down for once.
        High frequency wave create high pitch, low frequency wave create low pitch, we only count no silence signal wave per 0.01*second.

        This function will return you 3 audio: [low_frequency_audio, middle_frequency_audio, high_frequency_audio]
        """
        """
        Unsure:
            It seems like frequency spliting only need to use a pre_calcalated index_dict where frequency HZ is the key, index list is the value. The dict is different for different sample rate, for example 8000, 32000.
            xHz means 1 second has x closed wave.
            return {
                "20Hz": [],
                "63Hz": [],
                "200Hz": [],
                "630Hz": [],
                "2000Hz": [],
                "6300Hz": [],
                "20000Hz": [],
            }
        """
        a_audio_backup = self.copy().get_simplified_audio(sample_rate=8000)
        a_audio_backup = a_audio_backup.range_map(-32767, 32767, -32767, 32767, loudness_match=True)
        a_audio = a_audio_backup.copy().range_map(-32767, 32767, -1024, 1024, use_int=True, loudness_match=True)
        # get global max value of no silence signal number per 0.01 second
        standard_signal_number_per_part = int(sub_list_length_in_second * a_audio_backup.sample_rate)
        #standard_signal_number_per_part = int(0.01 * a_audio_backup.sample_rate)
        #standard_signal_number_per_part = int(0.1 * a_audio_backup.sample_rate)
        #standard_signal_number_per_part = int(0.5 * a_audio_backup.sample_rate)
        part_frequency_dict = dict()
        max_frequency = 0
        channels_number, one_channel_length = a_audio_backup.get_shape()
        for channel_index in range(channels_number):
            part_number = int(one_channel_length/standard_signal_number_per_part)
            for index in range(part_number):
                start_index = index * standard_signal_number_per_part
                end_index = start_index + standard_signal_number_per_part
                part_signal_list = a_audio.raw_data[channel_index][start_index: end_index]
                counting = 0
                index1 = 0
                while True:
                    signal = part_signal_list[index1]
                    if signal != 0:
                        index2 = index1+1
                        if index2 >= len(part_signal_list):
                            break
                        while True:
                            signal2 = part_signal_list[index2]
                            if signal > 0 and signal2 <= 0:
                                counting += 1
                                index1 = index2 - 1
                                break
                            if signal < 0 and signal2 >= 0:
                                counting += 1
                                index1 = index2 - 1
                                break
                            index2 += 1
                            if index2 >= len(part_signal_list):
                                index1 = index2
                                break
                    index1 += 1
                    if index1 >= len(part_signal_list):
                        break
                frequency = int(counting / 2)
                part_frequency_dict[index] = frequency
                if frequency > max_frequency:
                    max_frequency = frequency
        if raw_data == False:
            for part_index, frequency in part_frequency_dict.items():
                part_frequency_dict[part_index] = frequency / max_frequency

        if just_return_frequency_info_dict == True:
            return part_frequency_dict

        temp_audio = Audio()
        temp_audio.sample_rate = a_audio_backup.sample_rate
        temp_audio.raw_data = [[0] * one_channel_length]
        split_step = 1/audio_numbers
        audio_list = []
        for i in range(audio_numbers):
            audio_list.append(temp_audio.copy())
        for channel_index in range(channels_number):
            part_number = int(one_channel_length/standard_signal_number_per_part)
            for index in range(part_number):
                start_index = index * standard_signal_number_per_part
                end_index = start_index + standard_signal_number_per_part
                part_signal_list = a_audio_backup.raw_data[channel_index][start_index: end_index]
                frequency = part_frequency_dict[index]
                the_index = int(frequency/split_step)
                if the_index >= audio_numbers:
                    the_index = audio_numbers - 1
                audio_list[the_index].raw_data[0][start_index: end_index] = part_signal_list[:]

        return audio_list

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

    def reduce_noise_by_subtraction(self, noise_audio=None, threshold=None, use_first_x_second_noise=0.048, ratio=6, use_global_value=False, global_value=0.1):
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
        if use_global_value == True:
            threshold = round(max([abs(one) for one in self.raw_data[0]]) * global_value)

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

    def reduce_noise_by_gate(self, threshold=None, noise_audio=None, use_first_x_second_noise=0.048, kernel=105, top_noise_ratio=0.001, less_broken=True, ratio=3):
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
            threshold = sum([abs(one) for one in noise_audio.raw_data[0]]) / len(noise_audio.raw_data[0]) * ratio

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

    def reduce_noise_by_using_yingshaoxo_method(self, threshold=None, noise_audio=None, use_first_x_second_noise=0.048, kernel=100, less_broken=True, ratio=2.0, smooth=False):
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
            threshold = sum([abs(one) for one in noise_audio.raw_data[0]]) / len(noise_audio.raw_data[0]) * ratio

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
            new_audio = self.copy()
            new_audio.reduce_noise_by_gate()
            self.change_volume(0.1)
            a_audio.raw_data = a_audio.raw_data + new_audio.raw_data + self.raw_data
            self.raw_data = a_audio.merge_to_mono().raw_data
            self.change_volume(1.5)
            self.volume_db_limiter(-11, 0.7)
            if smooth == True:
                self.smooth_audio(kernel=1)
        else:
            self.raw_data = a_audio.raw_data

        return self

    def reduce_noise(self):
        """
        Two place to improve:
        1. find a way to reduce noise in voice just like audacity noise supression algorithm did, they use FFT
        2. find a better way to smooth audio
        """
        a_audio = self.copy()

        a_audio_1 = a_audio.copy().reduce_noise_by_using_yingshaoxo_method(less_broken=True, smooth=True)

        use_first_x_second_noise=0.048
        noise_numbers = round(a_audio.sample_rate*use_first_x_second_noise)
        noise_audio = Audio()
        noise_audio.raw_data = [a_audio.raw_data[0][:noise_numbers]]

        a_audio = a_audio.reduce_noise_by_subtraction(ratio=3)
        a_audio = a_audio.reduce_noise_by_using_yingshaoxo_method(noise_audio=noise_audio, less_broken=False, ratio=1.5, kernel=50)

        a_audio = a_audio.reduce_noise_by_counting(0.7)
        a_audio = a_audio.smooth_audio(kernel=1)

        a_audio.raw_data = a_audio.raw_data + a_audio_1.raw_data
        a_audio = a_audio.merge_to_mono()

        self = a_audio
        return self

    def smooth_audio(self, kernel=3):
        a_audio = self.copy()

        kernel = int(kernel)
        channels_number, one_channel_length = a_audio.get_shape()
        for channel_index in range(channels_number):
            for index in range(one_channel_length):
                #signal = a_audio.raw_data[channel_index][index]
                start_index = index - 1
                end_index = index + kernel
                if start_index <= 0:
                    start_index = 0
                if end_index >= one_channel_length:
                    end_index = one_channel_length
                signal_range = a_audio.raw_data[channel_index][start_index: end_index]
                average_value = round(sum(signal_range)/len(signal_range))
                a_audio.raw_data[channel_index][index] = average_value

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
        a_audio._fake_resize(x_size=int(width/line_length))
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

    def to_hash(self, seconds=0.5, hash_length=64):
        """
        For music, we use midi, which means a list of numbers between 0 and 128
        For voice, we use voice parts, which means a list of voice without silence inside. for example, "How are you" voice will get seperated into ["how", "are", "you"], and for each word of sound, we will make it has same length by stretching the audio part. And for each character part, we have to do loudness_match.
        The core is "audio strench" and "seperate audio by silence". And if you to have a more accurate one, you should have a dict where it has all audio for your language character. (Just think about how many sound or voice you hear before you can talk. It is about 5 years of length of audio.)
        Or if you busy, just use noise gate method to get volume level per 0.025 second. and for chinese, you have to also detect 4 tones in pinyin.

        Then, let me talk about statistic_based machine learning algorithm:
            If you have 10 audio that talks about "How are you", you can know that each audio was composed by 3 words.
            So you do a evenly split for each audio, let's say, split each one by 3. So that for each word, for example, "How", you can get 10 audio about "how".
            You simply add all 10 "how" audio togather, so you can get a general audio that represents the "how" word.
            You do this for all 500 general english words. In the end, if you have a new audio, you search your magic general audio word database. so that you can get a list of words to represent that new audio.
            For somehow, you already implemented a human voice to text function.

        Let me talk about the difference between deep learning and general machine learning:
            1. deep learning simply remembers all data, so that it could be very accurate. But it takes disk storage space.
            2. general machine learning uses hard coding algorithm or statistic mean value to solve a problem, it only solves standard question. It can be accurate only if the test question is a standard pure question without noise. But in real world, people sometimes talks in a way human themselves can't understand, how do you expect a mean value could cover that extream case?

        And a super quick audio to text application could be:
            1. record a audio, get per 0.025 second sound signal as a list after sound match for each silence interval. A 5 second audio will only have a 200 integer list as audio fingerprint.
            2. since you have a dict in server, where key is audio fingerprint, value is text, so the search speed is very quick. For the hash finding process, it first find key[0:200], if not found, it will find key[0:199], until it found a text, then find another text from remain audio signals. the maxmuim time wasting would be 200 hash looking time, which is not an expensive operation for modern computer.
            3. for wave audio, it is special, mean value will not work since they got negative value. So for each time point, you have get a max value and min value, treat two as one string.

        Sometimes I think, it is not deep learning changed the world, it is hash table or dict changed the world.
        """
        a_audio = self.copy()

        a_audio = a_audio.resize(seconds)
        a_audio = a_audio.change_sample_rate(20)
        a_audio = a_audio.reduce_noise_by_subtraction(use_global_value=True)
        a_audio = a_audio.merge_to_mono()
        a_audio = a_audio.range_map(-32767, 32767, -9, 9, use_int=True, loudness_match=True)

        # remove head and tail silence
        try:
            start_index = 0
            for signal in a_audio.raw_data[0]:
                if signal != 0:
                    start_index += 1
                    break
            end_index = len(a_audio.raw_data[0])
            for signal in reversed(a_audio.raw_data[0]):
                if signal != 0:
                    end_index -= 1
                    break
            a_audio.raw_data[0] = a_audio.raw_data[0][start_index: end_index]
            a_audio = a_audio.resize(seconds)
        except Exception as e:
            pass

        # volume
        text_data = "".join([str("{:01d}".format(abs(one))) for one in a_audio.raw_data[0]])

        # relative frequency
        frequency_dict = self.copy().split_audio_by_frequency(audio_numbers=3, just_return_frequency_info_dict=True, sub_list_length_in_second=0.02)
        frequency_text = "".join(["{:01d}".format(int(one*9)) for one in frequency_dict.values()])
        text_data += frequency_text

        # global frequency in [0, 4000] HZ
        frequency_dict = self.copy().split_audio_by_frequency(audio_numbers=3, just_return_frequency_info_dict=True, sub_list_length_in_second=1, raw_data=True)
        frequency_text = "".join(["{:01d}".format(min(int(one / 4000 * 10), 9)) for one in frequency_dict.values()])
        text_data += frequency_text

        old_text_length = len(text_data)
        if old_text_length > hash_length:
            kernel = old_text_length / hash_length
            new_text = ""
            for i in range(hash_length):
                i = int(i * kernel)
                if i >= old_text_length:
                    i = old_text_length-1
                new_text += text_data[i]
            return new_text
        else:
            kernel = hash_length / old_text_length
            new_text = ""
            for i in range(hash_length):
                i = int(i / kernel)
                if i >= old_text_length:
                    i = old_text_length-1
                new_text += text_data[i]
            return new_text

    def _fake_resize(self, x_size, y_size=None, adds=1327):
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
        number_of_frames = wav_object.getnframes() * int_width * channels
        signal_list = wav_object.readframes(number_of_frames)

        raw_data = []
        one_channel_number = int(number_of_frames/channels/int_width)
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

    def write_wav_file(self, wav_file_path, sample_width=2):
        import struct
        sample_rate = self.sample_rate
        channels_number, one_channel_length = self.get_shape()

        wav_object = self.wave_module.open(wav_file_path, 'w')
        wav_object.setnchannels(channels_number)
        wav_object.setsampwidth(sample_width) # can be 1 for small value
        wav_object.setframerate(sample_rate)

        for index in range(one_channel_length):
            for channel_index in range(channels_number):
                value = self.raw_data[channel_index][index]
                value = max(min(value, 32767), -32767)
                data = struct.pack('<h', value)
                wav_object.writeframesraw(data)

        wav_object.close()

    def save_to_file(self, file_path, extreme_mode=True):
        """
        For yingshaoxo audio text format, there could have more compression inside. By introducing a repeat symbol. For example, "1_9" means repeat 1 for 9 times. "6_5" means repeat 6 for 5 times.
        """
        if file_path.lower().endswith(".wav"):
            self.write_wav_file(file_path)
            return self

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

        text_data = "format: yingshaoxo_audio; version: 2024; help: the second part has sample_rate data. the third part contains a dict, you have to convert it into a dict where value is what you get by using space split, the key is the element index start from 0. then start from part 4, they are real data, each one represent a channel, from left ear to right ear, you have to use the dict you got before to convert those index number into real signal list. If you meet '1_9', it means repeat 1 for 9 times. '6_5' means repeat 6 for 5 times."
        text_data += "\n_______\n\n"
        text_data += "sample_rate," + str(sample_rate) + ",channels_number," + str(channels_number) + ",one_channel_length," + str(one_channel_length)
        text_data += "\n_______\n\n"
        for key in the_real_signal_dict.keys():
                text_data += str(key) + " "
        text_data += "\n_______\n\n"

        if extreme_mode == False:
            for channel_index in range(channels_number):
                for index in range(one_channel_length):
                    signal = self.raw_data[channel_index][index]
                    text_data += str(the_real_signal_dict[signal]) + " "
                text_data += "\n_______\n\n"
            text_data = text_data[:-len("\n_______\n\n")]
        else:
            for channel_index in range(channels_number):
                index = 0
                while True:
                    signal = self.raw_data[channel_index][index]
                    repeat_counting = 0
                    for temp_signal_index in range(index, one_channel_length):
                        temp_signal = self.raw_data[channel_index][temp_signal_index]
                        if temp_signal == signal:
                            repeat_counting += 1
                        else:
                            break
                    if repeat_counting >= 2:
                        text_data += str(the_real_signal_dict[signal]) + "_" + str(repeat_counting) + " "
                        index += repeat_counting - 1
                    else:
                        text_data += str(the_real_signal_dict[signal]) + " "
                    index += 1
                    if index >= one_channel_length:
                        break
                text_data += "\n_______\n\n"
            text_data = text_data[:-len("\n_______\n\n")]

        file = open(file_path, "w", encoding="utf-8")
        file.write(text_data)
        file.close()

    def read_from_file(self, file_path):
        if file_path.lower().endswith(".wav"):
            self.read_wav_file(file_path)
            return self

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

        if "_" not in the_text_data_list[0]:
            # not extreme mode
            raw_data = []
            for channel_index, the_text_data in enumerate(the_text_data_list):
                a_list = [None] * one_channel_length
                for index, signal_index in enumerate(the_text_data.split(" ")):
                    real_value = the_signal_dict[signal_index]
                    a_list[index] = real_value
                raw_data.append(a_list)
        else:
            # extreme mode
            raw_data = []
            for channel_index, the_text_data in enumerate(the_text_data_list):
                a_list = [None] * one_channel_length
                index = 0
                for _, signal_index in enumerate(the_text_data.split(" ")):
                    if "_" in signal_index:
                        real_signal_index, repeat_time = signal_index.split("_")
                        real_value = the_signal_dict[real_signal_index]
                        for one in range(int(repeat_time)):
                            a_list[index] = real_value
                            index += 1
                    else:
                        real_value = the_signal_dict[signal_index]
                        a_list[index] = real_value
                        index += 1
                raw_data.append(a_list)

        self.raw_data = raw_data


if __name__ == "__main__":
    audio = Audio()
    #audio.read_from_file("/home/yingshaoxo/Downloads/handclap2.wav.txt")
    audio = audio.read_wav_file("/home/yingshaoxo/Downloads/noise.wav")
    #audio = audio.reduce_noise()
    audio = audio.reduce_noise_by_subtraction(use_global_value=True)
    #audio = audio.reduce_noise_by_using_yingshaoxo_method(less_broken=True)
    #audio = audio.smooth_audio(kernel=1)
    #audio = audio.range_map(-32767, 32767, 0, 1023, loudness_match=True)
    #channels_number, one_channel_length = audio.get_shape()
    #print(channels_number, one_channel_length)
    #audio = audio.reduce_noise_by_gate()
    #audio = audio.reduce_noise_by_frequency()
    #audio = audio.reduce_noise_by_subtraction()
    #audio = audio.get_simplified_audio(sample_rate=4000)
    #audio = audio.to_stereo()
    #audio.save_to_file("/home/yingshaoxo/Downloads/song_small.wav.txt")
    #audio = audio.change_sample_rate(8000)
    #audio.change_volume(0.5)
    #audio = audio.merge_to_mono()
    #a_image = audio.print()
    #a_image.save_image_to_file_path("/home/yingshaoxo/Downloads/handclap2.png")
    audio.write_wav_file("/home/yingshaoxo/Downloads/no_noise.wav")
