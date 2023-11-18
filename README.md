# IMUAnalysis

Python Files used for Signal Processing (from an IMU) and for Extracting Features for Frailty Analysis

**Data Logger** : File for Extracting data from IMU and exporting to a CSV (Pitch,Roll,AccY,AccX,AccZ,GyroX,GyroY,GyroZ)

**Movement Analysis** : Graphing Output of all IMU Data. Contains Jerk Calculation and Butterworth Filter.

**FFT Analysis** : Fast Fourier Transform Function resulting in spectral analysis of IMU Data

**Feature Extraction** : Extracting Key Features from Data (Max, Min, RMS, STD, VAR, SMV) and Sliding Windows Function for Analysis

**DTW Movement** : DTW Function to compare input (IMU) signals to a known patter and return Similarity Measurement