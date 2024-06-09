import pandas as pd
import numpy
import matplotlib.pyplot as plt
from scipy import signal

filename = "../IMUData.csv"
plt.rcParams["figure.autolayout"] = True
df = pd.read_csv(filename)
print(df.columns)
Pitch = df["Pitch"]
Roll = df['Roll']
AccY = df['AccY']
AccX = df['AccX']
AccZ = df['AccZ']
GyroX = df['GyroX']
GyroY = df['GyroY']
GyroZ = df['GyroZ']
print("Contents in csv file:")
sampling_freq = 130
x_time = numpy.arange(0, len(Roll) / sampling_freq, 1 / sampling_freq)

def butter1():
    sos = signal.butter(1,0.25,'hp',fs=sampling_freq,output='sos')
    filtered_x = signal.sosfilt(sos,AccX)
    plt.subplot(3,1,1)
    plt.plot(x_time, filtered_x, label='filtered')
    plt.plot(x_time,AccX, label='original')
    plt.xlim(2)
    plt.legend()

    filtered_y = signal.sosfilt(sos,AccY)
    plt.subplot(3,1,2)
    plt.plot(x_time, filtered_y, label='filtered')
    plt.plot(x_time,AccY, label='original')
    plt.xlim(2)
    plt.legend()

    filtered_z = signal.sosfilt(sos,AccZ)
    plt.subplot(3,1,3)
    plt.plot(x_time, filtered_z, label='filtered')
    plt.plot(x_time,AccZ, label='original')
    plt.legend()
    plt.xlim(2)
    plt.show()

def jerk_calc():

    dt = 0.007
    plt.subplot(4,1,4)
    derivative_x = numpy.gradient(AccX,dt)
    plt.plot(x_time,derivative_x, label='X')
    derivative_y = numpy.gradient(AccY,dt)
    plt.plot(x_time,derivative_y, label='Y')
    derivative_z = numpy.gradient(AccZ,dt)
    plt.plot(x_time,derivative_z, label='Z')
    plt.xlabel("Time (s)")
    plt.ylabel("Jerk (g/s)")
    plt.legend(loc='center right')


def visualiser():

    plt.subplot(4, 1, 1)
    plt.plot(x_time, Roll, label="Roll")
    plt.plot(x_time, Pitch, label="Pitch")
    plt.xlabel("Time (s)")
    plt.ylabel("Angle (°)")
    plt.legend(loc='center right')

    plt.subplot(4, 1, 2)
    plt.plot(x_time, AccX, label="X")
    plt.plot(x_time, AccY, label="Y")
    plt.plot(x_time, AccZ, label="Z")
    plt.xlabel("Time (s)")
    plt.ylabel("Acceleration (g)")
    plt.legend(loc='center right')

    plt.subplot(4, 1, 3)
    plt.plot(x_time, GyroX, label="X")
    plt.plot(x_time, GyroY, label="Y")
    plt.plot(x_time, GyroZ, label="Z")
    plt.xlabel("Time (s)")
    plt.ylabel("Angular Velocity (r/s)")
    plt.legend(loc='center right')

    jerk_calc()
    plt.show()

butter1()