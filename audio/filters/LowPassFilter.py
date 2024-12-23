
import sys
sys.path.append('../add-waves')

import os.path
import argparse


from WaveCore import parse_wav_file
from WaveCore import write_wave
from WaveCore import display_plots

from Filters import butter_worse_lpf
from Filters import rc_lpf
from Filters import rc_lpf_ftt


def print_usage():
    print(sys.argv[0] + ": <input .wav file1> <fc> <output .wav>")

def main():

    parser = argparse.ArgumentParser(description='apply low pass filter')
    parser.add_argument('in_file', help='input file name')
    parser.add_argument('out_file', help='output file name')
    parser.add_argument('-f', '--fc', help='cutoff frequency', type=int)
    parser.add_argument('-b', '--butterworse', help='use butterworse filter', action='store_true', default=False)
    args = parser.parse_args()

#    print(sys.argv[0])

    in_fname1 = args.in_file
    if (not os.path.exists(in_fname1)):
        print("[" + in_fname1 + "] not found.")
        sys.exit(101)

    fc = args.fc

    out_fname = args.out_file
    if (os.path.exists(out_fname)):
        print("[" + out_fname + "] already exists. removing it.")
        os.remove(out_fname)

    wav_file1 = open(in_fname1, "rb")
    out_file = open(out_fname, "wb")


    wav1 = parse_wav_file(wav_file1)

    if args.butterworse:
        out_wave = butter_worse_lpf(wav1, fc)
    else:
#        out_wave = rc_lpf_ftt(wav1, fc)
        out_wave = rc_lpf(wav1, fc)

#    display_plots(out_wave)

    write_wave(out_file, out_wave)

    wav_file1.close()
    out_file.close()

if __name__ == "__main__":
    main()
