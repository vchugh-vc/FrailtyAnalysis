# IMUAnalysis

Python Files used for Signal Processing (from an IMU) and for Extracting Features for Frailty Analysis

**DataLogger** : File for Extracting data from IMU and exporting to a CSV (Pitch,Roll,AccY,AccX,AccZ,GyroX,GyroY,GyroZ)

**FeatureClass** : Extracting Key Features from Data (Max, Min, Range, RMS, STD, VAR, SMV, Frequency) and Jerk for Analysis

**SignalAnalysis** : Frailty Index Calculator (Processing Key Parameters from FeaturesClass)

**FeatureExtraction** : Runs FeatureClass using existing IMU Data (from DataLogger) and outputs to CSV (Database for ML Training)

**FFT Analysis** : (Legacy) Fast Fourier Transform Function resulting in spectral analysis of IMU Data

**Movement Analysis** : (Legacy) Graphing Output of all IMU Data. Contains Jerk Calculation and Butterworth Filter.