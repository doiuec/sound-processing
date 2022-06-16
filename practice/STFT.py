import csv
import numpy as np
import matplotlib.pyplot as pl
from scipy import ceil, complex64, float64, hamming, zeros
from scipy.fftpack import fft# , ifft
from scipy import ifft 

data = []
with open("result.csv","r") as f:
    reader = csv.reader(f)
    for row in reader:
        data.append(row[0])
fftLen = 60 
win = hamming(fftLen) 
step = fftLen//4
fdata = [float(s) for s in data]

def stft(x, win, step):
    l = len(x)
    N = len(win)
    M = int(ceil(float(l-N+step)/step))
    new_x = zeros(N+((M-1)*step), dtype = float64)
    x = new_x[:l]

    X = zeros([M,N],dtype = complex64)
    for m in range(M):
        start = step * M
        X[m, :] = fft(new_x[start : start + N] * win)
    return X

spectrogram = stft(fdata, win, step)

fig = pl.figure()
fig.add_subplot(311)
pl.plot(fdata)
pl.xlim([0, len(fdata)])
pl.title("Input signal", fontsize = 20)
fig.add_subplot(313)
pl.imshow(abs(spectrogram[:, : fftLen // 2 + 1].T), aspect = "auto", origin = "lower")
pl.title("Spectrogram", fontsize = 20)
pl.show()
print(spectrogram)
