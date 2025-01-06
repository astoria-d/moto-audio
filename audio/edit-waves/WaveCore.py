
import sys
import matplotlib.pyplot as plt


class FmtSubchunk:
    subchunk_id: str
    sub_chunk_size: int
    audio_format: int
    num_channel: int
    sample_rate: int
    byte_rate: int
    block_align: int
    bits_per_sample: int

    def __repr__(self):
        return f"<FmtSubchunk subchunk_id:{self.subchunk_id} sub_chunk_size:{self.sub_chunk_size} audio_format:{self.audio_format} num_channel:{self.num_channel} sample_rate:{self.sample_rate} byte_rate:{self.byte_rate} block_align:{self.block_align} bits_per_sample:{self.bits_per_sample}>"


class DataSubchunk:
    subchunk_id: str
    sub_chunk_size: int
    # [ch]x[sample]
    audio_data: [[]]

    def __repr__(self):
        def print_data(self):
            ret_str = f""
            ch = 0
            for ch_data in self.audio_data:
                ret_str += f"audio_data({ch}):{ch_data if len(ch_data) < 10 else ch_data[:10]}{'...' if len(ch_data) >= 10 else ''}({len(ch_data)}) "
                ch += 1
            return ret_str

        return f"<DataSubchunk subchunk_id:{self.subchunk_id} sub_chunk_size:{self.sub_chunk_size} {print_data(self)})>"


class WaveData:
    chunk_id: str
    chunk_size: int
    format: str
    fmt: FmtSubchunk
    data: DataSubchunk
    def __repr__(self):
        return f"<WaveData chunk_id:{self.chunk_id} chunk_size:{self.chunk_size} format:{self.format} fmt:{self.fmt} data:{self.data}>"



def write_wave(wav_file, wave: WaveData):

    def create_wave_header(wav_file, wave: WaveData):

        print('create_wave_header')

        if (wave.chunk_id != "RIFF"):
            print("invalid chunk_id")
            sys.exit(200)
        elif (wave.format != "WAVE"):
            print("invalid format")
            sys.exit(200)
        elif (wave.fmt.subchunk_id != "fmt "):
            print("invalid fmt chunk_id")
            sys.exit(200)
        elif (wave.fmt.audio_format != 1):
            print("invalid audio_format(PCM)")
            sys.exit(200)
        elif (wave.data.subchunk_id != "data"):
            print("invalid data chunk_id")
            sys.exit(200)


        num_channel = wave.fmt.num_channel
        sample_rate = wave.fmt.sample_rate
        bits_per_sample = wave.fmt.bits_per_sample
        audio_data_size = wave.data.sub_chunk_size

        num_samples = int(audio_data_size / num_channel / bits_per_sample * 8)

    #    print(wave)

        # RIFF
        chunk_id = 0x52494646
        # WAVE
        format = 0x57415645

        # fmt
        sub_chunk1_id = 0x666d7420
        sub_chunk1_size = wave.fmt.sub_chunk_size
        # 1: PCM
        audio_format = wave.fmt.audio_format

        # sample_rate * num_channel * bits_per_sample / 8
        byte_rate = int(sample_rate * num_channel * bits_per_sample / 8)
        # num_channel * bits_per_sample / 8
        block_align = wave.fmt.block_align

        # data
        sub_chunk2_id = 0x64617461
        sub_chunk2_size = int(num_samples * num_channel * bits_per_sample / 8)

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


    create_wave_header(wav_file, wave)

    num_channel = wave.fmt.num_channel
    bits_per_sample = wave.fmt.bits_per_sample

    audio_data_size = wave.data.sub_chunk_size
    num_samples = int(audio_data_size / num_channel / bits_per_sample * 8)

    bytes_per_sample = int(bits_per_sample / 8)

    for smp in range(num_samples):

        for ch in range(num_channel):

            suond_val = wave.data.audio_data[ch][smp]

#            print(f'smp: {smp} ch: {ch} suond_val:{suond_val}')

            wav_file.write(suond_val.to_bytes(bytes_per_sample, 'little', signed=True))




