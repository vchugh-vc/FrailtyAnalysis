import pandas as pd
import numpy
import matplotlib.pyplot as plt
from numpy.fft import fft, fftfreq, rfft
from scipy import signal

filename = "IMUData.csv"
plt.rcParams["figure.autolayout"] = True
df = pd.read_csv(filename)
# Time = df['Time']
IMUAccY = df['AccY']
IMUAccX = df['AccX']
IMUAccZ = df['AccZ']
IMUGyroX = df['GyroX']
IMUGyroY = df['GyroY']
IMUGyroZ = df['GyroZ']
IMURoll = df['Roll']
IMUPitch = df['Pitch']
# Time_diff = (df['Time'].iloc[-1] - df['Time'].iloc[0])

# SAMPLE_TIME = (Time_diff / len(Time)) / 1000
# SAMPLE_FREQ = numpy.round(1000 * len(Time) / Time_diff)

SAMPLE_TIME = 0.0096
SAMPLE_FREQ = 104

SENSE = 0.02
print(f"Sample Time: {SAMPLE_TIME} at Sample Freq: {SAMPLE_FREQ}")


class DataPreparation:

    def __init__(self):
        self.AccX_Trimmed = None
        self.AccY_Trimmed = None
        self.AccZ_Trimmed = None
        self.SMV_Trimmed = None
        self.Jerk_Trimmed = None
        self.GyroX_Trimmed = None
        self.GyroY_Trimmed = None
        self.GyroZ_Trimmed = None
        self.AccX = self.ButterFilter(IMUAccX)
        self.AccY = self.ButterFilter(IMUAccY)  # Gravity Filtered IMU Data
        self.AccZ = self.ButterFilter(IMUAccZ)
        self.GyroX = IMUGyroX[500:]
        self.GyroY = IMUGyroY[500:]  # Gyro Data (Sliced to match Acc length, post-gravity filtering)
        self.GyroZ = IMUGyroZ[500:]
        self.Roll = IMURoll[500:]
        self.Pitch = IMUPitch[500:]
        self.SMV = self.SMV_Calc()
        self.jerk = []
        self.jerk_roll = []
        self.jerk_calc()
        self.SMV_roll = []
        self.Sample_Freq = SAMPLE_FREQ
        self.FilteredLength = len(self.AccX)
        self.time_axis = numpy.arange(0, (self.FilteredLength / SAMPLE_FREQ),
                                      1 / SAMPLE_FREQ)
        self.SMV_Window()
        self.rolling_axis = numpy.arange(0, self.FilteredLength / SAMPLE_FREQ,
                                         (self.FilteredLength / SAMPLE_FREQ) / len(
                                             self.SMV_roll))

        self.grapher()

    def ButterFilter(self, RawData):  # Butterworth Function Filter to remove gravity
        sos = signal.butter(1, 0.25, 'hp', fs=SAMPLE_FREQ, output='sos')
        ButterData = signal.sosfilt(sos, RawData)
        return ButterData[500:]

    def jerk_calc(self):  # Jerk Calculation of movement (Acc. Derivative)

        self.jerk = numpy.gradient(self.SMV)
        self.jerk_roll = numpy.convolve(self.jerk, numpy.ones(20), 'same') / 20

    def SMV_Calc(self):  # Calculates SMV from Acceleration Data
        signal_sum = pow(self.AccX, 2) + pow(self.AccY, 2) + pow(self.AccZ, 2)
        return numpy.sqrt(signal_sum)

    def grapher(self):  # Graphs Acceleration and SMV

        print(f"Acc = {len(self.AccX)} and Time {len(self.time_axis)}")
        if len(self.AccX) < len(self.time_axis):
            self.time_axis = self.time_axis[:-1]
            print(f"Acc = {len(self.AccX)} and Time {len(self.time_axis)}")

        if len(self.AccX) == len(self.time_axis):
            plt.subplot(3, 1, 1)
            plt.plot(self.time_axis, self.AccX, label="X")
            plt.plot(self.time_axis, self.AccY, label="Y")
            plt.plot(self.time_axis, self.AccZ, label="Z")
            plt.ylim(-1, 1)
            plt.xlabel("Time (s)")
            plt.ylabel("Acceleration (g)")
            plt.title("Acceleration (X,Y,Z)")
            plt.legend(loc=1)
            plt.subplot(3, 1, 2)
            plt.plot(self.time_axis, self.SMV, label='SMV')
            plt.plot(self.time_axis, self.SMV_roll, label="SMV Rolling")
            plt.legend(loc=1)
            plt.xlabel("Time (s)")
            plt.ylabel("Acceleration (g)")
            plt.title("Acceleration (SMV)")
            plt.ylim(-0.2, 1)
            plt.subplot(3, 1, 3)
            # plt.plot(self.time_axis, self.jerk, label='Jerk')
            plt.plot(self.time_axis, self.jerk_roll, label="Jerk")
            plt.legend(loc=1)
            plt.ylim(-0.03, 0.03)
            plt.xlabel("Time (s)")
            plt.ylabel("Jerk (g/s)")
            plt.title("Jerk (SMV)")
            plt.legend(loc=1)
            plt.show()

    def SMV_Window(self):  # Creates Rolling Average for SMV
        self.SMV_roll = numpy.convolve(self.SMV, numpy.ones(15), 'same') / 15
        # self.movement_filter()
        self.movement_filter2()

    def movement_filter(
            self):  # Detects when movement has started or stopped based on previous values (of rolling SMV) at a
        # given threshold

        start = []  # used for if there are multiple start stops in a movement pattern
        stop = []
        start.append(0)
        for i in range(4, len(self.SMV_roll)):
            if (self.SMV_roll[i] > SENSE > self.SMV_roll[i - 4] and self.SMV_roll[i - 2] > SENSE and self.SMV_roll[
                i - 1] > SENSE and self.SMV_roll[i - 3] > SENSE):
                print(f"Started movement at {i * SAMPLE_TIME} : {i}")
                start.append(i)
            elif self.SMV_roll[i] < SENSE < self.SMV_roll[i - 4] and self.SMV_roll[i - 2] < SENSE and self.SMV_roll[
                i - 1] < SENSE and self.SMV_roll[i - 3] < SENSE:
                print(f"Stopped movement at {i * SAMPLE_TIME} : {i}")
                stop.append(i)

        stop.append(len(self.SMV_roll))
        if len(start) < 1:
            start.append(0)

        value = 0
        time_stamp = 0

        for j in range(len(start) - 1):
            print(j)
            if (stop[j - 1] - start[j - 1]) > value:
                value = stop[j - 1] - start[j - 1]
                time_stamp = j - 1
        print(f"From {start[time_stamp]} to {stop[time_stamp]}")

        self.SMV_Trimmed = self.SMV[start[time_stamp]:stop[time_stamp]]
        self.AccX_Trimmed = self.AccX[start[time_stamp]:stop[time_stamp]]
        self.AccY_Trimmed = self.AccY[start[time_stamp]:stop[time_stamp]]
        self.AccZ_Trimmed = self.AccZ[start[time_stamp]:stop[time_stamp]]
        self.Jerk_Trimmed = self.jerk_roll[start[time_stamp]:stop[time_stamp]]
        self.GyroX_Trimmed = self.GyroX[start[time_stamp]:stop[time_stamp]]
        self.GyroY_Trimmed = self.GyroY[start[time_stamp]:stop[time_stamp]]
        self.GyroZ_Trimmed = self.GyroZ[start[time_stamp]:stop[time_stamp]]
        self.Roll_Trimmed = self.Roll[start[time_stamp]:stop[time_stamp]]
        self.Pitch_Trimmed = self.Pitch[start[time_stamp]:stop[time_stamp]]

    def movement_filter2(
            self):  # Detects when movement has started or stopped based on previous values (of rolling SMV) at a
        # given threshold

        time_data = {}

        for i in range(4, len(self.SMV_roll)):
            if (self.SMV_roll[i] > SENSE > self.SMV_roll[i - 4] and self.SMV_roll[i - 2] > SENSE and self.SMV_roll[
                i - 1] > SENSE and self.SMV_roll[i - 3] > SENSE):
                print(f"2 Started movement at {i * SAMPLE_TIME} : {i}")
                time_data[i] = 'start'

            elif self.SMV_roll[i] < SENSE < self.SMV_roll[i - 4] and self.SMV_roll[i - 2] < SENSE and self.SMV_roll[
                i - 1] < SENSE and self.SMV_roll[i - 3] < SENSE:
                print(f"2 Stopped movement at {i * SAMPLE_TIME} : {i}")
                time_data[i] = "stop"

        longest_duration = 0

        sequence = ['start', 'stop']
        clips = []
        diff_movements = {}

        keys = list(time_data.keys())
        values = list(time_data.values())

        if 'start' in values:  # checks to make sure Start/Stop has been recorded
            print('start is there')
        else:
            time_data[0] = 'start'
        if 'stop' in values:
            print('stop is there')
        else:
            time_data[len(self.SMV_roll)] = 'stop'

        keys = list(time_data.keys())
        values = list(time_data.values())

        for i in range(len(values) - len(sequence) + 1):  # Checks for start-stop sequence
            if values[i:i + len(sequence)] == sequence:
                clips.append(keys[i:i + len(sequence)])

        for i in range(min(len(clips), len(clips))):  # calculates the longest period of movement to select
            start_time = clips[i][0]
            stop_time = clips[i][1]
            duration = stop_time - start_time
            diff_movements[i] = {'duration': duration, 'start': start_time, 'stop': stop_time}
            if duration > longest_duration:
                longest_duration = duration
                movement_start = start_time
                movement_stop = stop_time

        for k, v in diff_movements.items():  # Calculates the SMV (RMS) value for each movement clip
            array = self.SMV[v['start']:v['stop']]
            array_rms = numpy.sqrt(numpy.mean(array ** 2))
            v['SMV'] = numpy.round(array_rms, 3)
            v['Movement'] = numpy.round(v['duration'] * v['SMV'], 3)

        print(diff_movements)
        print(
            f"2 From {movement_start * SAMPLE_TIME} ({movement_start}) to {movement_stop * SAMPLE_TIME} ({movement_stop})")

        # creates filtered data based on movement filter

        self.SMV_Trimmed = self.SMV[movement_start:movement_stop]
        self.AccX_Trimmed = self.AccX[movement_start:movement_stop]
        self.AccY_Trimmed = self.AccY[movement_start:movement_stop]
        self.AccZ_Trimmed = self.AccZ[movement_start:movement_stop]
        self.Jerk_Trimmed = self.jerk_roll[movement_start:movement_stop]
        self.GyroX_Trimmed = self.GyroX[movement_start:movement_stop]
        self.GyroY_Trimmed = self.GyroY[movement_start:movement_stop]
        self.GyroZ_Trimmed = self.GyroZ[movement_start:movement_stop]
        self.Roll_Trimmed = self.Roll[movement_start:movement_stop]
        self.Pitch_Trimmed = self.Pitch[movement_start:movement_stop]


