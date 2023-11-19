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
        self.AccelData = []  # Butterworth Data (without settle time data
        self.max_data = None  # Max Value of Array
        self.min_data = None  # Min Value of Array
        self.minmax_data = None  # Min-Max of Array
        self.peak_data = None  # Peak of Array
        self.derivative = []
        if self.status == 'raw':  # If raw data (from IMU) filter through Butterworth Filter
            self.filtration()
        else:
            self.AccelData = self.RawData
        self.spread_stats()
        self.jerk_calc()
        self.length = len(self.AccelData)
        self.minmax()
        self.window_data = []  # Array for Sliding Windows Data
        self.sliding_windows()

    def filtration(self):  # Butterworth Function Filter
        sos = signal.butter(1, 0.25, 'hp', fs=SAMPLE_FREQ, output='sos')
        ButterData = signal.sosfilt(sos, self.RawData)
        self.AccelData = ButterData[300:]

    def spread_stats(self):  # Returns RMS, STD, VAR of an Array
        self.rms_data = numpy.sqrt(numpy.mean(self.AccelData ** 2))
        self.std_data = numpy.std(self.AccelData)
        self.var_data = numpy.var(self.AccelData)
        print(f"{self.name} | RMS = {self.rms_data} | STD = {self.std_data} | VAR = {self.var_data}")

    def minmax(self):   # Returns Min-Max Data of an Array
        self.max_data = max(self.AccelData)
        self.min_data = min(self.AccelData)
        self.minmax_data = self.max_data - self.min_data
        self.peak_data = max(self.max_data, -self.min_data)
        print(
            f"{self.name} | Min = {self.min_data} | Max = {self.max_data} | MinMax = {self.minmax_data} | Peak = {self.peak_data}")

    def sliding_windows(self):  # Creates Sliding Windows from Filtered and Sliced Array
        i = 0
        while i < len(self.AccelData):
            window_small = self.AccelData[i:i + 100]
            self.window_data.append(window_small)
            i += 50

        print(self.window_data)

    def jerk_calc(self):
        self.derivative = numpy.gradient(self.AccelData, DT)
