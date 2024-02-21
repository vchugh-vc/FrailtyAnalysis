from FeatureClass import DataPreparation, Features
import pandas as pd
import csv
import matplotlib.pyplot as plt
import numpy

FilteredData = DataPreparation()

time = numpy.round(FilteredData.time_axis_trimmed*1000)
accX = FilteredData.AccX_Trimmed
accY = FilteredData.AccY_Trimmed
accZ = FilteredData.AccZ_Trimmed
print(f"{len(time)} {len(accX)} {len(accY)} {len(accZ)}")

df = pd.DataFrame({

    'time': time,
    'accX': accX,
    'accY': accY,
    'accZ': accZ,
})

plt.plot(time,accX)
plt.plot(time,accY)
plt.plot(time,accZ)
plt.show()



df.to_csv("KettleData/Up-Mid-1.csv", index=False)
print(df)





