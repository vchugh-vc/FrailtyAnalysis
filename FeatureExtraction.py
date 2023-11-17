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


def filteration():
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


filtered_signals = filteration()
AccX = filtered_signals[0]
AccY = filtered_signals[1]
AccZ = filtered_signals[2]


def SignalMagnitudeVector():
    signal_sum = pow(AccX, 2) + pow(AccY, 2) + pow(AccZ, 2)
    smv = numpy.sqrt(signal_sum)
    plt.subplot(4, 1, 4)
    plt.plot(x_time, smv, label='filtered')
    plt.legend()
    plt.xlim(2)
    plt.show()
    return smv


smv_data = SignalMagnitudeVector()
print(smv_data)
