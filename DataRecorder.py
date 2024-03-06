from MQTT import *
import pandas as pd
from datetime import date

mqtt_transmission()

current_date = date.today()
print("Current date is:", current_date)

current_csv = 'IMUData.csv'
df = pd.read_csv(current_csv)

participant_ID = ""
hand = ""
trial = ""

new_csv = f'CollectionData/{current_date}-{participant_ID}-{hand}-{trial}.csv'
df.to_csv(new_csv, index=False)
print(f'Saved Data to New File to {new_csv}')