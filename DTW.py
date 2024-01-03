# https://github.com/talcs/simpledtw

import pandas as pd
import os
import matplotlib.pyplot as plt
from FeatureClass import DataPreparation, Features

from dtaidistance import dtw

FilteredData = DataPreparation()
DataFeatures = Features(FilteredData)

AccZ = DataFeatures.AccZ
AccY = DataFeatures.AccY
AccX = DataFeatures.AccX



def DTW1():  # DTW Comparing an entire signal against pre-recorded signals and return the best fit
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


def DTWUp():  # Compares a known lifting signal to different intervals of a movement
    IMUFile = "EdgeData/Up-Mid-Stable-1.csv"
    df = pd.read_csv(IMUFile)
    DTWAccZ = df['accZ']
    i = 30
    minimum = 100
    data_range = 0
    while i < 200:
        distance = dtw.distance(AccZ[0:i], DTWAccZ)
        print(f"From 0:{i}, the distance is {distance}")
        if distance <= minimum:
            minimum = distance
            data_range = i
        i += 30

    print(data_range)
    plt.plot(DTWAccZ, label='DTW')
    plt.plot(AccZ[0:data_range], label='IMU')
    plt.legend()
    plt.show()

    return data_range


def DTWDown():  # Compares a known down signal to different intervals of a movement
    IMUFile = "EdgeData/Down-Slow-Stable-2.csv"
    df = pd.read_csv(IMUFile)
    DTWAccZ = df['accZ']
    i = 30
    minimum = 100
    data_range = 0
    while i < 400:
        distance = dtw.distance(AccZ[-i:], DTWAccZ)
        print(f"From 0-{i}, the distance is {distance}")
        if distance <= minimum:
            minimum = distance
            data_range = i
        i += 30

    print(data_range)
    plt.plot(DTWAccZ, label='DTW')
    plt.plot(AccZ[-data_range:], label='IMU')
    plt.legend()
    plt.show()

    return data_range

up_end = DTWUp()
down_start = len(AccZ) - DTWDown()

plt.plot(AccX[up_end:down_start])
plt.plot(AccY[up_end:down_start])
plt.plot(AccZ[up_end:down_start])
plt.show()


