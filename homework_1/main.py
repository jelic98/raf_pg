import numpy as np
import scipy.io.wavfile as wf
import matplotlib.pyplot as plt
from tkinter import *
from tkinter.ttk import *

class App(Frame):
    def __init__(self, master=None):
        Frame.__init__(self, master)
        Style().theme_use("default")
        self.master = master
        self.master.title("Frequency Spectrum")

        for widget in self.winfo_children():
            widget.destroy()

        # Path
        self.path = StringVar(self, value="data/1.wav")
        Label(self, text="Path").grid(row=0, column=0, padx=10, pady=10)
        Entry(self, textvariable=self.path).grid(row=0, column=1, padx=10, pady=10)

        # Sample start
        self.sample_start = IntVar(self, value=0)
        Label(self, text="Sample start (ms)").grid(row=1, column=0, padx=10, pady=10)
        Entry(self, textvariable=self.sample_start).grid(row=1, column=1, padx=10, pady=10)

        # Sample end
        self.sample_end = IntVar(self, value=1000)
        Label(self, text="Sample end (ms)").grid(row=1, column=0, padx=10, pady=10)
        Entry(self, textvariable=self.sample_end).grid(row=1, column=1, padx=10, pady=10)

        # Windowing function
        self.win_funs = {"Hanning":0, "Hamming":1, "None":2}
        self.win_fun = IntVar(self, value=0)
        Label(self, text="Windowing").grid(row=2, column=0, padx=10, pady=10)
        for i, (k, v) in enumerate(self.win_funs.items()):
            Radiobutton(self, variable=self.win_fun,
                    text=k, value=v).grid(row=3, column=i, padx=10, pady=10)

        # Load
        Button(self, command=self.action_load,
                text="Load").grid(row=4, column=0, padx=10, pady=10)

        # Synthesize
        Button(self, command=self.action_synthesize,
                text="Synthesize").grid(row=4, column=1, padx=10, pady=10)

        # Spectrum
        Button(self, command=self.action_spectrum,
                text="Spectrum").grid(row=5, column=0, padx=10, pady=10)

        # Spectrogram
        Button(self, command=self.action_spectrogram,
                text="Spectrogram").grid(row=5, column=1, padx=10, pady=10)

        self.pack(fill=BOTH, expand=1)

    def action_load(self):
        path = self.path.get()
        # Read WAV file
        raw = wf.read(path)
        self.sample_rate, self.data = raw[0], raw[1]
        self.n_samples = len(self.data)
        # Perform endpointing
        dur_noise = 0.1
        n_noise = int(self.sample_rate * dur_noise)
        noise = np.abs(self.data[0:n_noise])
        lmt = np.mean(noise) + 2 * np.std(noise)
        dur_window = 0.01
        n_window = int(self.sample_rate * dur_window)
        windows = [0] * n_window
        p, q, r = 3, 3, 10
        for i in range(n_window, self.n_samples, n_window):
            val = sum(s for s in np.abs(self.data[i:i+n_window])) / n_window
            bin = 1 if val > lmt else 0
            windows.append(bin)
            if bin == 1 and sum(windows[i-p-1:i]) > 0 and sum(windows[i-r:i+1]) > r - p:
                windows[i-p:i] = [1] * p
        state = 0
        for i, w in enumerate(windows[q:]):
            if windows[i] == 0 and state == 1 and 0 < sum(windows[i-q:i]) < q:
                windows[i-q:i] = [0] * q
                state = windows[i]

    def action_synthesize(self):
        # Generate WAV file
        path = self.path.get()
        duration = (self.sample_end.get() - self.sample_start.get()) / 1000
        sample_rate = 44100
        freqs = [220, 440, 620]
        phases = [np.pi / 2, np.pi / 3, np.pi / 6]
        t = np.linspace(0, duration, sample_rate * duration)
        data = np.zeros(t.shape)
        for f, p in zip(freqs, phases):
            data = np.add(data, np.sin(p + f * 2 * np.pi * t))
        wf.write(path, sample_rate, data)

    def action_spectrum(self):
        # Apply windowing function
        win_funs = [np.hanning, np.hamming, np.ones]
        win_fun = self.win_fun.get()
        data = self.data * win_funs[win_fun](self.n_samples)
        # Perform Discrete Fourier Transform
        duration = self.n_samples / self.sample_rate
        freq = np.linspace(1000 // duration, self.sample_rate // 2, self.n_samples)
        amp = np.abs(np.fft.fft(data))
        amp_norm = np.interp(amp, (amp.min(), amp.max()), (0, 100))
        # Show spectrum
        plt.plot(freq, amp_norm)
        plt.show()

    def action_spectrogram(self):
        # Show spectrogram
        plt.specgram(self.data, Fs=self.sample_rate)
        plt.show()

root = Tk()
root.resizable(False, False)
app = App(root)
root.mainloop()
