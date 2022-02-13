from cmath import e
import wave as wave
import numpy as np
import scipy.signal as sp
import sounddevice as sd
import math, argparse

parser = argparse.ArgumentParser(description="spectrum subtraction")
        # コマンドライン引数で入力を受け取る準備
        # description を入れておくと， -h を入れたときにヘルプが出る
parser.add_argument("-f", "--file", help="input .wav file", metavar="<.wav>", required=True)
        # -f or --file とオプションを入れると，それを検証する
        # metaver はヘルプ表示の時の変数名
        # required が True だと必須の引数 
args = parser.parse_args()


# sample_wave_file="./CMU_ARCTIC/cmu_us_aew_arctic/wav/arctic_a0001.wav"
sample_wave_file = args.file

wav = wave.open(sample_wave_file)

'''
CMUから得た信号を一次元バッファに直して保存
'''
speech_length = wav.getnframes()
sampling_rate = wav.getframerate()
speech_signal = wav.readframes(speech_length)
speech_signal = np.frombuffer(speech_signal, dtype=np.int16)

'''
白色雑音を印加する
'''
noise_length = 40000
all_length = noise_length + speech_length
np.random.seed(0)
# 正規表現からノイズを作る
noise_signal = np.random.normal(scale = 0.04, size = all_length)
# 目的信号は一次元バッファ(2バイト)なので，それに合うように調整する
# ノイズ信号は大きいから，2バイトに合わせる必要がある
# iinfo.max で，正規化する
noise_signal = noise_signal*np.iinfo(np.int16).max
noise_signal = noise_signal.astype(np.int16)
# noise_signal = np.frombuffer(noise_signal, dtype=np.int16)
# print(speech_signal)
# print(noise_signal)

'''
雑音(noise_signal)と希望信号(speech_signal)を混ぜる
              400000 points
                   ||       
                   \/
--  noise_signal  -||--noise_signal + speech_signal--
+++++++++++++++++++++++++++++++++++++++++++++++++++++
'''
signal = noise_signal
signal = signal[noise_length:] + speech_signal
sd.play(signal, wav.getframerate())
print("処理前信号")
status = sd.wait()

'''
stft，つまり時間によって変化する非同期信号を一定間隔で切り出し，その周波数特性を考える
stft(x, fs, window, nperseg, noverlap)
    x : 計算対象の時間基準の配列
    fs : サンプルレート，ノイズを削る信号のサンプルレートに依存している
    window : ハニング窓
    nperseg : 窓関数の幅
    noverpal : 窓関数の重なり

    f : 配列の周波数単位
    t : 時間単位
    Zxx : 計算結果
'''
f, t, Zxx = sp.stft(signal, fs=wav.getframerate(), window = "hann", nperseg = 512, noverlap = 256)

'''
処理前信号の雑音を分析する
'''
amp = np.abs(Zxx)
phase = Zxx / np.maximum(amp, 1.e-20)
noise_time = (noise_length / sampling_rate) / (t[1] - t[0])
noise_time = math.ceil(noise_time)
# print(noise_time)

p = 1
alpha = 2

# ノイズの振幅を求める
# 入力信号の絶対値を二乗して平均を求める
noise_amp = np.power(amp, 2)[:,:noise_time]
# noise_amp = np.power(amp,2)[:,:noise_time]
# noise_amp = noise_amp[:noise_time]
noise_amp = np.mean(noise_amp,axis=1,keepdims=True)
noise_amp = np.power(noise_amp, 1/2)
# noise_amp=np.power(np.mean(np.power(amp,p)[:,:noise_time],axis=1,keepdims=True),1./p)
e = 0.01*np.power(amp, p)
'''
その信号を処理する
'''
after_signal = np.maximum(np.power(amp, p) - alpha*np.power(noise_amp, p), e)
after_signal = np.power(after_signal, 1./p)

# 処理後の信号の位相成分は入力信号と同じものを使う
after_signal = after_signal*phase
t, after_data = sp.istft(after_signal, fs=wav.getframerate(), window = "hann", nperseg = 512, noverlap = 256)
after_data = after_data.astype(np.int16)

sd.play(after_data, wav.getframerate())
print("処理後信号")
status = sd.wait()

#waveファイルに書き込む
wave_out = wave.open("./process_wave_ss.wav", 'w')
wave_out.setnchannels(1)
wave_out.setsampwidth(2)
wave_out.setframerate(wav.getframerate())
wave_out.writeframes(after_data)
wave_out.close()

print("yes")
# print(f)
# print(t)
# print(Zxx)
