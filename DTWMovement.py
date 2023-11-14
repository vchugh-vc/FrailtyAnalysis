import pandas as pd
import numpy
import matplotlib.pyplot as plt
from scipy.spatial.distance import euclidean
from fastdtw import fastdtw

reference = "PitchTiltDTW.csv"
plt.rcParams["figure.autolayout"] = True
df = pd.read_csv(reference)
Pitch = df[df.columns[0]]
Roll = df[df.columns[1]]
AccY = df[df.columns[2]]
AccX = df[df.columns[3]]
AccZ = df[df.columns[4]]
GyroX = df[df.columns[5]]
GyroY = df[df.columns[6]]
GyroZ = df[df.columns[7]]
print("Contents in csv file:")
sampling_freq = 130
x_time = numpy.arange(0, len(Roll) / sampling_freq, 1 / sampling_freq)

plt.subplot(2, 1, 1)
plt.plot(x_time, Pitch, label="Pitch")
plt.xlabel("Time (s)")
plt.ylabel("Angle (°)")
plt.legend(loc='center right')
plt.show()