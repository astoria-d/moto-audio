import sys
import os.path

from WaveCore import parse_wav_file
from WaveCore import concat_wave
from WaveCore import write_wave
from WaveCore import display_plots

def print_usage():
    print(sys.argv[0] + ": <input .wav file1> <input .wav file2> <output .wav>")

def main():
#    print(sys.argv[0])

    if (len(sys.argv) != 4):
        print_usage()
        sys.exit(100)

    in_fname1 = sys.argv[1]
    if (not os.path.exists(in_fname1)):
        print("[" + in_fname1 + "] not found.")
        sys.exit(101)

    in_fname2 = sys.argv[2]
    if (not os.path.exists(in_fname2)):
        print("[" + in_fname2 + "] not found.")
        sys.exit(101)

    out_fname = sys.argv[3]
    if (os.path.exists(out_fname)):
        print("[" + out_fname + "] already exists. removing it.")
        os.remove(out_fname)

    wav_file1 = open(in_fname1, "rb")
    wav_file2 = open(in_fname2, "rb")
    out_file = open(out_fname, "wb")

    wav1 = parse_wav_file(wav_file1)

    wav2 = parse_wav_file(wav_file2)

    out_wave = concat_wave(wav1, wav2)

    display_plots(out_wave)

    write_wave(out_file, out_wave)

    wav_file1.close()
    wav_file2.close()
    out_file.close()

if __name__ == "__main__":
    main()