def display_plots(wave: WaveData):

    audio_data_size = wave.data.sub_chunk_size
    num_channel = wave.fmt.num_channel
    sample_rate = wave.fmt.sample_rate
    bits_per_sample = wave.fmt.bits_per_sample

    num_samples = int(audio_data_size / num_channel / bits_per_sample * 8)
    sample_period = 1000 / sample_rate

    t_arr = [0] * num_samples

    for t in range(num_samples):
        t_arr[t] = t * sample_period

    for ch in range(num_channel):
        plt.plot(t_arr, wave.data.audio_data[ch])

    plt.xlabel('time (ms)')
    plt.ylabel('audio')
    
    plt.title('LPCM')
    plt.show()


def add_wave(wave1: WaveData, wave2: WaveData):
    if wave1.fmt.sample_rate != wave2.fmt.sample_rate:
        raise Exception(f"sample rate didn't match. ({wave1.fmt.sample_rate}/{wave2.fmt.sample_rate})")
    elif wave1.fmt.bits_per_sample != wave2.fmt.bits_per_sample:
        raise Exception(f"bits per sample didn't match. ({wave1.fmt.bits_per_sample}/{wave2.fmt.bits_per_sample})")

    audio_data_size = max(wave1.data.sub_chunk_size, wave2.data.sub_chunk_size)
    num_channel = max(wave1.fmt.num_channel, wave2.fmt.num_channel)
    sample_rate = wave1.fmt.sample_rate
    bits_per_sample = wave1.fmt.bits_per_sample

    num_samples = int(audio_data_size / num_channel / bits_per_sample * 8)
    bytes_per_sample = int(bits_per_sample / 8)
    block_align = bytes_per_sample * num_channel

    added_sound_val = [[0] * num_samples] * num_channel

#    print(wave2)

    for ch in range(num_channel):

#        print("indx:" + str(indx))

        num_samples1 = len(wave1.data.audio_data[ch])
        num_samples2 = len(wave2.data.audio_data[ch])
        for smp in range(num_samples):

            wave1_val = 0
            wave2_val = 0

            if ch < wave1.fmt.num_channel:
                if smp < num_samples1:
                    wave1_val = wave1.data.audio_data[ch][smp]
            if ch < wave2.fmt.num_channel:
                if smp < num_samples2:
                    wave2_val = wave2.data.audio_data[ch][smp]

            added_val = wave1_val + wave2_val

#            added_bytes.extend(audio_arr[ch][indx].to_bytes(bytes_per_sample, byteorder='little', signed=True))
            added_sound_val[ch][smp] = added_val

    fmt = FmtSubchunk()
    fmt.subchunk_id = wave1.fmt.subchunk_id
    fmt.sub_chunk_size = wave1.fmt.sub_chunk_size
    fmt.audio_format = wave1.fmt.audio_format
    fmt.num_channel = num_channel
    fmt.sample_rate = sample_rate
    fmt.byte_rate = wave1.fmt.byte_rate
    fmt.block_align = block_align
    fmt.bits_per_sample = bits_per_sample

    wdata = DataSubchunk()
    wdata.subchunk_id = wave1.data.subchunk_id
    wdata.sub_chunk_size = audio_data_size
    wdata.audio_data = added_sound_val

    added_wave = WaveData()
    added_wave.chunk_id = wave1.chunk_id
    added_wave.chunk_size = 36 + audio_data_size
    added_wave.format = wave1.format
    added_wave.fmt = fmt
    added_wave.data = wdata

    return added_wave

