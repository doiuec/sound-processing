import csv
import numpy as np
import matplotlib.pyplot as plt
from scipy import signal

data = []
with open("result.csv","r") as f:
    reader = csv.reader(f)
    for row in reader:
        data.append(row[1])

arr = np.array(data)

farr = np.asarray(arr, dtype=float)

print(type(farr[0]))

print(farr)

fs = 60e5

f, t, Sxx = signal.spectrogram(farr, fs)

plt.pcolormesh(t, f, 10*np.log(Sxx)) #intensityを修正
plt.ylabel('Frequency [Hz]')
plt.xlabel('Time [sec]')
cbar = plt.colorbar() #カラーバー表示のため追加
cbar.ax.set_ylabel("Intensity [dB]") #カラーバーの名称表示のため追加
plt.show()