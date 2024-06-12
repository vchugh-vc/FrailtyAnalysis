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

for i in range(146, len(files_order)):
    print(f"{i}: {files_order[i]}")

    name_parts = os.path.splitext(files_order[i])[0]
    date_and_time = name_parts.rsplit('-', 1)[0]

    FilteredData = DataPreparation(file=f"LongitudinalData/{files_order[i]}")
    AccZ = FilteredData.AccZ_Trimmed
    AccX = FilteredData.AccX_Trimmed
    DTWPhases = DataTimeWarping(AccZ, AccX)
    TimeStamps = DTWPhases.movement_stamps
    # TimeStamps = [0, 31, 68, 78, 138, 841, 1046]
    up_data = Features(FilteredData, TimeStamps, 'up')
    middle_data = Features(FilteredData, TimeStamps, 'middle')
    Frailty(up_data, middle_data, date=date_and_time)