def concat_wave(wave1: WaveData, wave2: WaveData):
    if wave1.fmt.sample_rate != wave2.fmt.sample_rate:
        raise Exception(f"sample rate didn't match. ({wave1.fmt.sample_rate}/{wave2.fmt.sample_rate})")
    elif wave1.fmt.bits_per_sample != wave2.fmt.bits_per_sample:
        raise Exception(f"bits per sample didn't match. ({wave1.fmt.bits_per_sample}/{wave2.fmt.bits_per_sample})")

    audio_data_size1 = wave1.data.sub_chunk_size
    audio_data_size2 = wave2.data.sub_chunk_size
    audio_data_size = audio_data_size1 + audio_data_size2
    num_channel = max(wave1.fmt.num_channel, wave2.fmt.num_channel)
    sample_rate = wave1.fmt.sample_rate
    bits_per_sample = wave1.fmt.bits_per_sample

    num_samples1 = int(audio_data_size1 / num_channel / bits_per_sample * 8)
    num_samples2 = int(audio_data_size2 / num_channel / bits_per_sample * 8)
    bytes_per_sample = int(bits_per_sample / 8)
    block_align = bytes_per_sample * num_channel

    added_sound_val = [[0] * (num_samples1 + num_samples2)] * num_channel

    for ch in range(num_channel):
        for smp in range(num_samples1):
            added_sound_val[ch][smp] = wave1.data.audio_data[ch][smp]
        for smp in range(num_samples2):
            added_sound_val[ch][num_samples1 + smp] = wave2.data.audio_data[ch][smp]

    fmt = FmtSubchunk()
    fmt.subchunk_id = wave1.fmt.subchunk_id
    fmt.sub_chunk_size = wave1.fmt.sub_chunk_size
    fmt.audio_format = wave1.fmt.audio_format
    fmt.num_channel = num_channel
    fmt.sample_rate = sample_rate
    fmt.byte_rate = wave1.fmt.byte_rate
    fmt.block_align = block_align
    fmt.bits_per_sample = bits_per_sample

    wdata = DataSubchunk()
    wdata.subchunk_id = wave1.data.subchunk_id
    wdata.sub_chunk_size = audio_data_size
    wdata.audio_data = added_sound_val

    added_wave = WaveData()
    added_wave.chunk_id = wave1.chunk_id
    added_wave.chunk_size = 36 + audio_data_size
    added_wave.format = wave1.format
    added_wave.fmt = fmt
    added_wave.data = wdata

    return added_wave


def mul_wave(wave1: WaveData, wave2: WaveData, divider: int = 32):
    if wave1.fmt.sample_rate != wave2.fmt.sample_rate:
        raise Exception(f"sample rate didn't match. ({wave1.fmt.sample_rate}/{wave2.fmt.sample_rate})")
    elif wave1.fmt.bits_per_sample != wave2.fmt.bits_per_sample:
        raise Exception(f"bits per sample didn't match. ({wave1.fmt.bits_per_sample}/{wave2.fmt.bits_per_sample})")

    audio_data_size = max(wave1.data.sub_chunk_size, wave2.data.sub_chunk_size)
    num_channel = max(wave1.fmt.num_channel, wave2.fmt.num_channel)
    sample_rate = wave1.fmt.sample_rate
    bits_per_sample = wave1.fmt.bits_per_sample

    num_samples = int(audio_data_size / num_channel / bits_per_sample * 8)
    bytes_per_sample = int(bits_per_sample / 8)
    block_align = bytes_per_sample * num_channel

    added_sound_val = [[0] * num_samples] * num_channel

    for ch in range(num_channel):
        for smp in range(num_samples):
            wave1_val = 0
            wave2_val = 0

            if ch < wave1.fmt.num_channel:
                if smp < num_samples:
                    wave1_val = wave1.data.audio_data[ch][smp]
            if ch < wave2.fmt.num_channel:
                if smp < num_samples:
                    wave2_val = wave2.data.audio_data[ch][smp]

            mul_val = wave1_val * wave2_val
            added_sound_val[ch][smp] = int((mul_val / divider))

    fmt = FmtSubchunk()
    fmt.subchunk_id = wave1.fmt.subchunk_id
    fmt.sub_chunk_size = wave1.fmt.sub_chunk_size
    fmt.audio_format = wave1.fmt.audio_format
    fmt.num_channel = num_channel
    fmt.sample_rate = sample_rate
    fmt.byte_rate = wave1.fmt.byte_rate
    fmt.block_align = block_align
    fmt.bits_per_sample = bits_per_sample

    wdata = DataSubchunk()
    wdata.subchunk_id = wave1.data.subchunk_id
    wdata.sub_chunk_size = audio_data_size
    wdata.audio_data = added_sound_val

    multiplied_wave = WaveData()
    multiplied_wave.chunk_id = wave1.chunk_id
    multiplied_wave.chunk_size = 36 + audio_data_size
    multiplied_wave.format = wave1.format
    multiplied_wave.fmt = fmt
    multiplied_wave.data = wdata

    return multiplied_wave

