import sys
import os.path
import argparse

from WaveCore import parse_wav_file
from WaveCore import mul_wave
from WaveCore import write_wave
from WaveCore import display_plots

def print_usage():
    print(sys.argv[0] + ": <input .wav file1> <input .wav file2> <output .wav>")

def main():

    parser = argparse.ArgumentParser(prog=sys.argv[0])
    parser.add_argument('file1')
    parser.add_argument('file2')
    parser.add_argument('output')
    parser.add_argument('-d', '--divider', help='divide after multiply', type=int, default=32)
    args = parser.parse_args()

#    print(sys.argv[0])

    if (not os.path.exists(args.file1)):
        print("[" + args.file1 + "] not found.")
        sys.exit(101)

    if (not os.path.exists(args.file2)):
        print("[" + args.file2 + "] not found.")
        sys.exit(101)

    if (os.path.exists(args.output)):
        print("[" + args.output + "] already exists. removing it.")
        os.remove(args.output)

    wav_file1 = open(args.file1, "rb")
    wav_file2 = open(args.file2, "rb")
    out_file = open(args.output, "wb")

    wav1 = parse_wav_file(wav_file1)
    wav2 = parse_wav_file(wav_file2)
    out_wave = mul_wave(wav1, wav2, args.divider)

    display_plots(out_wave)
    write_wave(out_file, out_wave)

    wav_file1.close()
    wav_file2.close()
    out_file.close()

if __name__ == "__main__":
    main()
