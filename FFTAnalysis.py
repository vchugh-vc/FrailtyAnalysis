import pandas as pd
from numpy.fft import fft, fftfreq
import numpy
import matplotlib.pyplot as plt

filename = "IMUData.csv"

plt.rcParams["figure.autolayout"] = True
df = pd.read_csv(filename)
Pitch = df[df.columns[0]]
Roll = df[df.columns[1]]
print("Contents in csv file:")


sampling_freq = 250

# Plotter Function

def plotter(csv_data):
    x_time = numpy.arange(0, len(csv_data) / sampling_freq, 1 / sampling_freq)
    fft_out = fft(csv_data)
    fft_freq = fftfreq(len(fft_out), 1 / sampling_freq)

    x_freq = numpy.abs(fft_freq)
    y_fft = numpy.abs(fft_out)

    # Plotting IMU angle through Time
    plt.subplot(2, 1, 1)
    plt.plot(x_time, csv_data)
    plt.xlabel("Time (s)")
    plt.ylabel("Angle (°)")

    # Plotting Frequency Amplitude (FFT)
    plt.subplot(2, 1, 2)
    plt.plot(x_freq, y_fft, 'r')
    plt.xlabel("Frequency (Hz)")
    plt.ylabel("Frequency Amplitude")
    plt.xlim(right=20)
    plt.xlim(left=-1)

    # Prints the dominate frequency
    y_max = numpy.argmax(y_fft)
    x_max = x_freq[y_max]
    print(x_max)

    plt.show()


plotter(Pitch)
