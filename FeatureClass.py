import pandas as pd
import numpy
import matplotlib.pyplot as plt
from scipy import signal

filename = "IMUData.csv"
plt.rcParams["figure.autolayout"] = True
df = pd.read_csv(filename)
Time = df['Time']
IMUAccY = df['AccY']
IMUAccX = df['AccX']
IMUAccZ = df['AccZ']
GyroX = df['GyroX']
GyroY = df['GyroY']
GyroZ = df['GyroZ']
Time_diff = (df['Time'].iloc[-1] - df['Time'].iloc[0])
SAMPLE_TIME = (Time_diff / len(Time)) / 1000
SAMPLE_FREQ = numpy.round(1000 * len(Time) / Time_diff)


class DataPreparation:

    def __init__(self):
        self.AccX_Trimmed = None
        self.AccY_Trimmed = None
        self.AccZ_Trimmed = None
        self.SMV_Trimmed = None
        self.AccX = self.ButterFilter(IMUAccX)
        self.AccY = self.ButterFilter(IMUAccY)
        self.AccZ = self.ButterFilter(IMUAccZ)
        self.SMV = self.SMV_Calc()
        self.SMV_roll = []
        self.jerk = []
        self.jerk_roll = []
        self.FilteredLength = len(self.AccX)
        self.time_axis = numpy.arange(0, self.FilteredLength / SAMPLE_FREQ,
                                      1 / SAMPLE_FREQ)
        self.SMV_Window()
        self.rolling_axis = numpy.arange(0, self.FilteredLength / SAMPLE_FREQ,
                                         (self.FilteredLength / SAMPLE_FREQ) / len(
                                             self.SMV_roll))

        self.jerk_calc()
        self.grapher()

    def ButterFilter(self, RawData):  # Butterworth Function Filter to remove gravity
        sos = signal.butter(1, 0.25, 'hp', fs=SAMPLE_FREQ, output='sos')
        ButterData = signal.sosfilt(sos, RawData)
        return ButterData[400:]

    def jerk_calc(self):

        self.jerk = numpy.gradient(self.SMV)
        self.jerk_roll = numpy.convolve(self.jerk, numpy.ones(20), 'same') / 20

    def SMV_Calc(self):  # Calculates SMV from Acceleratio Data
        signal_sum = pow(self.AccX, 2) + pow(self.AccY, 2) + pow(self.AccZ, 2)
        return numpy.sqrt(signal_sum)

    def grapher(self):  # Graphs Acceleration and SMV

        plt.subplot(3, 1, 1)
        plt.plot(self.time_axis, self.AccX, label="X")
        plt.plot(self.time_axis, self.AccY, label="Y")
        plt.plot(self.time_axis, self.AccZ, label="Z")
        plt.legend()
        plt.subplot(3, 1, 2)
        plt.plot(self.time_axis, self.SMV, label='SMV')
        plt.plot(self.time_axis, self.SMV_roll, label="SMV Rolling")
        plt.legend()
        plt.subplot(3, 1, 3)
        # plt.plot(self.time_axis, self.jerk, label='Jerk')
        plt.plot(self.time_axis, self.jerk_roll, label="Jerk Rolling")
        plt.legend()
        plt.show()

    def SMV_Window(self):  # Creates Rolling Average for SMV
        self.SMV_roll = numpy.convolve(self.SMV, numpy.ones(20), 'same') / 20
        self.movement_filter()

    def movement_filter(
            self):  # Detects when movement has started or stopped based on previous values (of rolling SMV) at a
        # given threshold
        start = []  # used for if there are multiple start stops in a movement pattern
        stop = []
        for i in range(2, len(self.SMV_roll)):
            if self.SMV_roll[i] > 0.015 > self.SMV_roll[i - 2] and self.SMV_roll[i - 1] > 0.015:
                print(f"Started movement at {i * SAMPLE_TIME} : {i}")
                start.append(i)
            elif self.SMV_roll[i] < 0.015 < self.SMV_roll[i - 2] and self.SMV_roll[i - 1] < 0.015:
                print(f"Stopped movement at {i * SAMPLE_TIME} : {i}")
                stop.append(i)

        value = 0
        time_stamp = 0
        for j in range(len(start)):
            if (stop[j-1]-start[j-1]) > value:
                value = stop[j-1]-start[j-1]
                time_stamp = j-1
        print(f"Duration {value}")
        self.SMV_Trimmed = self.SMV[start[time_stamp]:stop[time_stamp]]
        self.AccX_Trimmed = self.AccX[start[time_stamp]:stop[time_stamp]]
        self.AccY_Trimmed = self.AccY[start[time_stamp]:stop[time_stamp]]
        self.AccZ_Trimmed = self.AccZ[start[time_stamp]:stop[time_stamp]]


