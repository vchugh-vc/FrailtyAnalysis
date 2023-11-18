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
    plt.legend()

    butter_y = signal.sosfilt(sos, IMUAccY)
    plt.subplot(4, 1, 2)
    plt.plot(x_time, butter_y, label='filtered')
    plt.plot(x_time, IMUAccY, label='original')
    plt.legend()

    butter_z = signal.sosfilt(sos, IMUAccZ)
    plt.subplot(4, 1, 3)
    plt.plot(x_time, butter_z, label='filtered')
    plt.plot(x_time, IMUAccZ, label='original')
    plt.legend()


    return [butter_x, butter_y, butter_z]


filtered_signals = filtration()
AccX = filtered_signals[0][300:]
AccY = filtered_signals[1][300:]
AccZ = filtered_signals[2][300:]

x_time_filtered = numpy.arange(0, len(AccZ) / sampling_freq, 1 / sampling_freq)

def signal_magnitude_vector():
    signal_sum = pow(AccX, 2) + pow(AccY, 2) + pow(AccZ, 2)
    smv = numpy.sqrt(signal_sum)
    plt.subplot(4, 1, 4)
    plt.plot(x_time_filtered, smv, label='filtered')
    plt.legend()
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


def spread_stats():
    rms_x = numpy.sqrt(numpy.mean(AccX**2))
    std_x = numpy.std(AccX)
    var_x = numpy.var(AccX)
    print(f"Acc. X | RMS = {rms_x} | STD = {std_x} | VAR = {var_x}")
    rms_y = numpy.sqrt(numpy.mean(AccY ** 2))
    std_y = numpy.std(AccY)
    var_y = numpy.var(AccY)
    print(f"Acc. Y | RMS = {rms_y} | STD = {std_y} | VAR = {var_y}")
    rms_z = numpy.sqrt(numpy.mean(AccZ ** 2))
    std_z = numpy.std(AccZ)
    var_z = numpy.var(AccZ)
    print(f"Acc. Z | RMS = {rms_z} | STD = {std_z} | VAR = {var_z}")


def sliding_windows(data):

    window_data = []
    i = 0
    while i < len(data):
        print(data[i:i+100])
        window_small = data[i:i+100]
        window_data.append(window_small)
        i += 50

    print(len(window_data))

    return window_data


#minmax()
#spread_stats()
smv_data = signal_magnitude_vector()
window_smv = sliding_windows(smv_data)

