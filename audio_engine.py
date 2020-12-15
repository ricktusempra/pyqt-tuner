import sounddevice as sd
import soundfile as sf
import pyaudio
import numpy as np


sd.default.samplerate = 44100
sd.default.channels = 2

FRAME_SIZE = 2048
FRAMES_PER_FFT = 16
SAMPLES_PER_FFT = FRAME_SIZE * FRAMES_PER_FFT
FREQ_STEP = float(sd.default.samplerate) / SAMPLES_PER_FFT


def freq_to_number(f):
    return 69 + 12*np.log2(f/440.0)


def number_to_freq(n):
    return 440 * 2.0**((n-69)/12.0)


def note_to_fftbin(n):
    return number_to_freq(n)/FREQ_STEP


NOTE_MIN = 67  # 3 + 4 * 12  # 60 = c4
NOTE_MAX = 70  # 5 + 6 * 12  # 69 = a4
imin = max(0, int(np.floor(note_to_fftbin(NOTE_MIN-1))))
imax = min(SAMPLES_PER_FFT, int(np.ceil(note_to_fftbin(NOTE_MAX+1))))
window = 0.5 * (1 - np.cos(np.linspace(0, 2 * np.pi, SAMPLES_PER_FFT, False)))  # hanning window for signal

SENSIBILITY = 20000
TUNE_NOTE_NUM = []
TUNE_FREQ = []


def frequency():
    data = sd_stream_read()
    fft_from_data = np.fft.rfft(data * window)                                  # fourier transform of windowed data
    if np.average(np.abs(fft_from_data[imin:imax])) > SENSIBILITY:
        freq = (np.abs(fft_from_data[imin:imax]).argmax() + imin) * FREQ_STEP   # some black magic
        return freq
    else:
        return 0


def callback(indata, outdata, frames, time, status):
    if status:
        print(status)


def sd_stream_start():
    stream.start_stream()


def sd_stream_stop():
    stream.stop_stream()


def sd_stream_read():
    return np.fromstring(stream.read(SAMPLES_PER_FFT), np.int16)


def record_sample(slength):
    record = sd.rec(slength * sd.default.samplerate)
    return record


def play_sample(sample, wait=1):
    sd.play(sample)
    if wait:
        sd.wait()


def play_note(name, wait=0):
    data, samplerate = sf.read(name)
    play_sample(data, wait)


p = pyaudio.PyAudio()
stream = p.open(format=pyaudio.paInt16,
                channels=1,
                rate=sd.default.samplerate,
                input=True,
                frames_per_buffer=FRAME_SIZE,)


'''
 def frequency_spectrum(sample, samplerate):
    sample = sample - np.average(sample)
    size = len(sample)
    print(size)
    freqs_empty = np.arange(size)           # name??
    time_arr = size / float(samplerate)     # name??
    freq_arr = freqs_empty / float(time_arr)

    freq_arr = freq_arr[range(size // 2)]

    sample_fft = np.fft.fft(np.fft.rfft(sample))
    sample_fft = sample_fft[range(size // 2)]

    return freq_arr, abs(sample_fft)
# def frequency_plot(data, samplerate):

    y = data

    t = np.arange(len(y)) / float(samplerate)
    play_sample(y, 0)

    plt.plot(t, y)
    plt.xlabel('t')
    plt.ylabel('y')

    frq, s_fft = frequency_spectrum(y, samplerate)
    plt.subplot(2, 1, 2)
    plt.plot(frq, s_fft, 'b')
    plt.xlabel('Freq (Hz)')
    plt.ylabel('|X(freq)|')
    plt.tight_layout()
'''