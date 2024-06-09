from FeatureClass import DataPreparation, Features
import pandas as pd
import numpy
from scipy import signal

from DTW import DataTimeWarping
from FrailtyIndex import Frailty
import matplotlib.pyplot as plt

SAMPLE_TIME = 0.0096
SAMPLE_FREQ = 104



# df = pd.read_csv(FILE)
# x = df['AccX']
# y = df['AccY']
# z = df['AccZ']
#
# x_axis = len(x[500:])
# time_array = numpy.arange(x_axis) / 104
#
# plt.title('Raw Pouring Movement Graph')
# plt.plot(time_array, x[500:], label='X')
# plt.plot(time_array, y[500:], label='Y')
# plt.plot(time_array, z[500:], label='Z')
# plt.xlabel('Time (seconds)')
# plt.ylabel('Acceleration (g)')
# plt.legend()
# plt.show()

FILE = ('IMUData.csv')
DEMO = ('LongitudinalData/2024-03-29 18:22:48-T6.csv')

FilteredData = DataPreparation(file=DEMO)
AccZ = FilteredData.AccZ_Trimmed
AccX = FilteredData.AccX_Trimmed
DTWPhases = DataTimeWarping(AccZ, AccX)
TimeStamps = DTWPhases.movement_stamps
# TimeStamps = [0, 97, 107, 147, 167, 902, 1100]
up_data = Features(FilteredData, TimeStamps, 'up')
middle_data = Features(FilteredData, TimeStamps, 'middle')
Frailty(up_data, middle_data)




