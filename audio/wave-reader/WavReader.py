
import sys
import os.path
import matplotlib.pyplot as plt

def display_plots(audio_data, audio_data_size, num_channel, sample_rate, bits_per_sample):

    num_samples = int(audio_data_size / num_channel / bits_per_sample * 8)
    sample_period = 1000000 / sample_rate
    bytes_per_sample = int(bits_per_sample / 8)
    block_align = bytes_per_sample * num_channel

    t_arr = [0] * num_samples
#    print(audio_data[0:audio_data_size])
#    print("audio_data_size:" + str(audio_data_size))
#    print("num_samples:" + str(num_samples))

    audio_arr = [[0] * num_samples] * num_channel

    for t in range(num_samples):
        t_arr[t] = t * sample_period

    for smp in range(0, audio_data_size, block_align):

        indx = int(smp / block_align)
#        print("indx:" + str(indx))

        for ch in range(num_channel):

            ref_indx = smp + ch * num_channel
            audio_arr[ch][indx] = int.from_bytes(audio_data[ref_indx : ref_indx + bytes_per_sample], byteorder='little', signed=True)

#            print("  ch:" + str(ch) + ", ref_indx:" + str(ref_indx) + ", val: " + str(audio_arr[ch][indx]))

#                for bt in range(bytes_per_sample):
#                    print(smp + ch * num_channel + bt)


    for ch in range(num_channel):
        plt.plot(t_arr, audio_arr[ch])

    plt.xlabel('time')
    plt.ylabel('audio')
    
    plt.title('LPCM')
    plt.show()

def parse_wav_file(wav_file):
    data = wav_file.read()

#    print(type(data))
#    print(data[0:200])
#    print(data[4:8])

    chunk_id = int.from_bytes(data[0:4], byteorder='big')
    chunk_id_str = data[0:4].decode('utf-8')
    chunk_size = int.from_bytes(data[4:8], byteorder='little')
    format = int.from_bytes(data[8:12], byteorder='big')
    format_str = data[8:12].decode('utf-8')


    print("== RIFF chunk ==")
    print("chunk_id: " + hex(chunk_id))
    print("          " + chunk_id_str)
    print("chunk_size: " + str(chunk_size))
    print("format: " + hex(format))
    print("        " + format_str)

    if (chunk_id_str != "RIFF" or format_str != "WAVE"):
        print("invalid RIFF chunk")
        sys.exit(200)

    sub_chunk1_id = int.from_bytes(data[12:16], byteorder='big')
    sub_chunk1_str = data[12:16].decode('utf-8')
    sub_chunk1_size = int.from_bytes(data[16:20], byteorder='little')
    audio_format = int.from_bytes(data[20:22], byteorder='little')
    num_channel = int.from_bytes(data[22:24], byteorder='little')
    sample_rate = int.from_bytes(data[24:28], byteorder='little')
    byte_rate = int.from_bytes(data[28:32], byteorder='little')
    block_align = int.from_bytes(data[32:34], byteorder='little')
    bits_per_sample = int.from_bytes(data[34:36], byteorder='little')

    print("== fmt subchunk ==")
    print("sub_chunk1_id: " + hex(sub_chunk1_id))
    print("               " + sub_chunk1_str)
    print("sub_chunk1_size: " + str(sub_chunk1_size))
    print("audio_format: " + str(audio_format))
    print("num_channel: " + str(num_channel))
    print("sample_rate: " + str(sample_rate))
    print("byte_rate: " + str(byte_rate))
    print("block_align: " + str(block_align))
    print("bits_per_sample: " + str(bits_per_sample))

    if (sub_chunk1_str != "fmt "):
        print("invalid fmt subchunk")
        sys.exit(201)
    if (audio_format != 1):
        print("unknown audio format")
        sys.exit(202)
    if (sample_rate != 44100 and sample_rate != 48000):
        print("unknown sampling rate")
        sys.exit(203)
    if (byte_rate != (sample_rate * bits_per_sample * num_channel) / 8):
        print("invalid byte rate rate")
        sys.exit(204)
    if (block_align != num_channel * bits_per_sample / 8):
        print("invalid block align")
        sys.exit(205)

    sub_chunk2_id = int.from_bytes(data[36:40], byteorder='big')
    sub_chunk2_str = data[36:40].decode('utf-8')
    sub_chunk2_size = int.from_bytes(data[40:44], byteorder='little')
    audio_data = data[44:-1]

    print("== data subchunk ==")
    print("sub_chunk2_id: " + hex(sub_chunk2_id))
    print("               " + sub_chunk2_str)
    print("sub_chunk2_size: " + str(sub_chunk2_size))

    if (sub_chunk2_str != "data"):
        print("invalid data subchunk")
        sys.exit(202)

    print("====")
    num_samples = int(sub_chunk2_size / num_channel / bits_per_sample * 8)
    print("num samples: " + str(num_samples))
    print("data period {:.3f}(s): ".format(num_samples / sample_rate))

    display_plots(audio_data, sub_chunk2_size,
                  num_channel, sample_rate, bits_per_sample)

def print_usage():
    print(sys.argv[0] + ": <input .wav file>")

def main():
#    print(sys.argv[0])

    if (len(sys.argv) == 1):
        print_usage()
        sys.exit(100)

    wav_fname = sys.argv[1]
    if (not os.path.exists(wav_fname)):
        print("[" + wav_fname + "] not found.")
        sys.exit(101)

    wav_file = open(wav_fname, "rb")

    parse_wav_file(wav_file)

    wav_file.close()

if __name__ == "__main__":
    main()
