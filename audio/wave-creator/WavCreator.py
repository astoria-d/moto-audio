
import sys
import os.path
import math
import argparse

def write_sin_waves(wav_file, data_period, num_channel, sample_rate, bits_per_sample, amps, freqs):

    print("==================='")
    print("create simple sin wave audio")
    print("amp: " + str(amps) + ", freq: " + str(freqs))

    num_samples = int(data_period * sample_rate)
    sample_period = 1 / sample_rate
    bytes_per_sample = int(bits_per_sample / 8)
    block_align = bytes_per_sample * num_channel

    if (len(amps) < len(freqs)):
        wave_num = len(amps)
    else:
        wave_num = len(freqs)

    print("num_samples:" + str(num_samples))

    for smp in range(num_samples):

        indx = int(smp / block_align)
#        print("smp:" + str(smp))
#        print("indx:" + str(indx))
        t = smp * sample_period

        for ch in range(num_channel):

            suond_val = 0
            for i in range(wave_num):
                suond_val += int(amps[i] * math.sin(2 * math.pi * freqs[i] * t))

            wav_file.write(suond_val.to_bytes(bytes_per_sample, 'little', signed=True))

#            print("  ch:" + str(ch) + ", t:" + str(t) + ", val: " + str(suond_val))

def write_sqare_wave(wav_file, data_period, num_channel, sample_rate, bits_per_sample, amp, freq):

    print("==================='")
    print("create square wave audio")
    print("amp: " + str(amp) + ", freq: " + str(freq))

    num_samples = int(data_period * sample_rate)
    bytes_per_sample = int(bits_per_sample / 8)

    print("num_samples:" + str(num_samples))

    for smp in range(num_samples):

        t = 1000000 * smp / sample_rate
        ft = 1000000 / freq
        n = int(t / ft)
        t_start = ft * n
        t_end = ft * (n + 1)
        t_half = (t_start + t_end) / 2
#        print("t: {0}, n: {1}, t_start: {2}, t_end: {3}".format(t, n, t_start, t_end))

        for ch in range(num_channel):
            if (t < t_half):
                suond_val = amp
            else:
                suond_val = -amp
            wav_file.write(suond_val.to_bytes(bytes_per_sample, 'little', signed=True))


def write_triangle_wave(wav_file, data_period, num_channel, sample_rate, bits_per_sample, amp, freq):

    print("==================='")
    print("create triangle wave audio")
    print("amp: " + str(amp) + ", freq: " + str(freq))

    num_samples = int(data_period * sample_rate)
    bytes_per_sample = int(bits_per_sample / 8)

    print("num_samples:" + str(num_samples))

    ft = 1000000 / freq
    slope = amp / ft
    for smp in range(num_samples):

        t = 1000000 * smp / sample_rate
        n = int(t / ft)
        t_start = ft * n
        t_end = ft * (n + 1)
        t_half = (t_start + t_end) / 2
        t_offset = t - t_half
#        print("t: {0}, n: {1}, t_start: {2}, t_end: {3}".format(t, n, t_start, t_end))

        for ch in range(num_channel):
            suond_val = slope * t_offset
            wav_file.write(int(suond_val).to_bytes(bytes_per_sample, 'little', signed=True))

