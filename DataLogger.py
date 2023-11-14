import serial
import time

arduino_port = "/dev/tty.usbmodem142101"
baud = 57600
fileName = "IMUData.csv"

DATA_POINTS = 500

ser = serial.Serial(arduino_port, baud)
print("Connected to Arduino port:" + arduino_port)
file = open(fileName, "w")
print("Created file")

total = 0

while total < DATA_POINTS:

    if total == 1:
        print("Starting Data")
        START = time.time()
        print(START)
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