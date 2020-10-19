import numpy as np
import scipy.io.wavfile as wf
import matplotlib.pyplot as plt
from tkinter import *
from tkinter.ttk import *
from tkinter import messagebox as mb

def window_replace(arr, curr, repl, min):
    i, lmt = 0, len(arr)
    max_i, max_j = -1, -1
    if arr[-1] != repl:
        arr.append(repl)
        lmt -= 1
    while i < lmt:
        if arr[i] == curr:
            j = arr.index(repl, i+1)
            if j - i > max_j - max_i:
                max_i, max_j = i, j
            if j - i < min:
                arr[i:j] = [repl] * (j-i)
            i = j
        i += 1
    return max_i, max_j

class App(Frame):
    def __init__(self, master=None):
        Frame.__init__(self, master)
        Style().theme_use('default')
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
        Label(self, text="Sample end (ms)").grid(row=2, column=0, padx=10, pady=10)
        Entry(self, textvariable=self.sample_end).grid(row=2, column=1, padx=10, pady=10)

        # Windowing function
        self.win_funs = {"Hanning":0, "Hamming":1, "None":2}
        self.win_fun = IntVar(self, value=0)
        Label(self, text="Windowing").grid(row=3, column=0, padx=10, pady=10)
        for i, (k, v) in enumerate(self.win_funs.items()):
            Radiobutton(self, variable=self.win_fun,
                    text=k, value=v).grid(row=4, column=i, padx=10, pady=10)

        # Load
        Button(self, command=self.action_load,
                text="Load").grid(row=5, column=0, padx=10, pady=10)

        # Synthesize
        Button(self, command=self.action_synthesize,
                text="Synthesize").grid(row=5, column=1, padx=10, pady=10)

        # Spectrum
        Button(self, command=self.action_spectrum,
                text="Spectrum").grid(row=6, column=0, padx=10, pady=10)

        # Spectrogram
        Button(self, command=self.action_spectrogram,
                text="Spectrogram").grid(row=6, column=1, padx=10, pady=10)

        self.pack(fill=BOTH, expand=1)

    def action_load(self):
        path = self.path.get()
        # Read WAV file
        raw = wf.read(path)
        self.sample_rate, self.data = raw[0], raw[1]
        start = int(self.sample_rate * self.sample_start.get() / 1000)
        end = int(self.sample_rate * self.sample_end.get() / 1000)
        self.data = self.data[start:end]
        # Perform endpointing
        dur_noise = 0.1
        n_noise = int(self.sample_rate * dur_noise)
        noise = np.abs(self.data[:n_noise])
        lmt = np.mean(noise) + 2 * np.std(noise)
        dur_window = 0.01
        n_window = int(self.sample_rate * dur_window)
        windows = [1 if np.mean(np.abs(self.data[i:i+n_window])) > lmt else 0 for i in range(0, len(self.data), n_window)]
        p, q = 3, 3
        window_replace(windows, 0, 1, p)
        i, j = window_replace(windows, 1, 0, q)
        if j - i > 0:
            self.data = self.data[i*n_window:j*n_window]
        else:
            mb.showerror("Error", "No spoken word detected")

    def action_synthesize(self):
        # Generate WAV file
        path = self.path.get()
        duration = (self.sample_end.get() - self.sample_start.get()) / 1000
        sample_rate = 44100
        freqs = [220, 440, 620]
        t = np.linspace(0, duration, sample_rate * duration)
        data = np.zeros(t.shape)
        for f in freqs:
            data = np.add(data, np.sin(f * 2 * np.pi * t))
        wf.write(path, sample_rate, data)

    def action_spectrum(self):
        # Apply windowing function
        win_funs = [np.hanning, np.hamming, np.ones]
        win_fun = self.win_fun.get()
        self.data = self.data * win_funs[win_fun](len(self.data))
        # Perform Discrete Fourier Transform
        duration = len(self.data) / self.sample_rate
        freq = np.linspace(1000 // duration, self.sample_rate // 2, len(self.data))
        amp = np.abs(np.fft.fft(self.data))
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