def split_wave(input_wave: WaveData, split_point: float) -> (WaveData, WaveData):
#    print(input_wave)

    split_point_index = int(split_point * input_wave.fmt.sample_rate)
    print("split_point_index:" + str(split_point_index))
    print("len1:" + str(len(input_wave.data.audio_data[0])))
    print("len2:" + str(len(input_wave.data.audio_data[0][0:split_point_index])))
    print("len3:" + str(len(input_wave.data.audio_data[0][split_point_index:])))
    wave1_data = [[]] * input_wave.fmt.num_channel
    wave2_data = [[]] * input_wave.fmt.num_channel
    for ch in range(input_wave.fmt.num_channel):
        wave1_data[ch] = input_wave.data.audio_data[ch][0:split_point_index]
        wave2_data[ch] = input_wave.data.audio_data[ch][split_point_index:]

    print("len2-:" + str(len(wave1_data[ch])))
    print("len3-:" + str(len(wave2_data[ch])))

    fmt = FmtSubchunk()
    fmt.subchunk_id = input_wave.fmt.subchunk_id
    fmt.sub_chunk_size = input_wave.fmt.sub_chunk_size
    fmt.audio_format = input_wave.fmt.audio_format
    fmt.num_channel = input_wave.fmt.num_channel
    fmt.sample_rate = input_wave.fmt.sample_rate
    fmt.byte_rate = input_wave.fmt.byte_rate
    fmt.block_align = input_wave.fmt.block_align
    fmt.bits_per_sample = input_wave.fmt.bits_per_sample

    wdata1 = DataSubchunk()
    wdata1.subchunk_id = input_wave.data.subchunk_id
    wdata1.sub_chunk_size = len(wave1_data[0]) * input_wave.fmt.bits_per_sample / 8 * input_wave.fmt.num_channel
    wdata1.audio_data = wave1_data

    wave1 = WaveData()
    wave1.chunk_id = input_wave.chunk_id
    wave1.chunk_size = 36 + wdata1.sub_chunk_size
    wave1.format = input_wave.format
    wave1.fmt = fmt
    wave1.data = wdata1

    wdata2 = DataSubchunk()
    wdata2.subchunk_id = input_wave.data.subchunk_id
    wdata2.sub_chunk_size = len(wave2_data[0]) * input_wave.fmt.bits_per_sample / 8 * input_wave.fmt.num_channel
    wdata2.audio_data = wave2_data

    wave2 = WaveData()
    wave2.chunk_id = input_wave.chunk_id
    wave2.chunk_size = 36 + wdata2.sub_chunk_size
    wave2.format = input_wave.format
    wave2.fmt = fmt
    wave2.data = wdata2

    return wave1, wave2

def parse_wav_file(wav_file) -> WaveData:
    data = wav_file.read()

    print('parse_wav_file')
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
    num_samples = int(sub_chunk2_size / num_channel / bits_per_sample * 8)
    bytes_per_sample = int(bits_per_sample / 8)

    raw_data = data[44:]
    audio_data = [[0] * num_samples] * num_channel

    for smp in range(0, sub_chunk2_size, block_align):

        indx = int(smp / block_align)

        for ch in range(num_channel):

            ref_indx = smp + ch * num_channel
            audio_data[ch][indx] = int.from_bytes(raw_data[ref_indx : ref_indx + bytes_per_sample], byteorder='little', signed=True)


    print("== data subchunk ==")
    print("sub_chunk2_id: " + hex(sub_chunk2_id))
    print("               " + sub_chunk2_str)
    print("sub_chunk2_size: " + str(sub_chunk2_size))

    if (sub_chunk2_str != "data"):
        print("invalid data subchunk")
        sys.exit(202)

    print("====")
    print("num samples: " + str(num_samples))
    print("data period {:.4f}(s): ".format(num_samples / sample_rate))

    fmt = FmtSubchunk()
    fmt.subchunk_id = sub_chunk1_str
    fmt.sub_chunk_size = sub_chunk1_size
    fmt.audio_format = audio_format
    fmt.num_channel = num_channel
    fmt.sample_rate = sample_rate
    fmt.byte_rate = byte_rate
    fmt.block_align = block_align
    fmt.bits_per_sample = bits_per_sample

    wdata = DataSubchunk()
    wdata.subchunk_id = sub_chunk2_str
    wdata.sub_chunk_size = sub_chunk2_size
    wdata.audio_data = audio_data

    wave_file_data = WaveData()
    wave_file_data.chunk_id = chunk_id_str
    wave_file_data.chunk_size = chunk_size
    wave_file_data.format = format_str
    wave_file_data.fmt = fmt
    wave_file_data.data = wdata

    return wave_file_data

