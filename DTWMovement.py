from dtaidistance import dtw
from dtaidistance import dtw_visualisation as dtwvis
import numpy as np
import pandas as pd

IMUFile = "IMUData.csv"
df = pd.read_csv(IMUFile)
Pitch = df['Pitch']

ExampleFile = "PitchTiltDTW.csv"
exampleDF = pd.read_csv(ExampleFile)
ExamplePitch = exampleDF[df.columns[0]]


s1 = ExamplePitch
s2 = Pitch
path = dtw.warping_path(s1, s2)
distance = dtw.distance(s1,s2)
dtwvis.plot_warping(s1, s2, path, filename="warp.png")

print(distance)