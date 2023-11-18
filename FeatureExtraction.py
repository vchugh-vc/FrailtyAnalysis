import pandas as pd
import numpy
import matplotlib.pyplot as plt
from FeaturesClass import Features

filename = "IMUData.csv"
plt.rcParams["figure.autolayout"] = True
df = pd.read_csv(filename)
print(df.columns)
IMUAccY = df['AccY']
IMUAccX = df['AccX']
IMUAccZ = df['AccZ']
GyroX = df['GyroX']
GyroY = df['GyroY']
GyroZ = df['GyroZ']
sampling_freq = 130

AccX = Features(IMUAccX, status="raw", name='AccX')
AccY = Features(IMUAccY, status="raw",name='AccY')
AccZ = Features(IMUAccZ, status="raw", name='AccZ')

x_time_filtered = numpy.arange(0, AccX.length / sampling_freq, 1 / sampling_freq)


def signal_magnitude_vector():
    signal_sum = pow(AccX.AccelData, 2) + pow(AccY.AccelData, 2) + pow(AccZ.AccelData, 2)
    smv_data = numpy.sqrt(signal_sum)
    plt.subplot(2, 1, 2)
    plt.plot(x_time_filtered, smv_data, label='filtered')
    plt.legend()
    plt.xlabel("Time (s)")
    plt.title("Signal Magnitude Vector")
    plt.ylabel("Acceleration (g)")




def sliding_windows(data):
    window_data = []
    i = 0
    while i < len(data):
        window_small = data[i:i + 100]
        window_data.append(window_small)
        i += 50

    return window_data

SMV = signal_magnitude_vector()

def grapher():
    plt.subplot(2, 1, 1)
    plt.plot(x_time_filtered, AccX.AccelData, label="AccX")
    plt.plot(x_time_filtered, AccY.AccelData, label="AccY")
    plt.plot(x_time_filtered, AccZ.AccelData, label="AccZ")
    plt.legend()
    plt.xlabel("Time (s)")
    plt.title("Acceleration on Different Axis")
    plt.ylabel("Acceleration (g)")
    plt.show()

grapher()

