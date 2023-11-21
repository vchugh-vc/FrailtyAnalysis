import pandas as pd
import numpy
import matplotlib.pyplot as plt
from FeaturesClass import Features
from FeatureExtraction2 import DataPreparation

filename = "IMUData.csv"
plt.rcParams["figure.autolayout"] = True
df = pd.read_csv(filename)
print(df.columns)
IMUAccY = df['AccY']
IMUAccX = df['AccX']
IMUAccZ = df['AccZ']
GyroX = df['GyroX']
GyroY = df['GyroY']
GyroZ = df['GyroZ']
sampling_freq = 130

AccX = Features(IMUAccX, status="raw", name='AccX')
AccY = Features(IMUAccY, status="raw", name='AccY')
AccZ = Features(IMUAccZ, status="raw", name='AccZ')


def signal_magnitude_vector():
    signal_sum = pow(AccX.ProcessedData, 2) + pow(AccY.ProcessedData, 2) + pow(AccZ.ProcessedData, 2)
    smv_data = numpy.sqrt(signal_sum)

    return smv_data


smv = signal_magnitude_vector()
SMV = Features(smv, 'processed', 'SMV')



def detailed_visualiser():
    AccZ.sliding_windows()
    plt.show()

FilteredData = DataPreparation()





