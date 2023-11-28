from FeatureClass import DataPreparation, Features
import pandas as pd
import csv

sampling_freq = 130

HEADERS = ['Xmax', 'Xmin', 'Xminmax','XPeak', 'Xrms','Xstd','Xvar', 'YMax', 'Ymin', 'Yminmax','YPeak', 'Yrms','Ystd','Yvar','Zmax', 'Zmin', 'Zminmax','ZPeak', 'Zrms','Zstd','Zvar','SMVzax', 'SMVmin', 'SMVminmax','SMVPeak', 'SMVrms','SMVstd','SMVvar', 'ManualLabel']

outputFile = "FeaturesData.csv"

FilteredData = DataPreparation()
DataFeatures = Features(FilteredData)
data = DataFeatures.output2
df = pd.DataFrame.from_dict([data])



with open(outputFile, 'a') as f:  # You will need 'wb' mode in Python 2.x
    w = csv.DictWriter(f, data.keys())
    w.writerow(data)

print(df)



