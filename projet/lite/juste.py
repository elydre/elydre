import sounddevice as sd
import numpy as np
import time

def play_freqs(freqs, duration=2, sample_rate=44100):

    # mix the frequencies
    t = np.linspace(0, duration + 1, int(sample_rate * (duration + 1)), False)
    signal = np.sum([np.sin(2 * np.pi * f * t) for f in freqs], axis=0)

    # normalize the signal to -1 to 1
    signal /= np.max(np.abs(signal))

    # play the sound
    sd.play(signal, sample_rate)
    time.sleep(duration)

fifth = lambda f: f * 3/2
major_third = lambda f: f * 5/4
minor_third = lambda f: f * 6/5
quart = lambda f: f * 4/3

# play a single frequency
play_freqs([200, major_third(200), fifth(200)], 2)

sd.stop()
