
import math
import sys
sys.path.append('../edit-waves')

from WaveCore import FmtSubchunk
from WaveCore import DataSubchunk
from WaveCore import WaveData

import numpy as np

import matplotlib.pyplot as plt
from matplotlib import animation

STD_AMP = 1000

BIT0_FREQ = 1000
BIT1_FREQ = 2000
FRAMER_FREQ = 4000

# 10ms per symbol -> 100 sps
SYM_PERIOD = 0.01


def create_sin_wave(data_period: float, sample_rate: int, amp: int, freq: int) -> [[]]:
    num_samples = int(data_period * sample_rate)
    sample_period = 1 / sample_rate

    sin_wave = [0] * num_samples

    for smp in range(num_samples):
        t = smp * sample_period
        sin_wave[smp] = int(amp * math.sin(2 * math.pi * freq * t))

    return sin_wave


def encode_data(data: [], num_channel: int, sample_rate: int) -> [[]]:
    bit0_wave = create_sin_wave(SYM_PERIOD, sample_rate, STD_AMP, BIT0_FREQ)
    bit1_wave = create_sin_wave(SYM_PERIOD, sample_rate, STD_AMP, BIT1_FREQ)
    framer_wave = create_sin_wave(SYM_PERIOD, sample_rate, STD_AMP, FRAMER_FREQ)

#    print(len(bit0_wave))
#    print(bit1_wave)
    def copy_array(dst: [], dst_index: int, src: []):
        for i in range(len(src)):
            dst[dst_index + i] = src[i]

    encoded_data = [[0] * len(data) * (8 + 1) * len(bit0_wave)] * num_channel

#    print(len(encoded_data[0]))
#    print(len(encoded_data[1]))

    indx = 0
    for dt in data:
#        print(str(indx))
        d = dt
        for ch in range(num_channel):
            copy_array(encoded_data[ch], indx, framer_wave)
        indx += len(framer_wave)
        for i in range(8):
#            print("indx:" + str(indx))
            b0 = d & 0b1
#            print(b0)
            if b0 == 0:
                for ch in range(num_channel):
                    copy_array(encoded_data[ch], indx, bit0_wave)
            else:
                for ch in range(num_channel):
                    copy_array(encoded_data[ch], indx, bit1_wave)
            d >>= 1
            indx += len(bit0_wave)

#    print(len(encoded_data[0]))
#    print(len(encoded_data[1]))

    return encoded_data


#def seek_for_wave(data_array: [], freq: int) -> bool:

def decode_data(wav_data: WaveData) -> bytearray:
    print(wav_data)

    sym_period_cnt = int(wav_data.fmt.sample_rate * SYM_PERIOD)
    audio_data = wav_data.data.audio_data[0]

    f_datas = []
    freqs = []

#    X = fft(x)
#    N = len(X)
#    n = np.arange(N)
#    T = N/sr
#    freq = n/T = np.arange(N) / N * sr

    for i in range(0, len(audio_data), 1):
        start = i
        end = min(start + sym_period_cnt, len(audio_data))
        sym_data = audio_data[start:end]
        sym_data_f = np.fft.fft(sym_data)
        f_datas.append(abs(sym_data_f))
        freqs.append(np.arange(len(sym_data_f)) / len(sym_data_f) * wav_data.fmt.sample_rate)


    # Create a figure and axis
    fig, ax = plt.subplots()
    plt.xlabel('freq')
    plt.ylabel('amp')

#    line, = ax.plot(np.fft.fftfreq(f_datas[0]), f_datas[0])

    #plt.plot(f_datas[0].real, f_datas[0].real)
    line, = ax.plot(freqs[0][:100], f_datas[0][:100])

    def update_graph(frame):
        plt.title('frequent domain amplitude: time({:.4f})'.format(frame / wav_data.fmt.sample_rate))
        line.set_xdata(freqs[frame][:100])
        line.set_ydata(abs(f_datas[frame][:100]))
        return line


    ani=animation.FuncAnimation(fig, update_graph, frames=len(f_datas), interval=10)

    plt.show()


    decoded_data = bytearray(10)
#    print(type(decoded_data))


    return decoded_data
