import pandas as pd
import numpy
import matplotlib.pyplot as plt
from scipy import signal

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
print("Contents in csv file:")
sampling_freq = 130
x_time = numpy.arange(0, len(IMUAccY) / sampling_freq, 1 / sampling_freq)


def filtration():
    sos = signal.butter(1, 0.25, 'hp', fs=sampling_freq, output='sos')
    butter_x = signal.sosfilt(sos, IMUAccX)
    plt.subplot(4, 1, 1)
    plt.plot(x_time, butter_x, label='filtered')
    plt.plot(x_time, IMUAccX, label='original')
    plt.xlim(2)
    plt.legend()

    butter_y = signal.sosfilt(sos, IMUAccY)
    plt.subplot(4, 1, 2)
    plt.plot(x_time, butter_y, label='filtered')
    plt.plot(x_time, IMUAccY, label='original')
    plt.xlim(2)
    plt.legend()

    butter_z = signal.sosfilt(sos, IMUAccZ)
    plt.subplot(4, 1, 3)
    plt.plot(x_time, butter_z, label='filtered')
    plt.plot(x_time, IMUAccZ, label='original')
    plt.legend()
    plt.xlim(2)

    return [butter_x, butter_y, butter_z]


filtered_signals = filtration()
AccX = filtered_signals[0]
AccY = filtered_signals[1]
AccZ = filtered_signals[2]


def signal_magnitude_vector():
    signal_sum = pow(AccX, 2) + pow(AccY, 2) + pow(AccZ, 2)
    smv = numpy.sqrt(signal_sum)
    plt.subplot(4, 1, 4)
    plt.plot(x_time, smv, label='filtered')
    plt.legend()
    plt.xlim(2)
    plt.show()
    return smv


def minmax():
    max_x = max(AccX)
    min_x = min(AccX)
    minmax_x = max_x-min_x
    peak_x = max(max_x, -min_x)
    print(f"Acc. X | Min = {min_x} | Max = {max_x} | MinMax = {minmax_x} | Peak = {peak_x}")
    max_y = max(AccY)
    min_y = min(AccY)
    minmax_y = max_y - min_y
    peak_y = max(max_y, -min_y)
    print(f"Acc. Y | Min = {min_y} | Max = {max_y} | MinMax = {minmax_y} | Peak = {peak_y}")
    max_z = max(AccZ)
    min_z = min(AccZ)
    minmax_z = max_z - min_z
    peak_z = max(max_z, -min_z)
    print(f"Acc. Z | Min = {min_z} | Max = {max_z} | MinMax = {minmax_z} | Peak = {peak_z}")



minmax()
smv_data = signal_magnitude_vector()

