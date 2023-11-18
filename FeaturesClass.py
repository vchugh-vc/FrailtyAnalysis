import pandas as pd
import numpy
import matplotlib.pyplot as plt
from scipy import signal

SAMPLE_FREQ = 130

class Features():

    def __init__(self, RawData, status, name):
        self.var_data = None
        self.std_data = None
        self.rms_data = None
        self.name = name
        self.status = status
        self.RawData = RawData
        self.AccelData = []
        self.ButterData = []
        self.max_data = None
        self.min_data = None
        self.minmax_data = None
        self.peak_data = None
        if self.status == 'raw':
            self.filtration()
        self.spread_stats()
        self.length = len(self.AccelData)
        self.minmax()

    def filtration(self):
        sos = signal.butter(1, 0.25, 'hp', fs=SAMPLE_FREQ, output='sos')
        self.ButterData = signal.sosfilt(sos, self.RawData)
        self.AccelData = self.ButterData[300:]


    def spread_stats(self):
        self.rms_data = numpy.sqrt(numpy.mean(self.AccelData ** 2))
        self.std_data = numpy.std(self.AccelData)
        self.var_data = numpy.var(self.AccelData)
        print(f"{self.name} | RMS = {self.rms_data} | STD = {self.std_data} | VAR = {self.var_data}")

    def minmax(self):
        self.max_data = max(self.AccelData)
        self.min_data = min(self.AccelData)
        self.minmax_data = self.max_data - self.min_data
        self.peak_data = max(self.max_data, -self.min_data)
        print(f"{self.name} | Min = {self.min_data} | Max = {self.max_data} | MinMax = {self.minmax_data} | Peak = {self.peak_data}")


