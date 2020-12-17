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
NOTE_MAX = 71  # 5 + 6 * 12  # 69 = a4
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


def set_tune_note(note):
    global NOTE_MIN
    global NOTE_MAX
    global imin
    global imax

    NOTE_MIN = note - 1
    NOTE_MAX = note + 1

    imin = max(0, int(np.floor(note_to_fftbin(NOTE_MIN - 1))))
    imax = min(SAMPLES_PER_FFT, int(np.ceil(note_to_fftbin(NOTE_MAX + 1))))


p = pyaudio.PyAudio()
stream = p.open(format=pyaudio.paInt16,
                channels=1,
                rate=sd.default.samplerate,
                input=True,
                frames_per_buffer=FRAME_SIZE,)
