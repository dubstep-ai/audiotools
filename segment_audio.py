import os

#from pydub import AudioSegment
import numpy as np
from scipy.io import wavfile

THRESHOLD_MULTIPLIER = 0.3
SEGMENT_SIZE_IN_SECONDS = 0.2
DATA_PATH='/Users/arvindsuresh/projects/ai/datasets/51CenterChannel/'
OUTPUT_PATH='/Users/arvindsuresh/projects/ai/datasets/splits/CenterChannel100s/'


def get_best_silent_segments(indices):
    for x in indices:
        y = x
        while ((y+1) in indices) == True:
            y += 1
        
        # special casing sequence of 2 silent segments. Remove x, keep y
        if (y == x+1):
            indices = indices[indices != x]
            break

        # keep the middle silent segment, remove the ones before and after
        counter = 0
        while (y > x):
            indices = indices[indices != x]
            indices = indices[indices != y]
            x += 1
            y -= 1
            counter += 2

    return indices

for f in os.listdir(DATA_PATH):
    sample_counter = 0
    if not f.startswith('Stranger'):
        continue
    print(f)

    # read WAV file using scipy.io.wavfile
    fs_wav, data_wav = wavfile.read(DATA_PATH + f)

    # read MP3 file using pudub
    #audiofile = AudioSegment.from_file("data/k.mp3")
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

    # Remove pauses using an energy threshold = THRESHOLD_MULTIPLIER fraction of the median energy
    energies = [(s**2).sum() / len(s) for s in segments]
    # (attention: integer overflow would occure without normalization here!)
    threshold = THRESHOLD_MULTIPLIER * np.median(energies)
    
    index_of_silent_segments = get_best_silent_segments((np.where(energies < threshold)[0]))
    print(index_of_silent_segments) 
    # get segments that have energies higher than the threshold
    silence_segments = segments[index_of_silent_segments]

    # Write out the concatenated silence segments for manual verification
    #silence_signal = np.concatenate(silence_segments)
    #wavfile.write("splits/silence.wav", fs_wav, silence_signal)

    # Write out the slices
    prev = 0
    for splitter in index_of_silent_segments:
        if ((splitter - prev) * SEGMENT_SIZE_IN_SECONDS > 100):
            wavfile.write(OUTPUT_PATH + f[:-4] + '_' + str(sample_counter) + '.wav', fs_wav, np.concatenate(segments[prev:splitter+1] * (2**15)).astype(np.int16))
            prev = splitter
            sample_counter += 1
