from typing import Callable, List

from auto_everything.base import Terminal
t = Terminal(debug=True)

from auto_everything.python import Python
python = Python()

import numpy as np
import time

import torch
import torchaudio
from speechbrain.pretrained import SpectralMaskEnhancement, SepformerSeparation, WaveformEnhancement

class DeepAudio:
    def __init__(self):
        # self._spectral_mask_enhancement_model = SpectralMaskEnhancement.from_hparams(
        #     source="speechbrain/metricgan-plus-voicebank",
        #     savedir="pretrained_models/metricgan-plus-voicebank",
        # )

        # self._sepformer_wham16k_enhancement_model = SepformerSeparation.from_hparams(
        #     source="speechbrain/sepformer-wham16k-enhancement", 
        #     savedir='pretrained_models/sepformer-wham16k-enhancement')
        
        self._mtl_mimic_voicebank = WaveformEnhancement.from_hparams(
            source="speechbrain/mtl-mimic-voicebank",
            savedir="pretrained_models/mtl-mimic-voicebank",
        )

    def speech_enhancement(self, 
            source_audio_path,
            target_audio_path,
            sample_rate=16000
        ):

        # # Load and add fake batch dimension
        # noisy = self._spectral_mask_enhancement_model.load_audio(
        #     source_audio_path
        # ).unsqueeze(0)
        # # Add relative length tensor
        # enhanced = self._spectral_mask_enhancement_model.enhance_batch(noisy, lengths=torch.tensor([1.]))
        # # Saving enhanced signal on disk
        # torchaudio.save(target_audio_path, enhanced.cpu(), sample_rate) # type: ignore    

        # enhanced = self._sepformer_wham16k_enhancement_model.separate_file(path=source_audio_path) 
        # torchaudio.save(target_audio_path, enhanced[:, :, 0].detach().cpu(), sample_rate) # type: ignore

        enhanced = self._mtl_mimic_voicebank.enhance_file(
            filename=source_audio_path,
            # output_filename=target_audio_path
        )
        torchaudio.save(target_audio_path, enhanced.unsqueeze(0).cpu(), sample_rate=sample_rate, channels_first=True) # type: ignore


class AudioHandler:
    def __init__(self, device_index: int, call_back_function: Callable[[np.ndarray, ], None]):
        import pyaudio
        import librosa

        self.pyaudio = pyaudio
        self.librosa = librosa

        self.FORMAT = self.pyaudio.paFloat32
        self.CHANNELS = 1
        self.RATE = 44100
        self.CHUNK = 1024 * 2
        self.p = None
        self.stream = None

        self.device_index = device_index
        self.call_back_function = call_back_function

    def __del__(self):
        self.stream.close()
        self.p.terminate()

    def start(self):
        self.p = self.pyaudio.PyAudio()
        if self.device_index is None:
            self.stream = self.p.open(format=self.FORMAT,
                                      channels=self.CHANNELS,
                                      rate=self.RATE,
                                      input=True,
                                      output=False,
                                      stream_callback=self.callback,
                                      frames_per_buffer=self.CHUNK,
                                      )
        else:
            self.stream = self.p.open(format=self.FORMAT,
                                      channels=self.CHANNELS,
                                      rate=self.RATE,
                                      input=True,
                                      output=False,
                                      stream_callback=self.callback,
                                      frames_per_buffer=self.CHUNK,
                                      input_device_index=self.device_index,
                                      # print(self.sounddevice.query_devices())
                                      )

    def stop(self):
        self.stream.close()
        self.p.terminate()

    def callback(self, in_data, frame_count, time_info, flag):
        numpy_array = np.frombuffer(in_data, dtype=np.float32)

        if python.check_if_a_variable_is_a_function(self.call_back_function):
            self.call_back_function(numpy_array)

        # data = librosa.amplitude_to_db(numpy_array)
        # value = tf.math.reduce_mean(data)
        # print(value.numpy())

        return None, self.pyaudio.paContinue

    def mainloop(self):
        while self.stream.is_active():
            time.sleep(2.0)


class AudioMonitor:
    def __init__(self):
        try:
            import sounddevice
            import pyaudio
            self.sounddevice = sounddevice
            self.pyaudio = pyaudio
            self.AudioHandler = AudioHandler
        except Exception as e:
            print("python3 -m pip install sounddevice")
            print("python3 -m pip install pyaudio")
            raise e


class AudioAnalyzer:
    def __init__(self):
        try: 
            import pydub
            self.pydub = pydub
        except Exception as e:
            print("python3 -m pip install pydub")
            raise e
    
    def get_audio_loudness_per_x_millisecond(self, audio_file_path: str, x: int) -> List[float]:
        theWholeAudio = self.pydub.AudioSegment.from_file(audio_file_path)

        segmentsList = []
        totalLength = len(theWholeAudio)
        i = 0
        chunkLength = x
        while i < totalLength:
            segmentsList.append(theWholeAudio[i:i+chunkLength])
            i += chunkLength

        loudnessList = []
        for segment in segmentsList:
            loudnessList.append(segment.dBFS)
        return loudnessList


# if __name__ == "__main__":
#     audio = AudioHandler()
#     audio.start()  # open the the stream
#     audio.mainloop()  # main operations with librosa
#     audio.stop()
