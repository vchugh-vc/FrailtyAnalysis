from FeatureClass import DataPreparation, Features
import pandas as pd

sampling_freq = 130

headers = ['AccX','AccY', 'AccZ', 'SMV','Jerk' ,'XMax', 'XMin', 'XMinMax','XPeak', 'XSTD','XRMS','XVAR','YMax', 'YMin','YMinMax','YPeak', 'YSTD','YRMS','YVAR','ZMax', 'ZMin', 'ZMinMax','ZPeak', 'ZSTD','ZRMS','ZVAR','smvMax', 'smvMin', 'smvMinMax','smvPeak', 'smvSTD','smvRMS','smvVAR']

outputFile = "FeaturesData.csv"

FilteredData = DataPreparation()
DataFeatures = Features(FilteredData)
data = DataFeatures.output
print(data)
df = pd.DataFrame(data)
new = df.T
new.to_csv(outputFile, header=headers)







