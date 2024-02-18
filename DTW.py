# https://github.com/talcs/simpledtw

import pandas as pd
import os
import matplotlib.pyplot as plt
import numpy
from FeatureClass import DataPreparation, Features

from dtaidistance import dtw

# FilteredData = DataPreparation()
# DataFeatures = Features(FilteredData)
#
# AccZ = DataFeatures.AccZ
# AccY = DataFeatures.AccY
# AccX = DataFeatures.AccX

IMUFile = "EdgeData/Up-Mid-Stable-2.csv"

SAMPLE_FREQ = 104


class DataTimeWarping:

    def __init__(self, signal):

        self.movement_stamps = None
        self.up_end = None
        self.down_start = None
        self.AccZ = signal
        self.trimmed_axis = numpy.arange(0, len(self.AccZ) / SAMPLE_FREQ,
                                         1 / SAMPLE_FREQ)
        self.DTWUp()
        self.DTWDown()
        self.movement_stamps
        self.movement_phases()

    def DTW1(self):  # DTW Comparing an entire signal against pre-recorded signals and return the best fit
        minimum = 100
        name = 0

        for i in os.listdir('EdgeData'):
            df = pd.read_csv(f"EdgeData/{i}")
            DTWAccZ = df['accZ']
            distance = dtw.distance(AccZ, DTWAccZ)
            print(f"DTW Distance: {distance}")
            if distance <= minimum:
                minimum = distance
            name = i

        print(f"Closest File was {name}")

    def DTWUp(self):  # Compares a known lifting signal to different intervals of a movement

        IMUFile = "EdgeData/Up-Mid-Stable-2.csv"
        df = pd.read_csv(IMUFile)
        DTWAccZ = df['accZ']

        i = 30
        minimum = 100
        data_range = 0
        while i < 200:
            distance = dtw.distance(self.AccZ[0:i], DTWAccZ)
            print(f"From 0:{i}, the distance is {distance}")
            if distance <= minimum:
                minimum = distance
                data_range = i
            i += 30

        plt.suptitle('Lifting Graph')
        print(data_range)
        plt.plot(DTWAccZ, label='DTW')
        plt.plot(self.AccZ[0:data_range], label='IMU')
        plt.legend()
        plt.show()

        self.up_end = data_range

    def DTWDown(self):  # Compares a known down signal to different intervals of a movement

        IMUFile = "EdgeData/Down-Slow-Stable-2.csv"
        df = pd.read_csv(IMUFile)
        DTWAccZ = df['accZ']

        i = 50
        minimum = 100
        data_range = 0
        while i < 500:
            distance = dtw.distance(self.AccZ[-i:], DTWAccZ)
            print(f"From 0-{i}, the distance is {distance}")
            if distance <= minimum:
                minimum = distance
                data_range = i
            i += 30

        plt.suptitle('Putting Down Graph')
        print(data_range)
        plt.plot(DTWAccZ, label='DTW')
        plt.plot(self.AccZ[-data_range:], label='IMU')
        plt.legend()
        plt.show()

        self.down_start = len(self.AccZ) - data_range

    def movement_phases(self):

        # plt.plot(AccX[self.up_end:self.down_start])
        # plt.plot(AccY[self.up_end:self.down_start])
        # plt.plot(AccZ[self.up_end:self.down_start])
        # plt.show()

        self.movement_stamps = [0, self.up_end, self.down_start, len(self.AccZ)]

        # for i in range(len(self.movement_stamps) - 1):
        #     print(f"{self.movement_stamps[i]} and {self.movement_stamps[i + 1]}")

        print(self.movement_stamps)

