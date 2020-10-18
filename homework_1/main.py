import numpy as np
import matplotlib.pyplot as plt
import scipy.io.wavfile as wf
from IPython.display import Audio

# Hyperparameters
p, q, r = 3, 3, 10
sample_rate = 44100
freqs = [220, 440, 620]
phases = [np.pi / 2, np.pi / 3, np.pi / 6]

# Configurable parameters
win_id = 0
duration = 5
in_path, out_path = 'data/1.wav', 'data/5.wav'

# Generate WAV file
t = np.linspace(0, duration, sample_rate * duration)
data = np.zeros(t.shape)
for f, p in zip(freqs, phases):
    data = np.add(data, np.sin(p + f * 2 * np.pi * t))

wf.write(out_path, sample_rate, data)
Audio(data, rate=sample_rate)

# Read WAV file
raw = wf.read(in_path)
sample_rate, data = raw[0], raw[1]
n_samples = len(data)
duration = n_samples / sample_rate

# Perform endpointing
dur_noise = 0.1
n_noise = int(sample_rate * dur_noise)
noise = np.abs(data[0:n_noise])
lmt = np.mean(noise) + 2 * np.std(noise)

dur_window = 0.01
n_window = int(sample_rate * dur_window)
windows = [0] * n_window
for i in range(n_window, n_samples, n_window):
    val = sum(s for s in np.abs(data[i:i+n_window])) / n_window
    bin = 1 if val > lmt else 0
    windows.append(bin)
    if bin == 1 and sum(windows[i-p-1:i]) > 0 and sum(windows[i-r:i+1]) > r - p:
        windows[i-p:i] = [1] * p

state = 0
for i, w in enumerate(windows[q:]):
    if windows[i] == 0 and state == 1 and 0 < sum(windows[i-q:i]) < q:
        windows[i-q:i] = [0] * q
    state = windows[i]

# Apply windowing function
win_funs = [np.hanning, np.hamming, np.ones]
data = data * win_funs[win_id](n_samples)

# Perform Discrete Fourier Transform
freq = np.linspace(1000 // duration, sample_rate // 2, n_samples)
amp = np.abs(np.fft.fft(data))
amp_norm = np.interp(amp, (amp.min(), amp.max()), (0, 100))

# Show spectrum
plt.plot(freq, amp_norm)
plt.show()

# Show spectogram
plt.specgram(data, Fs=sample_rate)
plt.show()