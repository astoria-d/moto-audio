
import math
import sys
sys.path.append('../edit-waves')

from WaveCore import FmtSubchunk
from WaveCore import DataSubchunk
from WaveCore import WaveData


STD_AMP = 1000
BIT0_FREQ = 1000
BIT1_FREQ = 2000
FRAMER_FREQ = 4000
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

#    print(bit0_wave)
#    print(bit1_wave)

    encoded_data = [[]] * num_channel

    for dt in data:
        for ch in range(num_channel):
            encoded_data[ch].extend(framer_wave)
        for i in range(8):
            b0 = dt & 0b1
            print(b0)
            if b0 == 0:
                for ch in range(num_channel):
                    encoded_data[ch].extend(bit0_wave)
            else:
                for ch in range(num_channel):
                    encoded_data[ch].extend(bit1_wave)
            dt >>= 1

#    print(encoded_data)

    return encoded_data

def decode_data(wav_data: WaveData) -> bytearray:
    print(wav_data)

    decoded_data = bytearray(10)
#    print(type(decoded_data))


    return decoded_data
