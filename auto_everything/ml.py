import tensorflow as tf
import tensorflow_hub as hub
import numpy as np
import csv

import io
import tempfile
import os
import hashlib
import datetime

from auto_everything.video import VideoUtils, Video
from auto_everything.disk import Store

video = Video()
videoUtils = VideoUtils()


class DataProcessor():
    """
    To implement some functionality related to data
    """

    def __init__(self):
        pass

    def get_time_series_data_from_a_list(self, the_list, sequence_length):
        """
        Get sub sequences for LSTM network.

        Parameters
        ----------
        the_list: 
        sequence_length: int
            how long you want the subsequence to be.

        Returns
        -------
        tuple
            return ([features], [labels])
        """
        assert len(the_list) >= sequence_length + 1, "len(the_list) should >= sequence_length + 1"
        array_1d = []
        array_2d = []
        array_target = []
        for element in the_list:
            array_1d.append(element)
            if len(array_1d) == sequence_length + 1:
                target = array_1d.pop()
                array_target.append(target)
                array_2d.append(array_1d.copy())
                array_1d.clear()
        return array_2d, array_target


class AudioClassifier():
    def __init__(self):
        # Load the model.
        self.model = hub.load('https://tfhub.dev/google/yamnet/1')

        class_map_path = self.model.class_map_path().numpy()
        class_map_csv_text = tf.io.read_file(class_map_path).numpy().decode('utf-8')
        class_map_csv = io.StringIO(class_map_csv_text)
        class_names = [display_name for (class_index, mid, display_name) in csv.reader(class_map_csv)]
        self.class_names = class_names[1:]  # Skip CSV header

        # Input: 3 seconds of silence as mono 16 kHz waveform samples.
        waveform = np.zeros(3 * 16000, dtype=np.float32)
        self.store = Store("AudioClassifier")

    def getWaveFormListFromVideo(self, videoPath: str, secondsForOnePart=3):
        self.temp_dir: str = tempfile.gettempdir()
        m = hashlib.sha256()
        m.update(str(datetime.datetime.now()).encode("utf-8"))
        m.update(videoPath.encode("utf-8"))
        temp_audio_file = os.path.join(self.temp_dir, m.hexdigest()[:10] + ".wav")
        videoUtils.convert_video_to_wav(videoPath, temp_audio_file)
        soundArray, SampleRate = videoUtils.getMono16khzAudioArray(temp_audio_file)
        os.remove(temp_audio_file)
        return videoUtils.convertArrayToBatchSamples(soundArray, secondsForOnePart)

    def classify(self, waveform):
        # https://tfhub.dev/google/yamnet/1
        # Run the model, check the output.
        scores, embeddings, log_mel_spectrogram = self.model(waveform)
        scores.shape.assert_is_compatible_with([None, 521])
        embeddings.shape.assert_is_compatible_with([None, 1024])
        log_mel_spectrogram.shape.assert_is_compatible_with([None, 64])
        result = self.class_names[scores.numpy().mean(axis=0).argmax()]  # Should print 'Silence'.
        # print(result)
        return result

    def label_a_video_with_intervals(self, videoPath: str, intervalLength=3):
        if self.store.get("lastVideo", "") == videoPath:
            intervalsAndLabels = store.get("intervalsAndLabels", "[]")
            if intervalsAndLabels != []:
                return intervalsAndLabels[0], intervalsAndLabels[1]
        waveformList = self.getWaveFormListFromVideo(videoPath, secondsForOnePart=intervalLength)
        labels = []
        intervals = []
        for i, waveform in enumerate(waveformList):
            a = i * intervalLength
            b = a + intervalLength
            intervals.append([a, b])
            result = self.classify(waveform)
            labels.append(result)
            # print(i, result)
        return intervals, labels


class SpeechToText():
    pass
    # https://tfhub.dev/silero/silero-stt/en/1


if __name__ == "__main__":
    from pprint import pprint

    audioClassfier = AudioClassifier()
    audioClassfier.test("/home/yingshaoxo/Videos/freaks.mp4")

    """
    data_processor = DataProcessor()
    the_list = list(range(1000))
    features, labels = data_processor.get_time_series_data_from_a_list(the_list, 10)
    """
