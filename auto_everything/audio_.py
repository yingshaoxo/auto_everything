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
