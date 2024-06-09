from FeatureClass import DataPreparation, Features
import pandas as pd
import csv
import matplotlib.pyplot as plt
import numpy

FilteredData = DataPreparation()

time = numpy.round(FilteredData.time_axis_trimmed * 1000)
accX = FilteredData.AccX_Trimmed
accY = FilteredData.AccY_Trimmed
accZ = FilteredData.AccZ_Trimmed
gyroX = FilteredData.GyroX_Trimmed
gyroY = FilteredData.GyroY_Trimmed
gyroZ = FilteredData.GyroZ_Trimmed
pitch = FilteredData.Pitch_Trimmed
roll = FilteredData.Roll_Trimmed

print(f"{len(time)} {len(accX)} {len(accY)} {len(accZ)}")

df = pd.DataFrame({

    'AccX': accX,
    'AccY': accY,
    'AccZ': accZ,
    'GyroX': accX,
    'GyroY': accY,
    'GyroZ': accZ,
    'Roll': roll,
    'Pitch': pitch
})

plt.plot(time, accX)
plt.plot(time, accY)
plt.plot(time, accZ)
plt.show()

df.to_csv("CollectionData/Test1.csv", index=False)

