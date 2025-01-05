
import sys
sys.path.append('../edit-waves')

from WaveCore import FmtSubchunk
from WaveCore import DataSubchunk
from WaveCore import WaveData

import math
import numpy as np

from scipy.signal import butter, lfilter


def butter_lowpass(cutoff, fs, order=5):
    nyq = 0.5 * fs
    normal_cutoff = cutoff / nyq
    b, a = butter(order, normal_cutoff, btype='low', analog=False)
    return b, a

def rc_low_pass(x_input: float, prev_output: float, alpha: float):
    # https://en.wikipedia.org/wiki/Low-pass_filter

    # y(i) = alpha * x(i) + (1 - alpha) * y(i-1)
    # rc = 1 / (2 * pi * fc)
    # dt = 1 / sampling_rate
    # alpha = dt / (rc + dt)

    return alpha * x_input + (1 - alpha) * prev_output


def create_wave(wave: WaveData, sound_data: [[]]):
    bytes_per_sample = int(wave.fmt.bits_per_sample / 8)
    block_align = bytes_per_sample * wave.fmt.num_channel

    fmt = FmtSubchunk()
    fmt.subchunk_id = wave.fmt.subchunk_id
    fmt.sub_chunk_size = wave.fmt.sub_chunk_size
    fmt.audio_format = wave.fmt.audio_format
    fmt.num_channel = wave.fmt.num_channel
    fmt.sample_rate = wave.fmt.sample_rate
    fmt.byte_rate = wave.fmt.byte_rate
    fmt.block_align = block_align
    fmt.bits_per_sample = wave.fmt.bits_per_sample

    wdata = DataSubchunk()
    wdata.subchunk_id = wave.data.subchunk_id
    wdata.sub_chunk_size = wave.data.sub_chunk_size
    wdata.audio_data = sound_data

    filtered_wave = WaveData()
    filtered_wave.chunk_id = wave.chunk_id
    filtered_wave.chunk_size = 36 + wave.data.sub_chunk_size
    filtered_wave.format = wave.format
    filtered_wave.fmt = fmt
    filtered_wave.data = wdata

    return filtered_wave

def butter_worse_lpf(wave: WaveData, fc: float):
    num_samples = int(wave.data.sub_chunk_size / wave.fmt.num_channel / wave.fmt.bits_per_sample * 8)
    filtered_sound_val = [[0] * num_samples] * wave.fmt.num_channel

    b, a = butter_lowpass(fc, wave.fmt.sample_rate)
    for ch in range(wave.fmt.num_channel):
        # use scipy...
        filtered = lfilter(b, a, wave.data.audio_data[ch])
        for smp in range(num_samples):
            filtered_sound_val[ch][smp] = int(filtered[smp])

    return create_wave(wave, filtered_sound_val)

def rc_lpf(wave: WaveData, fc: float):

    num_samples = int(wave.data.sub_chunk_size / wave.fmt.num_channel / wave.fmt.bits_per_sample * 8)
    filtered_sound_val = [[0] * num_samples] * wave.fmt.num_channel

    rc = 1 / (2 * math.pi * fc)
    dt = 1 / wave.fmt.sample_rate
    alpha = dt / (rc + dt)

    for ch in range(wave.fmt.num_channel):
        prev_out = 0
        for smp in range(num_samples):
            wave_val = float(wave.data.audio_data[ch][smp])
            filtered_val = rc_low_pass(wave_val, prev_out, alpha)
            filtered_sound_val[ch][smp] = int(filtered_val)
            prev_out = filtered_val

    return create_wave(wave, filtered_sound_val)

# https://github.com/jimmyberg/LowPassFilter/blob/master/LowPassFilter.cpp
def rc_lpf2(wave: WaveData, fc: float):

    num_samples = int(wave.data.sub_chunk_size / wave.fmt.num_channel / wave.fmt.bits_per_sample * 8)
    dt = 1 / wave.fmt.sample_rate
    filtered_sound_val = [[0] * num_samples] * wave.fmt.num_channel

    epow = 1 - math.exp(-dt * 2 * math.pi * fc)

    for ch in range(wave.fmt.num_channel):
        prev_out = 0
        for smp in range(num_samples):
            wave_val = float(wave.data.audio_data[ch][smp])
            prev_out += (wave_val - prev_out) * epow
            filtered_sound_val[ch][smp] = int(prev_out)

    return create_wave(wave, filtered_sound_val)


# https://electricala2z.com/electrical-circuits/low-pass-and-high-pass-filter-frequency-response/
def rc_lpf_ftt(wave: WaveData, fc: float):

    num_samples = int(wave.data.sub_chunk_size / wave.fmt.num_channel / wave.fmt.bits_per_sample * 8)
    dt = 1 / wave.fmt.sample_rate
    filtered_sound_val = [[0] * num_samples] * wave.fmt.num_channel

    for ch in range(wave.fmt.num_channel):
        fft_amp = np.fft.fft(wave.data.audio_data[ch])
        freq = np.fft.fftfreq(len(wave.data.audio_data[ch]), d=dt)

        fft_lpf = [0] * num_samples
        for i in range(len(freq)):
            fft_lpf[i] = fft_amp[i] / math.sqrt( 1 + (freq[i] / fc) ** 2)

        ifft_lpf = np.fft.ifft(fft_lpf)
        for i in range(len(filtered_sound_val[ch])):
            filtered_sound_val[ch][i] = int(np.abs(ifft_lpf[i]))

    return create_wave(wave, filtered_sound_val)