def create_wave_header(wav_file, num_channel, sample_rate, bits_per_sample, data_period):
    print("data_period: " + str(data_period))

    # RIFF
    chunk_id = 0x52494646
    # WAVE
    format = 0x57415645

    sub_chunk1_id = 0x666d7420
    sub_chunk1_size = 16
    # 1: PCM
    audio_format = 1

    # sample_rate * num_channel * bits_per_sample / 8
    byte_rate = int(sample_rate * num_channel * bits_per_sample / 8)
    # num_channel * bits_per_sample / 8
    block_align = 4

    # data
    sub_chunk2_id = 0x64617461
    sub_chunk2_size = int(data_period * sample_rate * num_channel * bits_per_sample / 8)

    # total chunk size
    chunk_size = 36 + sub_chunk2_size

    print("== RIFF chunk ==")
    print("chunk_id: " + hex(chunk_id))
    print("chunk_size: " + str(chunk_size))
    print("format: " + hex(format))

    print("== fmt subchunk ==")
    print("sub_chunk1_id: " + hex(sub_chunk1_id))
    print("sub_chunk1_size: " + str(sub_chunk1_size))
    print("audio_format: " + str(audio_format))
    print("num_channel: " + str(num_channel))
    print("sample_rate: " + str(sample_rate))
    print("byte_rate: " + str(byte_rate))
    print("block_align: " + str(block_align))
    print("bits_per_sample: " + str(bits_per_sample))

    print("== data subchunk ==")
    print("sub_chunk2_id: " + hex(sub_chunk2_id))
    print("sub_chunk2_size: " + str(sub_chunk2_size))

    wav_file.write(chunk_id.to_bytes(4, 'big'))
    wav_file.write(chunk_size.to_bytes(4, 'little'))
    wav_file.write(format.to_bytes(4, 'big'))

    wav_file.write(sub_chunk1_id.to_bytes(4, 'big'))
    wav_file.write(sub_chunk1_size.to_bytes(4, 'little'))
    wav_file.write(audio_format.to_bytes(2, 'little'))
    wav_file.write(num_channel.to_bytes(2, 'little'))
    wav_file.write(sample_rate.to_bytes(4, 'little'))
    wav_file.write(byte_rate.to_bytes(4, 'little'))
    wav_file.write(block_align.to_bytes(2, 'little'))
    wav_file.write(bits_per_sample.to_bytes(2, 'little'))

    wav_file.write(sub_chunk2_id.to_bytes(4, 'big'))
    wav_file.write(sub_chunk2_size.to_bytes(4, 'little'))


def main():
#    print(sys.argv[0])

    parser = argparse.ArgumentParser(description='create .wav file')
    parser.add_argument('file_name', help='.wav file name')
    parser.add_argument('-t', '--type', type=int, help='wave file type, default is 0, 0: single sin wave, 1: 3 sin waves, 2: square wave, 3: triangle wave', default=0)
    parser.add_argument('-p', '--period', type=float, help='audio period (default is 3 seconds)', default=3)
    parser.add_argument('-f', '--freq', type=float, help='frequency (default is 440 Hz)', default=440)

    args = parser.parse_args()

    wav_fname = args.file_name
    if (os.path.exists(wav_fname)):
        print("[" + wav_fname + "] already exists. overwriting.")

    wav_file = open(wav_fname, "wb")

    # amplitude
    amp = 1000
    # stereo
    num_channel = 2
    # standard 44100
    sample_rate = 44100
    # standard 16 bit
    bits_per_sample = 16


    if (args.type == 0):
        # single sin wave audio
        amps = [amp]
        freqs = [args.freq]
        create_wave_header(wav_file, num_channel, sample_rate, bits_per_sample, args.period)
        write_sin_waves(wav_file, args.period, num_channel, sample_rate, bits_per_sample, amps, freqs)
    elif (args.type == 1):
        # 3 sin waves audio
        amps = [amp, amp * 2, amp * 3]
        freqs = [args.freq, args.freq * 2, args.freq * 3]
        create_wave_header(wav_file, num_channel, sample_rate, bits_per_sample, args.period)
        write_sin_waves(wav_file, args.period, num_channel, sample_rate, bits_per_sample, amps, freqs)
    elif (args.type == 2):
        # square wave audio
        create_wave_header(wav_file, num_channel, sample_rate, bits_per_sample, args.period)
        write_sqare_wave(wav_file, args.period, num_channel, sample_rate, bits_per_sample, amp, args.freq)
    elif (args.type == 3):
        # triangle wave audio
        amps = [amp, amp * 2, amp * 3]
        freqs = [args.freq, args.freq * 2, args.freq * 3]
        create_wave_header(wav_file, num_channel, sample_rate, bits_per_sample, args.period)
        write_triangle_wave(wav_file, args.period, num_channel, sample_rate, bits_per_sample, amp, args.freq)
    else:
        print("unknown type[" + str(args.type) + "]")
        parser.print_help()
        sys.exit(100)

    wav_file.close()

    print("[" + wav_fname + "] written.")

if __name__ == "__main__":
    main()
