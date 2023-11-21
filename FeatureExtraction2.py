import pandas as pd
import numpy
import matplotlib.pyplot as plt
from scipy import signal
from FeaturesClass import Features

filename = "IMUData.csv"
plt.rcParams["figure.autolayout"] = True
df = pd.read_csv(filename)
IMUAccY = df['AccY']
IMUAccX = df['AccX']
IMUAccZ = df['AccZ']
GyroX = df['GyroX']
GyroY = df['GyroY']
GyroZ = df['GyroZ']
SAMPLE_FREQ = 130

class DataPreparation:

    def __init__(self):
        self.AccX = self.ButterFilter(IMUAccX)
        self.AccY = self.ButterFilter(IMUAccY)
        self.AccZ = self.ButterFilter(IMUAccZ)
        self.SMV = self.SMV_Calc()
        self.SMV_roll = []
        self.FilteredLength = len(self.AccX)
        self.time_axis = numpy.arange(0, self.FilteredLength / SAMPLE_FREQ,
                                       1 / SAMPLE_FREQ)
        self.SMV_Window()
        self.rolling_axis = numpy.arange(0, self.FilteredLength / SAMPLE_FREQ,
                                          (self.FilteredLength / SAMPLE_FREQ) / len(
                                              self.SMV_roll))
        self.grapher()



    def ButterFilter(self, RawData):  # Butterworth Function Filter to remove gravity
        sos = signal.butter(1, 0.25, 'hp', fs=SAMPLE_FREQ, output='sos')
        ButterData = signal.sosfilt(sos, RawData)
        return ButterData[400:]

    def SMV_Calc(self): # Calculates SMV from Acceleratio Data
        signal_sum = pow(self.AccX, 2) + pow(self.AccY, 2) + pow(self.AccZ, 2)
        return numpy.sqrt(signal_sum)

    def grapher(self): # Graphs Acceleration and SMV

        plt.subplot(2, 1, 1)
        plt.plot(self.time_axis, self.AccX, label="X")
        plt.plot(self.time_axis, self.AccY, label="Y")
        plt.plot(self.time_axis, self.AccZ, label="Z")
        plt.legend()
        plt.subplot(2, 1, 2)
        plt.plot(self.time_axis, self.SMV, label='SMV')
        plt.plot(self.rolling_axis, self.SMV_roll, label="SMV Rolling")
        plt.legend()
        plt.show()

    def SMV_Window(self): # Creates Rolling Average for SMV
        self.SMV_roll = numpy.convolve(self.SMV, numpy.ones(25), 'valid') / 25
        self.movement()
        print(self.SMV_roll)


    def movement(self):
        for i in range(2, len(self.SMV_roll)):
            if self.SMV_roll[i] > 0.01 and self.SMV_roll[i - 1] > 0.01 and self.SMV_roll[i - 2] < 0.01:
                print(f"Started movement at {i}")
            elif self.SMV_roll[i] < 0.01 and self.SMV_roll[i - 1] < 0.01 and self.SMV_roll[i - 2] > 0.01:
                    print(f"Stopped movement at {i}")