class Features:

    def __init__(self, TrimmedData):

        self.AccX = TrimmedData.AccX_Trimmed
        self.AccY = TrimmedData.AccY_Trimmed
        self.AccZ = TrimmedData.AccZ_Trimmed
        self.SMV = TrimmedData.SMV_Trimmed
        self.trimmed_axis = numpy.arange(0, len(self.AccX) / SAMPLE_FREQ,
                                         1 / SAMPLE_FREQ)
        self.graph_trimmed()
        self.window_x = self.sliding_windows(self.AccX)
        self.window_y = self.sliding_windows(self.AccY)
        self.window_z = self.sliding_windows(self.AccZ)
        self.window_SMV = self.sliding_windows(self.SMV)

        self.x_features = {'max': [], 'min': [], 'minmax': [], 'peak': [], 'rms': [], 'std': [], 'var': []}
        self.y_features = {'max': [], 'min': [], 'minmax': [], 'peak': [], 'rms': [], 'std': [], 'var': []}
        self.z_features = {'max': [], 'min': [], 'minmax': [], 'peak': [], 'rms': [], 'std': [], 'var': []}
        self.SMV_features = {'max': [], 'min': [], 'minmax': [], 'peak': [], 'rms': [], 'std': [], 'var': []}

        self.data_extraction(self.window_SMV, self.SMV_features)
        self.data_extraction(self.window_z, self.z_features)
        self.data_extraction(self.window_y, self.y_features)
        self.data_extraction(self.window_x, self.x_features)

        self.features_graph()

    def graph_trimmed(self):  # graphs the sections that have been trimmed by the movement filter

        plt.subplot(2, 1, 1)
        plt.plot(self.trimmed_axis, self.AccX, label="X")
        plt.plot(self.trimmed_axis, self.AccY, label="Y")
        plt.plot(self.trimmed_axis, self.AccZ, label="Z")
        plt.legend()
        plt.subplot(2, 1, 2)
        plt.plot(self.trimmed_axis, self.SMV, label='SMV')
        plt.legend()
        plt.show()

    def sliding_windows(self, data):  # Creates Sliding Windows from Filtered and Sliced Array
        i = 0
        window_array = []
        while i <= len(data):
            window_small = data[i:i + 10]
            window_array.append(window_small)
            i += 5
        return window_array

    def minmax_spread(self, array, dictionary):  # Returns Min-Max Data of an Array
        max_data = max(array)
        min_data = min(array)
        minmax_data = max_data - min_data
        peak_data = max(max_data, min_data)
        rms_data = numpy.sqrt(numpy.mean(array ** 2))
        std_data = numpy.std(array)
        var_data = numpy.var(array)

        dictionary['max'].append(max_data)
        dictionary['min'].append(min_data)
        dictionary['minmax'].append(minmax_data)
        dictionary['peak'].append(peak_data)
        dictionary['rms'].append(rms_data)
        dictionary['std'].append(std_data)
        dictionary['var'].append(var_data)

    def data_extraction(self, array, dictionary):

        for i in array:
            if len(i) > 0:
                self.minmax_spread(i, dictionary)

    def features_graph(self):

        axis = {"x": self.x_features, "y": self.y_features, "z": self.z_features, "SMV": self.SMV_features}
        labels = ['max','min','minmax','peak','rms','std','var']
        plt.figure(figsize=(10, 8))
        for i in range(len(labels)):
            for key, value in axis.items():
                # print(f"{key} {labels[i]} {value[labels[i]]} {i}")
                plt.subplot(7, 1, i+1)
                plt.plot(value[labels[i]], label=key)
                plt.legend()
            plt.title(labels[i])

        plt.show()