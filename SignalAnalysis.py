from FeatureClass import DataPreparation, Features
import pandas as pd
import numpy
from scipy import signal

from DTW import DataTimeWarping
from FrailtyIndex import Frailty
import matplotlib.pyplot as plt

SAMPLE_TIME = 0.0096
SAMPLE_FREQ = 104

FILE = ('Graph.csv')



df = pd.read_csv(FILE)
x = df['AccX']
y = df['AccY']
z = df['AccZ']

x_axis = len(x[500:])
time_array = numpy.arange(x_axis) / 104

plt.title('Raw Pouring Movement Graph')
plt.plot(time_array, x[500:], label='X')
plt.plot(time_array, y[500:], label='Y')
plt.plot(time_array, z[500:], label='Z')
plt.xlabel('Time (seconds)')
plt.ylabel('Acceleration (g)')
plt.legend()
plt.show()

# FilteredData = DataPreparation(file=FILE)
# AccZ = FilteredData.AccZ_Trimmed
# AccX = FilteredData.AccX_Trimmed
# DTWPhases = DataTimeWarping(AccZ, AccX)
# TimeStamps = DTWPhases.movement_stamps
# # TimeStamps = [0, 97, 107, 147, 167, 902, 1100]
# up_data = Features(FilteredData, TimeStamps, 'up')
# middle_data = Features(FilteredData, TimeStamps, 'middle')
# Frailty(up_data, middle_data)


def ButterFilter(RawData):  # Butterworth Function Filter to remove gravity
    sos = signal.butter(1, 0.25, 'hp', fs=SAMPLE_FREQ, output='sos')
    ButterData = signal.sosfilt(sos, RawData)
    return ButterData[500:]

xb = ButterFilter(x)
yb = ButterFilter(y)
zb = ButterFilter(z)
plt.title('Filtered Pouring Movement Graph')
plt.plot(time_array, xb, label='X')
plt.plot(time_array, yb, label='Y')
plt.plot(time_array, zb, label='Z')
plt.xlabel('Time (seconds)')
plt.ylabel('Acceleration (g)')
plt.legend()
plt.show()

# Jerk = DataFeatures.Jerk
# AccX = DataFeatures.AccX
# AccY = DataFeatures.AccY
# AccZ = DataFeatures.AccZ
# Jerk_RMS = numpy.sqrt(numpy.mean(Jerk ** 2))
# print(f"Average Jerk of Movement: {Jerk_RMS} m/s-3")
# print(f"Length of movemenet {len(Jerk)} at {DataFeatures.time}")
# print(f"Dominant Freq is {DataFeatures.FFTFreq}")


# new = butter_lowpass_filter(FilteredData.AccZ_Trimmed, 10, 104, 2)
# plt.subplot(2, 1, 1)
# plt.plot(FilteredData.AccZ_Trimmed)
# plt.subplot(2, 1, 2)
# plt.plot(new)
# plt.show()


def minmax_spread(array):  # Returns Min-Max Data of an Array
    max_data = max(array)
    min_data = min(array)
    minmax_data = max_data - min_data
    peak_data = max(max_data, min_data)
    rms_data = numpy.sqrt(numpy.mean(array ** 2))
    std_data = numpy.nanstd(array)
    var_data = numpy.nanvar(array)
    print(
        f"Max: {max_data}, Min: {min_data}, Range : {minmax_data}, Peak {peak_data}, RMS {rms_data}, STD {std_data}, Var {var_data}")

