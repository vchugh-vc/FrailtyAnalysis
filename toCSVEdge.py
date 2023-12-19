from FeatureClass import DataPreparation, Features
import pandas as pd
import csv
import matplotlib.pyplot as plt
import numpy

FilteredData = DataPreparation()
DataFeatures = Features(FilteredData)

time = numpy.round(DataFeatures.trimmed_axis*1000)
accX = DataFeatures.AccX
accY = DataFeatures.AccY
accZ = DataFeatures.AccZ
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



df.to_csv("EdgeData/Up.1.csv", index=False)





