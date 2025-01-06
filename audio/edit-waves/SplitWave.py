import sys
import os.path

from WaveCore import parse_wav_file
from WaveCore import split_wave
from WaveCore import write_wave

def print_usage():
    print(sys.argv[0] + ": <input .wav file> <split point in second>")

def main():
#    print(sys.argv[0])

    if (len(sys.argv) != 3):
        print_usage()
        sys.exit(100)

    in_fname = sys.argv[1]
    if (not os.path.exists(in_fname)):
        print("[" + in_fname + "] not found.")
        sys.exit(101)

    split_point = float(sys.argv[2])

    wav_file = open(in_fname, "rb")
    wav_data = parse_wav_file(wav_file)
    wav_file.close()

    wav1, wav2 = split_wave(wav_data, split_point)

    print(wav_data)
    print(wav1)
    print(wav2)

    if (os.path.exists(in_fname + ".1")):
        print("[" + in_fname + ".1" + "] already exists. removing it.")
        os.remove(in_fname + ".1")

    out_file1 = open(in_fname + ".1", "wb")
    write_wave(out_file1, wav1)
    out_file1.close()

    if (os.path.exists(in_fname + ".2")):
        print("[" + in_fname + ".2" + "] already exists. removing it.")
        os.remove(in_fname + ".2")

    out_file2 = open(in_fname + ".2", "wb")
    write_wave(out_file2, wav2)
    out_file2.close()

if __name__ == "__main__":
    main()
