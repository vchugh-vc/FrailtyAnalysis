import pandas as pd
import numpy
import matplotlib.pyplot as plt
from FeaturesClass import Features

filename = "IMUData.csv"
plt.rcParams["figure.autolayout"] = True
df = pd.read_csv(filename)
print(df.columns)
IMUAccY = df['AccY']
IMUAccX = df['AccX']
IMUAccZ = df['AccZ']
GyroX = df['GyroX']
GyroY = df['GyroY']
GyroZ = df['GyroZ']
sampling_freq = 130

AccX = Features(IMUAccX, status="raw", name='AccX')
AccY = Features(IMUAccY, status="raw",name='AccY')
AccZ = Features(IMUAccZ, status="raw", name='AccZ')

x_time_filtered = numpy.arange(0, AccX.length / sampling_freq, 1 / sampling_freq)

x_time_window = numpy.arange(0, AccX.length / sampling_freq, 0.4)


def signal_magnitude_vector():
    signal_sum = pow(AccX.AccelData, 2) + pow(AccY.AccelData, 2) + pow(AccZ.AccelData, 2)
    smv_data = numpy.sqrt(signal_sum)
    plt.subplot(3, 1, 2)
    plt.plot(x_time_filtered, smv_data, label='SMV')
    plt.legend()
    plt.xlabel("Time (s)")
    plt.title("Signal Magnitude Vector")
    plt.ylabel("Acceleration (g)")

    return smv_data

SMV = signal_magnitude_vector()


def window_graph_rms(window_data):
    graph_array = []
    for i in window_data:
        graph_variable = Features(i, 'processed', '0')
        graph_array.append(graph_variable.rms_data)
    return graph_array

def window_graph_var(window_data):
    graph_array = []
    for i in window_data:
        graph_variable = Features(i, 'processed', '0')
        graph_array.append(graph_variable.var_data)
    return graph_array

def grapher():
    plt.subplot(3, 1, 1)
    plt.plot(x_time_filtered, AccX.AccelData, label="AccX")
    plt.plot(x_time_filtered, AccY.AccelData, label="AccY")
    plt.plot(x_time_filtered, AccZ.AccelData, label="AccZ")
    plt.legend()
    plt.xlabel("Time (s)")
    plt.title("Acceleration on Different Axis")
    plt.ylabel("Acceleration (g)")

    plt.subplot(3, 1, 3)
    plt.plot(x_time_filtered, AccX.derivative, label="JerkX")
    plt.plot(x_time_filtered, AccY.derivative, label="JerkY")
    plt.plot(x_time_filtered, AccZ.derivative, label="JerkZ")
    plt.legend()
    plt.xlabel("Time (s)")
    plt.title("Jerk on Different Axis")
    plt.ylabel("Jerk (g/s)")

    plt.show()




def grapher_spread():
    x_window_rms = window_graph_rms(AccX.window_data)
    y_window_rms = window_graph_rms(AccY.window_data)
    z_window_rms = window_graph_rms(AccZ.window_data)
    plt.subplot(4, 1, 1)
    plt.plot(x_time_window, x_window_rms,label="X RMS")
    plt.plot(x_time_window, y_window_rms, label="Y RMS")
    plt.plot(x_time_window, z_window_rms, label="Z RMS")
    plt.legend()
    plt.xlabel("Time (s)")
    plt.title("RMS of Acceleration on Diff. Axis")
    plt.ylabel("Acceleration (g)")

    x_window_var = window_graph_var(AccX.window_data)
    y_window_var = window_graph_var(AccY.window_data)
    z_window_var = window_graph_var(AccZ.window_data)
    plt.subplot(4, 1, 2)
    plt.plot(x_time_window, x_window_var,label="X VAR")
    plt.plot(x_time_window, y_window_var, label="Y VAR")
    plt.plot(x_time_window, z_window_var, label="Z VAR")
    plt.legend()
    plt.xlabel("Time (s)")
    plt.title("VAR of Acceleration on Diff. Axis")
    plt.ylabel("Acceleration (g)")
    plt.show()
    plt.show()


grapher()



