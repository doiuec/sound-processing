import stegano.tools as tools
import soundfile as sf
import numpy as np
from scipy.io.wavfile import write as wav_write
from scipy.io.wavfile import read as wav_read
import matplotlib.pyplot as plt

def embedding(input:str, output:str, message:str):
    index = 0
    fs, input_data = wav_read(input, False)
    # WavFileWarning: Chunk (non-data) not understood, skipping it.
    # scipy が wavファイルのチャンクを読み取れなかったぽい

#TODO:SoundFile オブジェクトを作る
    # https://pysoundfile.readthedocs.io/en/latest/#soundfile-objects
    with sf.SoundFile(input) as f:
        channel = f.channels
        frame = f.frames
        samplerate = f.samplerate
    length = input_data.shape[0] / samplerate
    time = np.linspace(0., length, input_data.shape[0])

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
                input_data[index][j] = input_data[index][j] & ~1 | int(bits[index])
            #print(i)
        index = index + 1
    
#TODO: vector を戻す
#TODO: 書き込み
    wav_write(output, samplerate, input_data)

def unearth(input: str):

    ascii = []

    _fs, input_data = wav_read(input, False)
    with sf.SoundFile(input) as f:
        channel = f.channels
        frame = f.frames
        samplerate = f.samplerate

    length = input_data.shape[0] / samplerate
    for  i in range(frame):
        for j in range(channel):
            
#TODO: 最下位ビットを取得
#TODO: 8回取得したら復元
#TODO: 取得したかの確認（末尾）
#TODO: メッセージの書き出し
            
def main():
    input_file = './INPUT.wav'
    output_file = './OUTPUT.wav'

    embedding(input_file, output_file, "Please conceal me!")

if __name__ == '__main__':
    main()
