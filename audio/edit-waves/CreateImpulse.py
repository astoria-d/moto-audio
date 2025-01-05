
import os.path
import argparse

from WaveCore import write_wave
from WaveCore import display_plots

from WaveCore import FmtSubchunk
from WaveCore import DataSubchunk
from WaveCore import WaveData


def main():
    parser = argparse.ArgumentParser(description='create .wav file')
    parser.add_argument('file_name', help='.wav file name')
    parser.add_argument('-p', '--period', type=float, help='audio period (default is 3 seconds)', default=3)

    args = parser.parse_args()

    out_fname = args.file_name
    if (os.path.exists(out_fname)):
        print("[" + out_fname + "] already exists. removing it.")
        os.remove(out_fname)

    # stereo
    num_channel = 2
    # standard 44100
    sample_rate = 44100
    # standard 16 bit
    bits_per_sample = 16

    # sample_rate * num_channel * bits_per_sample / 8
    byte_rate = int(sample_rate * num_channel * bits_per_sample / 8)
    # num_channel * bits_per_sample / 8
    block_align = 4

    # data
    sub_chunk2_size = int(args.period * sample_rate * num_channel * bits_per_sample / 8)

    num_samples = int(sub_chunk2_size / num_channel / bits_per_sample * 8)
    audio_data = [[0] * num_samples] * num_channel

    for ch in range(num_channel):
        audio_data[ch][0] = 32767

    fmt = FmtSubchunk()
    fmt.subchunk_id = "fmt "
    fmt.sub_chunk_size = 16
    fmt.audio_format = 1
    fmt.num_channel = num_channel
    fmt.sample_rate = sample_rate
    fmt.byte_rate = byte_rate
    fmt.block_align = block_align
    fmt.bits_per_sample = bits_per_sample

    wdata = DataSubchunk()
    wdata.subchunk_id = "data"
    wdata.sub_chunk_size = sub_chunk2_size
    wdata.audio_data = audio_data

    wave_file_data = WaveData()
    wave_file_data.chunk_id = "RIFF"
    wave_file_data.chunk_size = 36 + sub_chunk2_size
    wave_file_data.format = "WAVE"
    wave_file_data.fmt = fmt
    wave_file_data.data = wdata

    wav_file = open(out_fname, "wb")
    write_wave(wav_file, wave_file_data)
    wav_file.close()

    display_plots(wave_file_data)

if __name__ == "__main__":
    main()
