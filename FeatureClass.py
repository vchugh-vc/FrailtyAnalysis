import pandas as pd
import numpy
import matplotlib.pyplot as plt
from numpy.fft import fft, fftfreq
from scipy import signal

SAMPLE_TIME = 0.0096
SAMPLE_FREQ = 104
SENSE = 0.01
SENSE_START = 0.015
SENSE_STOP = 0.015

IMUFile = 'IMUData.csv'


class DataPreparation:

    def __init__(self, file=IMUFile):

        filename = file
        plt.rcParams["figure.autolayout"] = True
        df = pd.read_csv(filename)
        IMUAccY = df['AccY']
        IMUAccX = df['AccX']
        IMUAccZ = df['AccZ']
        IMUGyroX = df['GyroX']
        IMUGyroY = df['GyroY']
        IMUGyroZ = df['GyroZ']
        IMURoll = df['Roll']
        IMUPitch = df['Pitch']

        self.AccX_Trimmed = None
        self.AccY_Trimmed = None
        self.AccZ_Trimmed = None
        self.SMV_Trimmed = None
        self.Jerk_Trimmed = None
        self.GyroX_Trimmed = None
        self.GyroY_Trimmed = None
        self.GyroZ_Trimmed = None
        self.Pitch_Trimmed = None
        self.Roll_Trimmed = None
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
        self.time_axis_trimmed = []
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
            plt.suptitle('Raw Movement Graph')
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
        self.SMV_roll = numpy.convolve(self.SMV, numpy.ones(30), 'same') / 30
        # self.movement_filter()
        self.movement_filter2()

    def movement_filter(
            self):  # Detects when movement has started or stopped based on previous values (of rolling SMV) at a
        # given threshold

        start = []  # used for if there are multiple start stops in a movement pattern
        stop = []
        start.append(0)
        for i in range(4, len(self.SMV_roll)):
            if self.SMV_roll[i] > SENSE > self.SMV_roll[i - 4] and self.SMV_roll[i - 2] > SENSE and self.SMV_roll[
                i - 1] > SENSE and self.SMV_roll[i - 3] > SENSE:
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

    def movement_filter2(self):  # Detects when movement based on previous values (of rolling SMV) at a given threshold

        time_data = {}

        for i in range(4, len(self.SMV_roll)):
            if (self.SMV_roll[i] > SENSE_START > self.SMV_roll[i - 4] and self.SMV_roll[i - 2] > SENSE_START and
                    self.SMV_roll[
                        i - 1] > SENSE_START and self.SMV_roll[i - 3] > SENSE_START):
                print(f"2 Started movement at {i * SAMPLE_TIME} : {i}")
                time_data[i] = 'start'

            elif self.SMV_roll[i] < SENSE_STOP < self.SMV_roll[i - 4] and self.SMV_roll[i - 2] < SENSE_STOP and \
                    self.SMV_roll[
                        i - 1] < SENSE_STOP and self.SMV_roll[i - 3] < SENSE_STOP:
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

        time_data[0] = 'start'

        if 'stop' in values:
            print('stop is there')
        else:
            time_data[len(self.SMV_roll)] = 'stop'

        time_data[len(self.SMV_roll)] = 'stop'

        time_data_sorted = sorted(
            time_data.items())  # used to sort the dictionary by time stamp (preserves order of data)

        time_data_order = {key: value for key, value in time_data_sorted}  # new ordered dictionary of time stamps

        keys = list(time_data_order.keys())
        values = list(time_data_order.values())

        status = None  # checks for sequence of starts and stops
        for timestamp, event in time_data_order.items():
            if event == 'start':
                start_time = timestamp
                status = 'start'
            elif event == 'stop' and status is not None:
                clips.append([start_time, timestamp])
                status = None

        # for i in range(len(values) - len(sequence) + 1):  # Checks for start-stop sequence
        #     if values[i:i + len(sequence)] == sequence:
        #         clips.append(keys[i:i + len(sequence)])

        print(f"Clips {clips}")

        for i in range(min(len(clips), len(clips))):  # calculates the longest period of movement to select
            start_time = clips[i][0]
            stop_time = clips[i][1]
            duration = stop_time - start_time
            diff_movements[i] = {'duration': duration, 'start': start_time, 'stop': stop_time}

            # if duration > longest_duration:
            #     longest_duration = duration
            #     movement_start = start_time
            #     movement_stop = stop_time

        movement_start = None
        movement_stop = None

        for k, v in diff_movements.items():  # Calculates the SMV (RMS) value for each movement clip
            array = self.SMV[v['start']:v['stop']]
            array_rms = numpy.sqrt(numpy.mean(array ** 2))
            v['SMV'] = numpy.round(array_rms, 3)
            v['Movement'] = numpy.round(v['duration'] * v['SMV'], 3)
            if movement_start is None and v['Movement'] > 20:
                movement_start = v['start']
            if v['Movement'] > 10:
                movement_stop = v['stop']

        print(diff_movements)
        print(
            f"From {movement_start * SAMPLE_TIME} ({movement_start}) to {movement_stop * SAMPLE_TIME} ({movement_stop})")

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
        self.time_axis_trimmed = numpy.arange(0, (len(self.AccX_Trimmed) / SAMPLE_FREQ),
                                              1 / SAMPLE_FREQ)