class Features:

    def __init__(self, TrimmedData):

        self.AccX = TrimmedData.AccX_Trimmed
        self.AccY = TrimmedData.AccY_Trimmed
        self.AccZ = TrimmedData.AccZ_Trimmed
        self.SMV = TrimmedData.SMV_Trimmed
        self.Jerk = TrimmedData.Jerk_Trimmed
        self.GyroX = TrimmedData.GyroX_Trimmed
        self.GyroY = TrimmedData.GyroY_Trimmed
        self.GyroZ = TrimmedData.GyroZ_Trimmed
        self.Roll = TrimmedData.Roll_Trimmed
        self.Pitch = TrimmedData.Pitch_Trimmed

        self.time = len(self.SMV) * SAMPLE_TIME
        self.trimmed_axis = numpy.arange(0, len(self.AccX) / SAMPLE_FREQ,
                                         1 / SAMPLE_FREQ)
        self.graph_trimmed()
        self.FFTFreq = 0

        self.x_features = {}
        self.y_features = {}
        self.z_features = {}
        self.SMV_features = {}

        self.data_extraction(self.SMV, self.SMV_features)
        self.data_extraction(self.AccZ, self.z_features)
        self.data_extraction(self.AccY, self.y_features)
        self.data_extraction(self.AccX, self.x_features)

        self.frequency_calc()
        self.freq_calc_2()

        self.output = [self.x_features['max'], self.x_features['min'], self.x_features['minmax'],
                       self.x_features['peak'], self.x_features['std'], self.x_features['rms'], self.x_features['var'],
                       self.y_features['max'], self.y_features['min'], self.y_features['minmax'],
                       self.y_features['peak'], self.y_features['std'], self.y_features['rms'], self.y_features['var'],
                       self.z_features['max'], self.z_features['min'], self.z_features['minmax'],
                       self.z_features['peak'], self.z_features['std'], self.z_features['rms'], self.z_features['var'],
                       self.SMV_features['max'], self.SMV_features['min'], self.SMV_features['minmax'],
                       self.SMV_features['peak'], self.SMV_features['std'], self.SMV_features['rms'],
                       self.SMV_features['var'], self.FFTFreq]

        self.output2 = {}
        self.dictionary_combine()
        self.angle_graph()

    def graph_trimmed(self):  # graphs the sections that have been trimmed by the movement filter

        if (len(self.trimmed_axis)) > len(self.AccX):
            last = len(self.trimmed_axis) - 1
            self.trimmed_axis = self.trimmed_axis[:last]
        plt.subplot(3, 1, 1)
        plt.plot(self.trimmed_axis, self.AccX, label="X")
        plt.plot(self.trimmed_axis, self.AccY, label="Y")
        plt.plot(self.trimmed_axis, self.AccZ, label="Z")
        plt.ylim(-1, 1)
        plt.xlabel("Time (s)")
        plt.ylabel("Acceleration (g)")
        plt.title("Acceleration (X, Y, Z)")
        plt.legend(loc=1)
        plt.subplot(3, 1, 2)
        plt.plot(self.trimmed_axis, self.SMV, label='SMV')
        plt.legend(loc=1)
        plt.ylim(-0.2, 1.5)
        plt.xlabel("Time (s)")
        plt.ylabel("Acceleration (g)")
        plt.title("Acceleration (SMV)")
        plt.subplot(3, 1, 3)
        plt.plot(self.trimmed_axis, self.Jerk, label='SMV')
        plt.legend(loc=1)
        plt.ylim(-0.03, 0.03)
        plt.xlabel("Time (s)")
        plt.ylabel("Jerk (g/s)")
        plt.title("Jerk (SMV)")
        plt.show()

    def sliding_windows(self, data):  # Creates Sliding Windows from Filtered and Sliced Array
        i = 0
        window_array = []
        while i <= len(data):
            window_small = data[i:i + 20]
            window_array.append(window_small)
            i += 10
        return window_array

    def minmax_spread(self, array, dictionary):  # Returns Min-Max Data of an Array
        max_data = max(array)
        min_data = min(array)
        minmax_data = max_data - min_data
        peak_data = max(max_data, min_data)
        rms_data = numpy.sqrt(numpy.mean(array ** 2))
        std_data = numpy.nanstd(array)
        var_data = numpy.nanvar(array)
        dictionary['max'] = max_data
        dictionary['min'] = min_data
        dictionary['minmax'] = minmax_data
        dictionary['peak'] = peak_data
        dictionary['rms'] = rms_data
        dictionary['std'] = std_data
        dictionary['var'] = var_data

    def data_extraction(self, array, dictionary):
        self.minmax_spread(array, dictionary)
        print(dictionary)

    def dictionary_combine(self):

        axis = [self.x_features, self.y_features, self.z_features, self.SMV_features]

        for i in range(len(axis)):
            for keys, values in axis[i].items():
                if i == 0:
                    label = 'X'
                elif i == 1:
                    label = 'Y'
                elif i == 2:
                    label = 'Z'
                elif i == 3:
                    label = 'SMV'
                print(f"{label}{keys} : {values}")
                self.output2[f"{label}{keys}"] = values

        self.output2['Freq'] = self.FFTFreq

    def features_graph(self):

        plt.subplot(3, 1, 1)
        plt.plot(self.x_features['rms'], label="X")
        plt.plot(self.y_features['rms'], label="Y")
        plt.plot(self.z_features['rms'], label="Z")
        plt.plot(self.SMV_features['rms'], label="SMV")
        plt.ylim(-0.1, 0.5)
        plt.title("RMS of Data")
        plt.legend(loc=1)
        plt.subplot(3, 1, 2)
        plt.plot(self.x_features['var'], label="X")
        plt.plot(self.y_features['var'], label="Y")
        plt.plot(self.z_features['var'], label="Z")
        plt.plot(self.SMV_features['var'], label="SMV")
        plt.ylim(-0.005, 0.03)
        plt.title("VAR of Data")
        plt.legend(loc=1)
        plt.subplot(3, 1, 3)
        plt.plot(self.x_features['std'], label="X")
        plt.plot(self.y_features['std'], label="Y")
        plt.plot(self.z_features['std'], label="Z")
        plt.plot(self.SMV_features['std'], label="SMV")
        plt.ylim(-0.05, 0.15)
        plt.title("STD of Data")
        plt.legend(loc=1)
        plt.show()

    def features_graph2(self):

        plt.subplot(4, 1, 1)
        plt.plot(self.x_features['max'], label="X")
        plt.plot(self.y_features['max'], label="Y")
        plt.plot(self.z_features['max'], label="Z")
        plt.plot(self.SMV_features['max'], label="SMV")
        plt.ylim(-1, 1.5)
        plt.title("Max of Data")
        plt.legend(loc=1)
        plt.subplot(4, 1, 2)
        plt.plot(self.x_features['min'], label="X")
        plt.plot(self.y_features['min'], label="Y")
        plt.plot(self.z_features['min'], label="Z")
        plt.plot(self.SMV_features['min'], label="SMV")
        plt.ylim(-1, 1)
        plt.title("Min of Data")
        plt.legend(loc=1)
        plt.subplot(4, 1, 3)
        plt.plot(self.x_features['minmax'], label="X")
        plt.plot(self.y_features['minmax'], label="Y")
        plt.plot(self.z_features['minmax'], label="Z")
        plt.plot(self.SMV_features['minmax'], label="SMV")
        plt.ylim(-0.2, 1.5)
        plt.title("MinMax of Data")
        plt.legend(loc=1)
        plt.subplot(4, 1, 4)
        plt.plot(self.x_features['peak'], label="X")
        plt.plot(self.y_features['peak'], label="Y")
        plt.plot(self.z_features['peak'], label="Z")
        plt.plot(self.SMV_features['peak'], label="SMV")
        plt.ylim(-0.2, 1)
        plt.title("Peak of Data")
        plt.legend(loc=1)
        plt.show()

    def frequency_calc(self):

        fft_array = []
        mean = numpy.mean(self.SMV)

        for i in self.SMV:
            fft_array.append(i - mean)
        fft_out = fft(fft_array)
        fft_freq = fftfreq(len(fft_out), 1 / SAMPLE_FREQ)

        x_freq = numpy.abs(fft_freq)
        y_fft = numpy.abs(fft_out)

        # Plotting IMU angle through Time

        # Plotting Frequency Amplitude (FFT)
        plt.subplot(1, 1, 1)
        plt.plot(x_freq, y_fft, 'b', label='mean smv')
        plt.xlabel("Frequency (Hz)")
        plt.ylabel("Frequency Amplitude")
        plt.xlim(right=20)
        plt.xlim(left=-1)

        # Prints the dominate frequency
        y_max = numpy.argmax(y_fft)
        x_max = x_freq[y_max]
        print(f"Frequency is {x_max}")
        self.FFTFreq = x_max

    def freq_calc_2(self):

        fft_out = fft(self.AccZ)
        fft_freq = fftfreq(len(fft_out), 1 / SAMPLE_FREQ)
        x_freq = numpy.abs(fft_freq)
        y_fft = numpy.abs(fft_out)

        # Plotting IMU angle through Time

        # Plotting Frequency Amplitude (FFT)
        plt.subplot(1, 1, 1)
        plt.plot(x_freq, y_fft, 'r', label="normal single axis")
        plt.xlabel("Frequency (Hz)")
        plt.ylabel("Frequency Amplitude")
        plt.xlim(right=20)
        plt.xlim(left=-1)
        plt.legend()
        plt.show()

    def angle_graph(self):  # graphs the sections that have been trimmed by the movement filter

        plt.plot(self.trimmed_axis, self.Roll, label="Roll")
        plt.plot(self.trimmed_axis, self.Pitch, label="Pitch")
        plt.ylim(-90, 90)
        plt.xlabel("Time (s)")
        plt.ylabel("Angle (*)")
        plt.title("Angle (Pitch, Roll")
        plt.legend(loc=1)
        plt.show()