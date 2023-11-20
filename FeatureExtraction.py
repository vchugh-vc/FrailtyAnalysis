import pandas as pd
import numpy
import matplotlib.pyplot as plt
from FeaturesClass import Features

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

def overview():

    AccX.Accel_Graph()
    AccY.Accel_Graph()
    AccZ.Accel_Graph()
    SMV.SMV_Graph()
    plt.show()

def detailed_visualiser():
    AccX.sliding_windows()
    plt.show()

overview()
detailed_visualiser()



