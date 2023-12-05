from FeatureClass import DataPreparation, Features
import pandas as pd
import numpy
import csv
import matplotlib.pyplot as plt

FilteredData = DataPreparation()
DataFeatures = Features(FilteredData)

Jerk = DataFeatures.Jerk
Jerk_RMS = numpy.sqrt(numpy.mean(Jerk ** 2))
print(f"Average Jerk of Movement: {Jerk_RMS} m/s-3")
print(f"Length of movemenet {len(Jerk)} at {DataFeatures.time}")
print(f"Dominant Freq is {DataFeatures.FFTFreq}")