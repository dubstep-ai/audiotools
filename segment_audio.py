import os

#from pydub import AudioSegment
import numpy as np
from scipy.io import wavfile
from plotly.offline import init_notebook_mode
import plotly.graph_objs as go
import plotly


thresholdHOLD_MULTIPLIER = 0.00004
SEGMENT_SIZE_IN_SECONDS = 0.2
DATA_PATH='/users/arvind/Downloads/Modi Audio/wavs/'

for f in os.listdir(DATA_PATH):
    if not f.endswith('3.wav'):
        continue
    print(f)

    # read WAV file using scipy.io.wavfile
    fs_wav, data_wav = wavfile.read(DATA_PATH + f)

    # read MP3 file using pudub
    #audiofile = AudioSegment.from_file("data/music_8k.mp3")
    #data_mp3 = np.array(audiofile.get_array_of_samples())
    #fs_mp3 = audiofile.frame_rate

    #print('Sq Error Between mp3 and wav data = {}'.
    #      format(((data_mp3 - data_wav)**2).sum()))
    print('Signal Duration = {} seconds'.
          format(data_wav.shape[0] / fs_wav))

    time_wav = np.arange(0, len(data_wav)) / fs_wav

    # Normalization
    data_wav_norm = data_wav / (2**15)
    time_wav = np.arange(0, len(data_wav)) / fs_wav

    # Fix-sized segmentation (breaks a signal into non-overlapping segments)
    segment_size = int(SEGMENT_SIZE_IN_SECONDS * fs_wav)  # segment size in samples

    # Break signal into list of segments in a single-line Python code
    segments = np.array([data_wav_norm[x:x + segment_size] for x in
                         np.arange(0, len(data_wav_norm), segment_size)])

    # Remove pauses using an energy thresholdhold = 50% of the median energy:
    energies = [(s**2).sum() / len(s) for s in segments]
    # (attention: integer overflow would occure without normalization here!)
    threshold = thresholdHOLD_MULTIPLIER * np.median(energies)
    index_of_silent_segments = (np.where(energies < threshold)[0])
    # get segments that have energies higher than a the thresholdhold:
    silence_segments = segments[index_of_silent_segments]

    print(threshold)
    print(index_of_silent_segments)

    # Write out the concatenated silence segments for manual verification
    silence_signal = np.concatenate(silence_segments)
    wavfile.write("data/silence.wav", fs_wav, silence_signal)

    # now find the silences where we wanna split
    prev = 0
    for splitter in index_of_silent_segments:
        if ((splitter - prev) * SEGMENT_SIZE_IN_SECONDS > 7):
            wavfile.write("data/" + str(prev) + ".wav", fs_wav, np.concatenate(segments[prev:splitter]))
            print(prev, splitter) # write out form prev till right before this segment
            prev = splitter
