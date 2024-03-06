# IMUAnalysis

Python Files used for Signal Processing (from an IMU) and for Extracting Features for Frailty Analysis

**FrailtyIndex** Calculates Frailty Score from Specific Parameters

**FeatureClass** : Contains Class for Data Pre-Processing (Filtration of Noise and Movement) and Class for Processing and Extracting Parameters Related to Frailty

**SignalAnalysis** : Analyses Signal (from a given CSV) using FrailtyClass and FrailtyIndex

**MQTT** : Enables MQTT Server for Receiving Data from Nearable Device

**DTW**: Segments Signal into different movement phases, using DTW and Peaks Algorithm

**Main** : Runs MQTT, Feature Class & Frailty Index to Receive and Analyse Signal immediately

**DataRecorder** : Receives Data (through MQTT) and stores data in CSV File

**SPARC** : (Legacy) Calculates Spectral Arc Length of Signal, which is being called in FeatureClass

**FeatureExtraction** : (Legacy) Runs FeatureClass using existing IMU Data (from DataLogger) and outputs to CSV (Database for ML Training)

**WireDataLogger** : (Legacy) File for Extracting data from IMU and exporting to a CSV (Pitch,Roll,AccY,AccX,AccZ,GyroX,GyroY,GyroZ)

**FFT Analysis** : (Legacy) Fast Fourier Transform Function resulting in spectral analysis of IMU Data

**Movement Analysis** : (Legacy) Graphing Output of all IMU Data. Contains Jerk Calculation and Butterworth Filter.