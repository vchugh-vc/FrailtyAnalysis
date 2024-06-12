from MQTT import *
import pandas as pd
from datetime import datetime
current_time = datetime.now()
import os

current_date = current_time.today()
print("Current date is:", current_date)
formatted_time = current_date.strftime("%Y-%m-%d %H:%M:%S")
print("Formatted current date and time:", formatted_time)

participant_ID = "P10"
hand = "Non-L"
trial = "T150"

new_csv = f'LongitudinalData/{formatted_time}-{trial}.csv'
new_csv = 'Graph.csv'

if os.path.isfile(new_csv):
    print('File Already Exists')
else:
    mqtt_transmission()
    current_csv = 'IMUData.csv'
    df = pd.read_csv(current_csv)
    df.to_csv(new_csv, index=False)
    print(f'Saved Data to New File to {new_csv}')

