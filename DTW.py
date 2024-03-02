# https://github.com/talcs/simpledtw

import pandas as pd
import os
import matplotlib.pyplot as plt
import numpy
from FeatureClass import DataPreparation
import scipy.signal as signal

from dtaidistance import dtw

# DataFeatures = Features(FilteredData)
#
# AccZ = DataFeatures.AccZ
# AccY = DataFeatures.AccY
# AccX = DataFeatures.AccX

# IMUFile = "EdgeData/Up-Mid-Stable-2.csv"

SAMPLE_FREQ = 104


class DataTimeWarping:

    def __init__(self, AccZ, AccX):

        self.lifting_up_peak = None
        self.pour_start = None
        self.lifting_down_peak = None
        self.movement_stamps = None
        self.DTW_up_end = None
        self.down_start = None
        self.AccZ = AccZ
        self.AccX = AccX
        self.trimmed_axis = numpy.arange(0, len(self.AccZ) / SAMPLE_FREQ,
                                         1 / SAMPLE_FREQ)

        # self.DTWDown()
        # self.DTWDown2()
        self.PhaseUp()
        self.Down_Peaks()
        self.movement_stamps
        self.walking_filter()
        self.movement_phases()


    def DTWGeneral(self):  # DTW Comparing an entire signal against pre-recorded signals and return the best fit
        minimum = 100
        name = 0

        for i in os.listdir('EdgeData'):
            df = pd.read_csv(f"EdgeData/{i}")
            DTWAccZ = df['accZ']
            distance = dtw.distance(self.AccZ, DTWAccZ)
            print(f"DTW Distance: {distance}")
            if distance <= minimum:
                minimum = distance
            name = i

        print(f"Closest File was {name}")

    def DTWUpFast(self):  # Compares a known lifting signal to different intervals of a movement

        # IMUFile = "EdgeData/Up-Mid-Stable-2.csv" IMU File for Mug
        IMUFile = "KettleData/Up-Mid-1.csv"
        df = pd.read_csv(IMUFile)
        DTWAccZ = df['accZ']

        i = 100
        minimum = 100
        data_range = 0
        while i < 300:
            distance = dtw.distance(self.AccZ[0:i], DTWAccZ)
            # print(f"From 0:{i}, the distance is {distance}")
            if distance <= minimum:
                minimum = distance
                data_range = i
            i += 30

        print(f"Up Fast: From {data_range}, the distance is {distance}")

        self.Up_Peaks()
        plt.suptitle('Lifting Graph (Fast)')
        print(data_range)
        plt.plot(DTWAccZ, label='DTW')
        plt.plot(self.AccZ[0:data_range], label='IMU')
        plt.legend()
        plt.show()

        return [data_range, minimum]

    def DTWUpSlow(self):  # Compares a known lifting signal to different intervals of a movement

        # IMUFile = "EdgeData/Up-Mid-Stable-2.csv" IMU File for Mug
        IMUFile = "KettleData/Up-Slow-1.csv"
        df = pd.read_csv(IMUFile)
        DTWAccZ = df['accZ']

        i = 100
        minimum = 100
        data_range = 0
        while i < 300:
            distance = dtw.distance(self.AccZ[0:i], DTWAccZ)
            # print(f"From 0:{i}, the distance is {distance}")
            if distance <= minimum:
                minimum = distance
                data_range = i
            i += 30

        print(f"Up Slow: From {data_range}, the distance is {distance}")

        plt.suptitle('Lifting Graph (Slow)')
        print(data_range)
        plt.plot(DTWAccZ, label='DTW')
        plt.plot(self.AccZ[0:data_range], label='IMU')
        plt.legend()
        plt.show()

        return [data_range, minimum]

    def Up_Peaks(self, start_range=200):

        lifting_up_peak = signal.find_peaks(self.AccZ[0:start_range], prominence=0.05, height=0.02)
        lifting_down_peak = signal.find_peaks(-self.AccZ[0:start_range], prominence=0.05)
        j = 0.04
        while len(lifting_up_peak[0]) < 1:
            lifting_up_peak = signal.find_peaks(self.AccZ[0:start_range], prominence=j, height=0.02)
            j = j - 0.01

        k = 0.04
        while len(lifting_down_peak[0]) < 1:
            lifting_down_peak = signal.find_peaks(-self.AccZ[0:start_range], prominence=k)
            k = k - 0.01

        print(f"Scipy Peak of {lifting_up_peak}")
        print(f"Scipy Peak Down of {lifting_down_peak}")
        prom = 0
        for i in range(len(lifting_up_peak[1]['prominences'])):
            if lifting_up_peak[1]['prominences'][i] >= prom:
                prom = lifting_up_peak[1]['prominences'][i]
                location = lifting_up_peak[0][i]
        self.lifting_up_peak = location

        print(f"UP3: Main Up Peak at {location} with Prom = {prom}")

        prom = 0
        for i in range(len(lifting_down_peak[1]['prominences'])):
            if lifting_down_peak[1]['prominences'][i] >= prom:
                prom = lifting_down_peak[1]['prominences'][i]
                location = lifting_down_peak[0][i]

        print(f"UP3: Main Down Peak at {location} with Prom = {prom}")
        self.lifting_down_peak = location

    def PhaseUp(self):

        fast = self.DTWUpFast()
        slow = self.DTWUpSlow()
        self.Up_Peaks()

        if fast[1] <= slow[1]:
            self.DTW_up_end = fast[0]
            print("Fast")
        else:
            self.DTW_up_end = slow[0]
            print("Slow")
        print(f"DTW UP End: {self.DTW_up_end}")

        if self.lifting_down_peak < self.lifting_up_peak:
            print(f"Rerunning Peaks Algorithm")
            self.Up_Peaks(start_range=250)


        if self.lifting_down_peak > self.DTW_up_end:
            self.DTW_up_end = self.lifting_down_peak + 10

    def DTWDown(self):  # Compares a known down signal to different intervals of a movement

        IMUFile = "EdgeData/Down-Slow-Stable-2.csv"
        df = pd.read_csv(IMUFile)
        DTWAccZ = df['accZ']

        i = 50
        minimum = 100
        data_range = 0
        while i < 500:
            distance = dtw.distance(self.AccZ[-i:], DTWAccZ)
            # print(f"From 0-{i}, the distance is {distance}")
            if distance <= minimum:
                minimum = distance
                data_range = i
            i += 30

        print(f"From {data_range}, the distance is {distance}")

        plt.suptitle('Putting Down Graph')
        print(data_range)
        plt.plot(DTWAccZ, label='DTW')
        plt.plot(self.AccZ[-data_range:], label='IMU')
        plt.legend()
        plt.show()

        self.down_start = len(self.AccZ) - data_range

    def DTWDown2(self):  # Detects putting down motion based on peak caused by impact with a surface

        peak = numpy.max(self.AccZ[-200:])
        print(peak)
        # max_time = numpy.where(self.AccZ[-200:] == peak)[0]
        max_time = numpy.argmax(self.AccZ[-100:])
        print(max_time)
        data_range = 110 - max_time.item()
        plt.suptitle('Putting Down Graph')
        print(data_range)
        self.down_start = len(self.AccZ) - data_range

        plt.plot(self.AccZ[self.down_start:], label='IMU')
        plt.legend()
        plt.show()

    def Down_Peaks(self):

        up_peak = signal.find_peaks(self.AccZ[-200:], height=0.01, prominence=0.1)
        # prom = signal.peak_prominences(self.AccZ[-200:], up_peak[0])
        print(f"Put down peak at {up_peak}")
        print(f"{up_peak[0][0]} at {up_peak[1]['peak_heights'][0]}")

        prom = 0
        for i in range(len(up_peak[1]['prominences'])):
            if up_peak[1]['prominences'][i] >= prom:
                prom = up_peak[1]['prominences'][i]
                peak_location = up_peak[0][i]

        print(f"UP3: Main Up Peak at {peak_location} with Prom = {prom}")

        location = len(self.AccZ) - (210 - peak_location)
        print(location)
        self.down_start = location
        # print(f"Prominences {prom}")
        plt.suptitle('Putting Down Graph')
        plt.plot(self.AccZ[self.down_start:], label='IMU')
        plt.legend()
        plt.show()

    def walking_filter(self):

        i = 20
        while i <= 300:
            Zgrad = numpy.gradient(self.AccZ[self.DTW_up_end + i:self.DTW_up_end + 20 + i])
            Zgradient = numpy.mean(Zgrad) * 10000
            Xgrad = numpy.gradient(self.AccX[self.DTW_up_end:self.DTW_up_end + i])
            Xgradient = numpy.mean(Xgrad) * 10000
            print(f"{self.DTW_up_end + i}:  X Grad {Xgradient} & Z Grad {Zgradient}")
            i = i + 10

        self.pour_start = self.DTW_up_end + 50

    def movement_phases(self):

        # plt.plot(AccX[self.up_end:self.down_start])
        # plt.plot(AccY[self.up_end:self.down_start])
        # plt.plot(AccZ[self.up_end:self.down_start])
        # plt.show()

        self.movement_stamps = [0, self.DTW_up_end, self.pour_start, self.down_start, len(self.AccZ)]

        for point in self.movement_stamps:
            plt.axvline(x=point, color='r', linestyle='--', label=f'x = {point}')

        plt.plot(self.AccZ)
        plt.show()

        # for i in range(len(self.movement_stamps) - 1):
        #     print(f"{self.movement_stamps[i]} and {self.movement_stamps[i + 1]}")

        print(self.movement_stamps)
