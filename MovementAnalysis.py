import pandas as pd
import numpy
import matplotlib.pyplot as plt

filename = "IMUData.csv"


plt.rcParams["figure.autolayout"] = True
df = pd.read_csv(filename)
Pitch = df[df.columns[0]]
Roll = df[df.columns[1]]
AccY = df[df.columns[2]]
AccX = df[df.columns[3]]
AccZ = df[df.columns[4]]
GyroX = df[df.columns[5]]
GyroY = df[df.columns[6]]
GyroZ = df[df.columns[7]]
print("Contents in csv file:")

sampling_freq = 250
x_time = numpy.arange(0, len(Roll) / sampling_freq, 1 / sampling_freq)

plt.subplot(3, 1, 1)
plt.plot(x_time, Roll,label="Roll")
plt.plot(x_time, Pitch,label="Pitch")
plt.xlabel("Time (s)")
plt.ylabel("Angle (°)")
plt.legend(loc='center right')

plt.subplot(3, 1, 2)
plt.plot(x_time, AccX, label="X")
plt.plot(x_time, AccY, label="Y")
plt.plot(x_time, AccZ, label="Z")
plt.xlabel("Time (s)")
plt.ylabel("Acceleration (m/s2)")
plt.legend(loc='center right')

plt.subplot(3, 1, 3)
plt.plot(x_time, GyroX, label="X")
plt.plot(x_time, GyroY, label="Y")
plt.plot(x_time, GyroZ, label="Z")
plt.xlabel("Time (s)")
plt.ylabel("Angular Velocity (r/s)")
plt.legend(loc='center right')

plt.show()