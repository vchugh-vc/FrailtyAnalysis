import pandas as pd
import numpy
import matplotlib.pyplot as plt
from scipy import signal

SAMPLE_FREQ = 130

DT = 0.007


class Features:

    def __init__(self, RawData, status, name):
        self.var_data = None  # Variance of Array
        self.std_data = None  # Standard Deviation of Array
        self.rms_data = None  # RMS of Array
        self.name = name  # Name Label (Printing)
        self.status = status  # Status on Filtered or Raw Data
        self.RawData = RawData  # Raw IMU Data
        self.ProcessedData = []  # Butterworth Data (without settle time data
        self.max_data = None  # Max Value of Array
        self.min_data = None  # Min Value of Array
        self.minmax_data = None  # Min-Max of Array
        self.peak_data = None  # Peak of Array
        self.jerk_data = []
        if self.status == 'raw':  # If raw data (from IMU) filter through Butterworth Filter
            self.filtration()
        else:
            self.ProcessedData = self.RawData
        self.jerk_calc()
        self.length = len(self.ProcessedData)
        self.window_array = []  # Array for Sliding Windows
        self.window_stat_data = [[], [], [], []] # Array for Stat Data [Max, Min, MinMax, Peak]
        self.window_spread_data = [[],[],[]] # Array for Spread Data [RMS, STD, VAR]
        self.x_time_filtered = numpy.arange(0, self.length / SAMPLE_FREQ,
                                            1 / SAMPLE_FREQ)  # X Axis (time for Acceleration Data)
        self.x_time_window = [] # X Axis (time for Windowed Data Analysis)

    def filtration(self):  # Butterworth Function Filter
        sos = signal.butter(1, 0.25, 'hp', fs=SAMPLE_FREQ, output='sos')
        ButterData = signal.sosfilt(sos, self.RawData)
        self.ProcessedData = ButterData[300:]

    def spread_stats(self, array):  # Returns RMS, STD, VAR of an Array
        self.rms_data = numpy.sqrt(numpy.mean(array ** 2))
        self.std_data = numpy.std(array)
        self.var_data = numpy.var(array)
        print(f"{self.name} | RMS = {self.rms_data} | STD = {self.std_data} | VAR = {self.var_data}")

        return [self.rms_data, self.std_data, self.var_data]

    def minmax(self,array):   # Returns Min-Max Data of an Array
        self.max_data = max(array)
        self.min_data = min(array)
        self.minmax_data = self.max_data - self.min_data
        self.peak_data = max(self.max_data, -self.min_data)
        print(
            f"{self.name} | Min = {self.min_data} | Max = {self.max_data} | MinMax = {self.minmax_data} | Peak = {self.peak_data}")

        return [self.max_data, self.min_data, self.minmax_data, self.peak_data]

    def sliding_windows(self):  # Creates Sliding Windows from Filtered and Sliced Array
        i = 0
        while i < len(self.ProcessedData):
            window_small = self.ProcessedData[i:i + 100]
            self.window_array.append(window_small)
            i += 50

        for i in self.window_array:
            stat = self.minmax(i)
            self.window_stat_data[0].append(stat[0]) # Max Data of Windowed Array
            self.window_stat_data[1].append(stat[1]) # Min Data of Windowed Array
            self.window_stat_data[2].append(stat[2]) # MinMax Data of Windowed Array
            self.window_stat_data[3].append(stat[3]) # Peak Data of Windowed Array
            spread = self.spread_stats(i)
            self.window_spread_data[0].append(spread[0]) # RMS of Windowed Array
            self.window_spread_data[1].append(spread[1])  # STD of Windowed Array
            self.window_spread_data[2].append(spread[2])  # VAR of Windowed Array

        self.x_time_window = numpy.arange(0, self.length / SAMPLE_FREQ,
                                          (self.length / SAMPLE_FREQ) / len(
                                              self.window_array))  # X Axis (time for Acceleration Data)
        self.Stat_graph()
        self.Spread_graph()



    def jerk_calc(self):
        self.jerk_data = numpy.gradient(self.ProcessedData, DT)

    def Accel_Graph(self):
        plt.subplot(3, 1, 1)
        plt.plot(self.x_time_filtered, self.ProcessedData, label=f"{self.name}")
        plt.legend()
        plt.xlabel("Time (s)")
        plt.title("Acceleration on Different Axis")
        plt.ylabel("Acceleration (g)")

    def SMV_Graph(self):
        plt.subplot(3, 1, 2)
        plt.plot(self.x_time_filtered, self.ProcessedData, label=f"{self.name}")
        plt.legend()
        plt.xlabel("Time (s)")
        plt.title("SMV")
        plt.ylabel("Acceleration (g)")

    def Stat_graph(self):
        plt.subplot(2, 1, 1)
        plt.plot(self.x_time_window, self.window_stat_data[0], label=f"{self.name} Max")
        plt.plot(self.x_time_window, self.window_stat_data[1], label=f"{self.name} Min")
        plt.plot(self.x_time_window, self.window_stat_data[2], label=f"{self.name} MinMax")
        plt.plot(self.x_time_window, self.window_stat_data[3], label=f"{self.name} Peak")
        plt.legend()
        plt.xlabel("Time (s)")
        plt.title("Stats of Windowed Data")
        plt.ylabel("Acceleration (g)")

    def Spread_graph(self):
        plt.subplot(2, 1, 2)
        plt.plot(self.x_time_window, self.window_spread_data[0], label=f"{self.name} RMS")
        plt.plot(self.x_time_window, self.window_spread_data[1], label=f"{self.name} STD")
        plt.plot(self.x_time_window, self.window_spread_data[2], label=f"{self.name} VAR")
        plt.legend()
        plt.xlabel("Time (s)")
        plt.title("Spread of Windowed Data")
        plt.ylabel("Acceleration (g)")
