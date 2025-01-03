
import sys
sys.path.append('../../add-waves')

import os.path
import argparse

from WaveCore import write_wave
from WaveCore import display_plots

from WaveCore import FmtSubchunk
from WaveCore import DataSubchunk
from WaveCore import WaveData

from ModulationCore import encod_data

def main():
    parser = argparse.ArgumentParser(description='create .wav file')
    parser.add_argument('input_file', help='input data file name')
    parser.add_argument('output_name', help='encoded .wav file name')

    args = parser.parse_args()

    input_fname = args.input_file
    if (not os.path.exists(input_fname)):
        print("[" + input_fname + "] does not exist.")
        sys.exit(100)

    out_fname = args.output_name
    if (os.path.exists(out_fname)):
        print("[" + out_fname + "] already exists. removing it.")
        os.remove(out_fname)

    data_file = open(input_fname, "rb")
    in_data = data_file.read()
#    print(in_data)
    data_file.close()


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
    audio_data = encod_data(in_data, num_channel, sample_rate)
    data_chunk_size = int(len(audio_data[0]) * num_channel * bits_per_sample / 8)


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
    wdata.sub_chunk_size = data_chunk_size
    wdata.audio_data = audio_data

    wave_file_data = WaveData()
    wave_file_data.chunk_id = "RIFF"
    wave_file_data.chunk_size = 36 + data_chunk_size
    wave_file_data.format = "WAVE"
    wave_file_data.fmt = fmt
    wave_file_data.data = wdata

    print(wave_file_data)

    wav_file = open(out_fname, "wb")
    write_wave(wav_file, wave_file_data)
    wav_file.close()

    display_plots(wave_file_data)




if __name__ == "__main__":
    main()
