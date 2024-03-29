from FeatureClass import DataPreparation, Features
import pandas as pd
import numpy
from scipy.signal import butter, lfilter
from DTW import DataTimeWarping
from FrailtyIndex import Frailty
import matplotlib.pyplot as plt
import os

FILE = ('LongitudinalData/2024-03-29 18:19:00-T1.csv')

FOLDER = 'LongitudinalData'
files = os.listdir(FOLDER)
files_order = sorted(files)

for i in range(140,len(files_order)):
    print(f"{i}: {files_order[i]}")

    FilteredData = DataPreparation(file=f"LongitudinalData/{files_order[i]}")
    AccZ = FilteredData.AccZ_Trimmed
    AccX = FilteredData.AccX_Trimmed
    DTWPhases = DataTimeWarping(AccZ, AccX)
    TimeStamps = DTWPhases.movement_stamps
    # TimeStamps = [0, 97, 107, 147, 167, 902, 1100]
    up_data = Features(FilteredData, TimeStamps, 'up')
    middle_data = Features(FilteredData, TimeStamps, 'middle')
    Frailty(up_data, middle_data)