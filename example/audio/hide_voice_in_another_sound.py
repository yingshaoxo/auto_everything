from auto_everything.audio_ import Audio
from auto_everything.string_ import String

audio = Audio()
string = String()

audio_1 = audio.read_wav_file("/home/yingshaoxo/Downloads/simplified.wav").copy().get_simplified_audio()
audio_2 = audio.read_wav_file("/home/yingshaoxo/Downloads/noise_hd.wav").copy().get_simplified_audio().reduce_noise_by_subtraction(use_global_value=True)

channels_number, one_channel_length = audio_1.get_shape()
_, one_channel_length2 = audio_2.get_shape()
for channel_index in range(channels_number):
    for x in range(one_channel_length):
        if x >= one_channel_length2:
            continue
        signal_a = audio_1.raw_data[channel_index][x]
        signal_b = audio_2.raw_data[channel_index][x]
        if abs(signal_a) < 3000:
            audio_1.raw_data[channel_index][x] = signal_a + int(signal_b / 3 / 2)
        else:
            audio_1.raw_data[channel_index][x] = signal_a + int(signal_b / 3)

audio_1.write_wav_file("/home/yingshaoxo/Downloads/hidden_voice.wav")

# Another method is based on similarity, the speaker did a pre_record of what he/she wanted to say, then the system will anylyze every real time audio, if software found any sound chunk is similar to the pre_recorded voice, they will do a merge to get average audio, then play that average audio. This tech only happens when your brain get hooked or used in not really real time live show, for example, late for 1 minute. But this will not work on those people who do not know any language.
# And I secretly doudt some people use thinking stream hook to let you think a meanlingless audio has some text meaning, but they are not. You can verify it by asking another people to record that sound. If others can also hear the human voice in that audio, that means that tech was based on audio similarity. Otherwise, it is a thinking stream hook, and it only works best for you. For others, they need to do test and experiment.

"""
Just let the human voice wave frequency to match the target audio wave frequency. wave here means "signals from positive to negative" or "signals from negative to positive"
"""
