import numpy as np
import scipy.io.wavfile as wf
import matplotlib.pyplot as plt
from tkinter import *
from tkinter.ttk import *
from tkinter import messagebox as mb

class App(Frame):
    def __init__(self, master=None):
        Frame.__init__(self, master)
        Style().theme_use('default')
        self.master = master
        self.master.title("Frequency Spectrum Analyzer")

        self.path = StringVar(self, value="data/1.wav")
        Label(self, text="Path").grid(row=0, column=0, padx=10, pady=10)
        Entry(self, textvariable=self.path).grid(row=0, column=1, padx=10, pady=10)

        self.start = IntVar(self, value=0)
        Label(self, text="Sample start (ms)").grid(row=1, column=0, padx=10, pady=10)
        Entry(self, textvariable=self.start).grid(row=1, column=1, padx=10, pady=10)

        self.end = IntVar(self, value=5000)
        Label(self, text="Sample end (ms)").grid(row=2, column=0, padx=10, pady=10)
        Entry(self, textvariable=self.end).grid(row=2, column=1, padx=10, pady=10)

        self.win_funs = {"Hanning":0, "Hamming":1, "None":2}
        self.win_fun = IntVar(self, value=0)
        Label(self, text="Windowing").grid(row=3, column=0, padx=10, pady=10)
        for i, (k, v) in enumerate(self.win_funs.items()):
            Radiobutton(self, variable=self.win_fun, text=k, value=v).grid(row=4, column=i, padx=10, pady=10)

        Button(self, command=self.action_load, text="Load WAV").grid(row=5, column=0, padx=10, pady=10)
        Button(self, command=self.action_synthesize, text="Synthesize WAV").grid(row=5, column=1, padx=10, pady=10)
        Button(self, command=self.action_spectrum, text="Show spectrum").grid(row=6, column=0, padx=10, pady=10)
        Button(self, command=self.action_spectrogram, text="Show spectrogram").grid(row=6, column=1, padx=10, pady=10)

        self.pack(fill=BOTH, expand=1)

    def action_load(self):
        # Reading WAV file
        raw = wf.read(self.path.get())
        self.rate, self.data = raw[0], raw[1]
        self.data = self.data[self.rate*self.start.get()//1000:self.rate*self.end.get()//1000]
        self.length = len(self.data)
        # Endpointing
        p, q = 25, 25
        dur_noise, dur_window = 0.1, 0.01
        n_noise, n_window = int(self.rate * dur_noise), int(self.rate * dur_window)
        noise = np.abs(self.data[:n_noise])
        lmt = np.mean(noise) + 2 * np.std(noise)
        windows = [1 if np.mean(np.abs(self.data[i:i+n_window])) > lmt else 0 for i in range(0, self.length, n_window)]
        self.window_replace(windows, 0, 1, p)
        i, j = self.window_replace(windows, 1, 0, q)
        if j - i == 0:
            mb.showerror("Error", "Only silence detected")
            return
        self.data = self.data[i*n_window:j*n_window]
        self.length = len(self.data)
        # Windowing function
        win_funs = [np.hanning, np.hamming, np.ones]
        self.data = self.data * win_funs[self.win_fun.get()](self.length)
        # Discrete Fourier Transform
        self.freq = np.linspace(1000 // (self.length / self.rate), self.rate // 2, self.length)
        self.amp = np.abs(np.fft.fft(self.data))
        self.amp = np.interp(self.amp, (self.amp.min(), self.amp.max()), (0, 100))

    def action_synthesize(self):
        path, length = self.path.get(), (self.end.get() - self.start.get()) // 1000
        rate, freqs = 44100, [220, 480, 620]
        data, t = np.zeros(rate * length), np.linspace(0, length, rate * length)
        for f in freqs:
            data = np.add(data, np.sin(f * 2 * np.pi * t))
        wf.write(path, rate, data)

    def action_spectrum(self):
        plt.plot(self.freq, self.amp)
        plt.xlabel("Frequency (Hz)")
        plt.ylabel("Magnitude (%)")
        plt.show()

    def action_spectrogram(self):
        plt.specgram(self.data, Fs=self.rate)
        plt.xlabel("Time (s)")
        plt.ylabel("Frequency (Hz)")
        plt.gca().grid(axis='y')
        plt.show()

    def window_replace(self, arr, curr, repl, occrs):
        i, lmt, max_i, max_j = 0, len(arr), -1, -1
        if arr[-1] != repl:
            arr.append(repl)
            lmt -= 1
        while i < lmt:
            if arr[i] == curr:
                j = arr.index(repl, i+1)
                if j - i > max_j - max_i:
                    max_i, max_j = i, j
                elif j - i < occrs:
                    arr[i:j] = [repl] * (j-i)
                i = j
            i += 1
        return max_i, max_j

root = Tk()
root.resizable(False, False)
App(root)
root.mainloop()
