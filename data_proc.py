import librosa
from tqdm import tqdm
import numpy as np
import os
from keras.utils.np_utils import to_categorical

DATA_PATH = 'C:\\Users\\silly\\Documents\\voice_pathology\\SVD_db\\u'


def get_labels(path=DATA_PATH):
    labels = os.listdir(path)
    label_indices = np.arange(0, len(labels))
    return labels, label_indices, to_categorical(label_indices)


def wav2mfcc(file_path, max_len=11):
    wave, sr = librosa.load(file_path, mono=True, sr=None)
    wave = wave[::3]
    mfcc = librosa.feature.mfcc(wave, sr=16000)

    # If maximum length exceeds mfcc lengths then pad the remaining ones
    if max_len > mfcc.shape[1]:
        pad_width = max_len - mfcc.shape[1]
        mfcc = np.pad(mfcc, pad_width=((0, 0), (0, pad_width)), mode='constant')

    # Else cutoff the remaining parts
    else:
        mfcc = mfcc[:, :max_len]

    return mfcc


def save_data_to_array(path=DATA_PATH, max_len=11):
    labels, _, _ = get_labels(path)

    for label in labels:
        # Init mfcc vectors
        mfcc_vectors = []

        wavfiles = [path + '\\' + label ]#+ '\\' + wavfile for wavfile in os.listdir(path + '\\' + label)]
        for wavfile in tqdm(wavfiles, "Saving vectors of label - '{}'".format(label)):
            mfcc = wav2mfcc(wavfile, max_len=max_len)
            mfcc_vectors.append(mfcc)
        np.save('npy_u\\' + label + '.npy', mfcc_vectors)
        print('saved data : ', label)


def save_data_to_array_nonhuman_only(path=DATA_PATH, max_len=11):
    labels, _, _ = get_labels(path)

    for label in labels:
        # Init mfcc vectors
        mfcc_vectors = []

        wavfiles = [path + '\\' + label ]#+ '\\' + wavfile for wavfile in os.listdir(path + '\\' + label)]
        for wavfile in tqdm(wavfiles, "Saving vectors of label - '{}'".format(label)):
            if wavfile[-7:] == 'egg.wav':
                mfcc = wav2mfcc(wavfile, max_len=max_len)
                mfcc_vectors.append(mfcc)
        np.save('npy_u\\' + label + '.npy', mfcc_vectors)
        print('saved data : ', label)


def save_data_to_array_voice_only(path=DATA_PATH, max_len=11):
    labels, _, _ = get_labels(path)

    for label in labels:
        # Init mfcc vectors
        mfcc_vectors = []

        wavfiles = [path + '\\' + label ]#+ '\\' + wavfile for wavfile in os.listdir(path + '\\' + label)]
        for wavfile in tqdm(wavfiles, "Saving vectors of label - '{}'".format(label)):
            if wavfile[-7:] != 'egg.wav':
                mfcc = wav2mfcc(wavfile, max_len=max_len)
                mfcc_vectors.append(mfcc)
        np.save('npy_u\\' + label + '.npy', mfcc_vectors)
        print('saved data : ', label)


if __name__ == '__main__':
    save_data_to_array_voice_only(max_len=50)