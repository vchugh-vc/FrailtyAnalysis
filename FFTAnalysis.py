import pandas as pd
from numpy.fft import fft, fftfreq
import numpy
import matplotlib.pyplot as plt
from scipy import signal

filename = "IMUData.csv"

plt.rcParams["figure.autolayout"] = True
df = pd.read_csv(filename)
AccX = df[df.columns[6]]
AccY = df[df.columns[2]]
print("Contents in csv file:")


sampling_freq = 130
order = 6

# Plotter Function
x_time = numpy.arange(0, len(AccX) / sampling_freq, 1 / sampling_freq)


def plotter(csv_data):

    fft_out = fft(csv_data)
    fft_freq = fftfreq(len(fft_out), 1 / sampling_freq)

    x_freq = numpy.abs(fft_freq)
    y_fft = numpy.abs(fft_out)

    # Plotting IMU angle through Time
    plt.subplot(3, 1, 1)
    plt.plot(x_time, csv_data)
    plt.xlabel("Time (s)")
    plt.ylabel("Angle (°)")

    # Plotting Frequency Amplitude (FFT)
    plt.subplot(3, 1, 2)
    plt.plot(x_freq, y_fft, 'r')
    plt.xlabel("Frequency (Hz)")
    plt.ylabel("Frequency Amplitude")
    plt.xlim(right=20)
    plt.xlim(left=-1)

    # Prints the dominate frequency
    y_max = numpy.argmax(y_fft)
    x_max = x_freq[y_max]
    print(x_max)
    return x_max

def ButterFilter(RawData, freq):  # Butterworth Function Filter to remove gravity
    sos = signal.butter(1, freq/0.5, 'lp', fs=sampling_freq, output='sos')
    ButterData = signal.sosfilt(sos, RawData)
    return ButterData

def butter_lowpass(cutoff, fs, order=5):
    return signal.butter(order, cutoff, fs=fs, btype='low', analog=False)

def butter_lowpass_filter(data, cutoff, fs, order=5):
    b, a = butter_lowpass(cutoff, fs, order=order)
    y = signal.lfilter(b, a, data)
    return y

Freq = plotter(AccX)
# y = butter_lowpass_filter(AccX, 20, sampling_freq, 1)

# plt.subplot(3, 1, 3)
# plt.plot(x_time, AccX, label='data')
# plt.plot(x_time, y, label='filtered data')
# plt.xlabel('Time [sec]')
# plt.grid()
# plt.legend()
plt.show()








