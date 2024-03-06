import serial
import time

arduino_port = "/dev/tty.usbmodem142101"
baud = 57600
fileName = "IMUData.csv"

DATA_POINTS = 2000

ser = serial.Serial(arduino_port, baud)
print("Connected to Arduino port:" + arduino_port)
file = open(fileName, "w")
print("Created file")

total = 0
i = 0

file.write("Time,AccX,AccY,AccZ,GyroX,GyroY,GyroZ\n")

while i < 500:  # Adds arbitrary data that to be Processed by the Butterworth Filter
    file.write(f"{i},0,0,1,0,0,0 \n")
    i += 1


while total < DATA_POINTS:

    if total == 1:
        print("Starting Data")
        START = time.time()
        print(START)
        print("Move")
    # if total == 400:
    #     print("Move")
    if total == DATA_POINTS - 1 :
        END = time.time()
        print(END)
    getData = ser.readline()
    data = str(getData)
    formatted = data[2:-5]
    #print(formatted)

    file.write(formatted + "\n")
    total += 1

print("Finished")
duration = END - START

from FeatureClass import DataPreparation, Features

FilteredData = DataPreparation()
DataFeatures = Features(FilteredData)
print(DataFeatures.FFTFreq)