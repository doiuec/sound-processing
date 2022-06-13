import pyvisa as visa
import time
import csv
import numpy as np
 
rm = visa.ResourceManager()
inst = rm.list_resources()
usb = list(filter(lambda x: 'USB' in x, inst))
scope = rm.open_resource(usb[0])
print(scope.query("*IDN?"))

scope.write(":STOP")

scope.write(":WAV:SOUR CHAN1")
scope.write(":WAV:MODE RAW")
scope.write(":WAV:FORM BYTE")
scope.write(":WAV:STAR 1")
scope.write(":WAV:STOP 120000")


preample = scope.query(':WAV:PRE?').split(',')
#preample[0] : format(0...BYTE)
#preample[1] : type(2...RAW)
points = int(preample[2])
xinc = float(preample[4]) # 時間軸に対するインクリメント
xorg = float(preample[5]) # x軸データの開始
xref = float(preample[6]) # x:offset
yinc = float(preample[7]) # y軸に対するインクリメント
yorg = float(preample[8]) # y軸データの開始
yref = float(preample[9]) # y:offset

#print(preample)

data_bin = scope.query_binary_values('WAV:DATA?', datatype='B', container=bytes)
time.sleep(3)

t = [(float(i) - xref)*xinc + xorg for i in range(points)]
v = [(float(byte_data) - yref)*yinc + yorg for byte_data in data_bin]

#print(t)
#print(len(v))

data = []
data.append(t)
data.append(v)
data = np.array(data).T
print(data)

#load_data = {}
#load_data['time'] = t
#load_data['data'] = v
#print(load_data)

with open("result.csv", 'w') as f:
    writer = csv.writer(f, lineterminator='\n')
    writer.writerows(data)