from MQTT import *
import pandas as pd
from datetime import date
import os

current_date = date.today()
print("Current date is:", current_date)

participant_ID = "P3"
hand = "Non"
trial = "3"

new_csv = f'CollectionData/{current_date}-{participant_ID}-{hand}-{trial}.csv'

if os.path.isfile(new_csv):
    print('File Already Exists')
else:
    mqtt_transmission()
    current_csv = 'IMUData.csv'
    df = pd.read_csv(current_csv)
    df.to_csv(new_csv, index=False)
    print(f'Saved Data to New File to {new_csv}')