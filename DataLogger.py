import serial
import time

arduino_port = "/dev/tty.usbmodem142101"
baud = 57600
fileName = "IMUData.csv"

DATA_POINTS = 3000

ser = serial.Serial(arduino_port, baud)
print("Connected to Arduino port:" + arduino_port)
file = open(fileName, "w")
print("Created file")

total = 0

while total < DATA_POINTS:

    if total == 1:
        print("Starting Data")
        print(time.time())
    if total == 2999:
        print(time.time())
    getData = ser.readline()
    data = str(getData)
    formatted = data[2:-5]
    #print(formatted)

    file.write(formatted + "\n")
    total += 1

print("Finished")