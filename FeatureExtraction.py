import pandas as pd
import numpy
import matplotlib.pyplot as plt
from scipy import signal

filename = "IMUData.csv"
plt.rcParams["figure.autolayout"] = True
df = pd.read_csv(filename)
print(df.columns)
AccY = df['AccY']
AccX = df['AccX']
AccZ = df['AccZ']
GyroX = df['GyroX']
GyroY = df['GyroY']
GyroZ = df['GyroZ']
print("Contents in csv file:")
sampling_freq = 130
x_time = numpy.arange(0, len(AccY) / sampling_freq, 1 / sampling_freq)