class Features:

    def __init__(self, ProcessedData, timestamps, label):

        self.label = label
        self.RawAccX = ProcessedData.AccX_Trimmed
        self.RawAccY = ProcessedData.AccY_Trimmed
        self.RawAccZ = ProcessedData.AccZ_Trimmed
        self.RawSMV = ProcessedData.SMV_Trimmed
        self.RawJerk = ProcessedData.Jerk_Trimmed
        self.RawGyroX = ProcessedData.GyroX_Trimmed
        self.RawGyroY = ProcessedData.GyroY_Trimmed
        self.RawGyroZ = ProcessedData.GyroZ_Trimmed
        self.RawRoll = ProcessedData.Roll_Trimmed
        self.RawPitch = ProcessedData.Pitch_Trimmed

        self.timestamps = timestamps
        if self.label == 'up':
            self.start = timestamps[0]
            self.stop = timestamps[3]
        else:
            self.start = timestamps[4]
            self.stop = timestamps[5]



        self.AccX = self.RawAccX[self.start:self.stop]
        self.AccY = self.RawAccY[self.start:self.stop]
        self.AccZ = self.RawAccZ[self.start:self.stop]
        self.SMV = self.RawSMV[self.start:self.stop]
        self.Jerk = self.RawJerk[self.start:self.stop]
        self.GyroX = self.RawGyroX[self.start:self.stop]
        self.GyroY = self.RawGyroY[self.start:self.stop]
        self.GyroZ = self.RawGyroZ[self.start:self.stop]
        self.Roll = self.RawRoll[self.start:self.stop]
        self.Pitch = self.RawPitch[self.start:self.stop]

        self.SparcX = self.sparc(self.GyroZ)
        self.SparcY = self.sparc(self.GyroX)
        self.SparcZ = self.sparc(self.GyroY)
        self.SPARC_RMS = (self.SparcZ[0] + self.SparcX[0] + self.SparcY[0]) / 3

        # print(f"Total = {self.SPARC_RMS}, X = {self.SparcX[0]}, Y = {self.SparcY[0]}, Z = {self.SparcZ[0]}")

        self.time = len(self.SMV) * SAMPLE_TIME
        self.trimmed_axis = numpy.arange(0, len(self.AccX) / SAMPLE_FREQ,
                                         1 / SAMPLE_FREQ)
        # self.graph_trimmed()

        self.FFTFreq = 0

        self.x_features = {}
        self.y_features = {}
        self.z_features = {}
        self.roll_features = {}
        self.pitch_features = {}
        self.frequency_calc()
        self.freq_calc_2()

        self.data_extraction(self.AccZ, self.z_features)
        self.data_extraction(self.AccY, self.y_features)
        self.data_extraction(self.AccX, self.x_features)
        self.data_extraction(self.Roll, self.roll_features)
        self.data_extraction(self.Pitch, self.pitch_features)

        self.output2 = {}

        self.dictionary_combine()
        # self.angle_graph()

    def graph_trimmed(self):  # graphs the sections that have been trimmed by the movement filter

        if (len(self.trimmed_axis)) > len(self.AccX):
            last = len(self.trimmed_axis) - 1
            self.trimmed_axis = self.trimmed_axis[:last]

        plt.suptitle('Individual Movement Phase Graph')
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

    def minmax_spread(self, array, dictionary):  # Returns Min-Max Data of an Array
        max_data = max(array)
        max_time = numpy.where(array == max_data)[0]
        if len(max_time) > 1:
            max_time = max_time[0]

        min_data = min(array)
        min_time = numpy.where(array == min_data)[0]
        if len(min_time) > 1:
            min_time = min_time[0]

        minmax_data = max_data - min_data

        peak_data = max(max_data, numpy.abs(min_data))
        peak_time = numpy.where(array == peak_data)[0]
        if len(peak_time) == 0:
            peak_time = numpy.where(array == -peak_data)[0]
        elif len(peak_time) > 1:
            peak_time = peak_time[0]

        rms_data = numpy.sqrt(numpy.mean(array ** 2))
        std_data = numpy.nanstd(array)
        var_data = numpy.nanvar(array)

        dictionary['max'] = max_data
        dictionary['max time'] = max_time.item() * SAMPLE_TIME
        dictionary['min'] = min_data
        dictionary['min time'] = min_time.item() * SAMPLE_TIME
        dictionary['range'] = minmax_data
        dictionary['peak'] = peak_data
        dictionary['peak time'] = peak_time.item() * SAMPLE_TIME
        dictionary['up peak'] = self.AccZ[self.timestamps[1]]
        dictionary['up peak time'] = self.timestamps[1] * SAMPLE_TIME
        dictionary['down peak'] = self.AccZ[self.timestamps[2]]
        dictionary['down peak time'] = self.timestamps[2] * SAMPLE_TIME
        dictionary['rms'] = rms_data
        dictionary['std'] = std_data
        dictionary['var'] = var_data
        dictionary['length'] = len(self.AccZ)
        dictionary['freq'] = self.FFTFreq

    def data_extraction(self, array, dictionary):
        self.minmax_spread(array, dictionary)
        # print(dictionary)

    def dictionary_combine(self):

        axis = [self.x_features, self.y_features, self.z_features, self.roll_features, self.pitch_features]

        for i in range(len(axis)):
            for keys, values in axis[i].items():
                if i == 0:
                    label = 'X'
                elif i == 1:
                    label = 'Y'
                elif i == 2:
                    label = 'Z'
                elif i == 3:
                    label = 'Roll'
                elif i ==4:
                    label = "Pitch"
                # print(f"{label}{keys} : {values}")
                self.output2[f"{label}{keys}"] = values

        self.output2['Freq'] = self.FFTFreq
        self.output2['SPARC X'] = self.SparcX[0]
        self.output2['SPARC Y'] = self.SparcY[0]
        self.output2['SPARC Z'] = self.SparcZ[0]
        self.output2['SPARC RMS'] = self.SPARC_RMS

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
        # plt.subplot(1, 1, 1)
        # plt.plot(x_freq, y_fft, 'b', label='mean smv')
        # plt.xlabel("Frequency (Hz)")
        # plt.ylabel("Frequency Amplitude")
        # plt.xlim(right=20)
        # plt.xlim(left=-1)
        # plt.show()

        # Prints the dominate frequency
        y_max = numpy.argmax(y_fft)
        x_max = x_freq[y_max]
        # print(f"Frequency is {x_max}")
        self.FFTFreq = x_max

    def freq_calc_2(self):

        fft_out = fft(self.AccZ)
        fft_freq = fftfreq(len(fft_out), 1 / SAMPLE_FREQ)
        x_freq = numpy.abs(fft_freq)
        y_fft = numpy.abs(fft_out)

        y_max = numpy.argmax(y_fft)
        x_max = x_freq[y_max]
        # print(f"Frequency is {x_max}")
        print(f"New Freq Calc {self.label}: {x_max}")

        # Plotting IMU angle through Time

        # Plotting Frequency Amplitude (FFT)
        # plt.subplot(1, 1, 1)
        # plt.plot(x_freq, y_fft, 'r', label="normal single axis")
        # plt.xlabel("Frequency (Hz)")
        # plt.ylabel("Frequency Amplitude")
        # plt.xlim(right=20)
        # plt.xlim(left=-1)
        # plt.legend()
        # plt.show()

    def angle_graph(self):  # graphs the sections that have been trimmed by the movement filter

        plt.suptitle('Pitch & Roll of Movement Phase Graph')

        plt.plot(self.trimmed_axis, self.Roll, label="Roll")
        plt.plot(self.trimmed_axis, self.Pitch, label="Pitch")
        plt.ylim(-90, 90)
        plt.xlabel("Time (s)")
        plt.ylabel("Angle (*)")
        plt.title("Angle (Pitch, Roll")
        plt.legend(loc=1)
        plt.show()

    def sparc(self, movement, fs=104, padlevel=4, fc=10.0, amp_th=0.05):

        # Number of zeros to be padded.
        nfft = int(pow(2, numpy.ceil(numpy.log2(len(movement))) + padlevel))

        # Frequency
        f = numpy.arange(0, fs, fs / nfft)
        # Normalized magnitude spectrum
        Mf = abs(numpy.fft.fft(movement, nfft))
        Mf = Mf / max(Mf)

        fc_inx = ((f <= fc) * 1).nonzero()
        f_sel = f[fc_inx]
        Mf_sel = Mf[fc_inx]

        inx = ((Mf_sel >= amp_th) * 1).nonzero()[0]
        fc_inx = range(inx[0], inx[-1] + 1)
        f_sel = f_sel[fc_inx]
        Mf_sel = Mf_sel[fc_inx]

        # Calculate arc length
        new_sal = -sum(numpy.sqrt(pow(numpy.diff(f_sel) / (f_sel[-1] - f_sel[0]), 2) +
                                  pow(numpy.diff(Mf_sel), 2)))

        # plt.subplot(2, 1, 1)
        # plt.plot(f, Mf)
        # plt.xlim(-1, 20)
        # plt.subplot(2, 1, 2)
        # plt.plot(f_sel, Mf_sel)
        # plt.xlim(-1, 20)
        # plt.show()

        # print(f"Arc Length {new_sal}, Frequ {f}, Magn. {Mf}")
        return [new_sal, (f, Mf), (f_sel, Mf_sel)]
