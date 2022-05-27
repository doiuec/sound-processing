import stegano.tools as tools
import soundfile as sf
import numpy as np
from scipy.io.wavfile import write as wav_write
from scipy.io.wavfile import read as wav_read
import matplotlib.pyplot as plt

def embedding(input:str, output:str, message:str):
    index = 0
    _fs, input_data = wav_read(input, False)
    # WavFileWarning: Chunk (non-data) not understood, skipping it.
    # scipy が wavファイルのチャンクを読み取れなかったぽい

#TODO:SoundFile オブジェクトを作る
    # https://pysoundfile.readthedocs.io/en/latest/#soundfile-objects
    with sf.SoundFile(input) as f:
        channel = f.channels
        frame = f.frames
        samplerate = f.samplerate
    length = input_data.shape[0] / samplerate
    _time = np.linspace(0., length, input_data.shape[0])

#TODO: scipy の wav_read の shape を vector へ
    #print(np.ndim(input_data))
    ## 2
    #print(len(input_data))
    ## 264600
    #print(frame)
    ## 264600

#TODO: message にヘッダ情報をつける
    header = "header" + str(len(message)) + ":"
    secret = header + str(message)

#TODO: message を 1,0 に変換
    # https://github.com/cedricbonhomme/Stegano/blob/master/stegano/tools.py
    bits = "".join(tools.a2bits_list(secret))
    #print(bits)
    #print(secret)

#TODO: 音源フレームに，LSB で埋め込み
    for i in range(frame):
        for j in range(channel):
            if (i * 2) + j + 1 < len(bits):
                #print(str(input_data[i][j]) + "+" + str(bits[index]))
                input_data[i][j] = input_data[i][j] & 1 | int(bits[index])
                #print(input_data[i][j])
                #print(input_data[index][j])
            #print(i)
            index = index + 1
    
#TODO: vector を戻す
#TODO: 書き込み
    wav_write(output, samplerate, input_data)


def unearth(input: str):
    index = 0
    cnt = 0
    ascii = []
    tmp = []
    sum = 0
    put = 0

    _fs, input_data = wav_read(input, False)
    with sf.SoundFile(input) as f:
        channel = f.channels
        frame = f.frames
        samplerate = f.samplerate

    length = input_data.shape[0] / samplerate
    for  i in range(frame):
        for j in range(channel):
            ascii.append(input_data[i][j] & 1)
            cnt = cnt + 1
            #print(cnt)
            if cnt == 8:
                #print(ascii)
                for k in range(len(ascii)):
                    #print(k)
                    #print(str(sum) + "+" + str(2**k) + "*" + str(ascii[7-k]))
                    sum = sum + (2**k) * ascii[7-k]
                #print(sum)
                if put == 1:
                    tmp.append(chr(sum))
                if chr(sum) == ":":
                    put = 1
                if chr(sum) == "!":
                    break
                #print(chr(sum))
                cnt = 0
                ascii.clear()
                index = index + 1
                sum = 0
        else:
            continue
        break
    print("".join(tmp))


def main():
    input_file = './INPUT.wav'
    output_file = './OUTPUT.wav'

    embedding(input_file, output_file, "Please conceal me!")
    unearth(output_file)

if __name__ == '__main__':
    main()
