from FeatureClass import DataPreparation, Features
import pandas as pd

from datetime import date

current_date = date.today()
print("Current date is:", current_date)

current_csv = 'IMUData.csv'
df = pd.read_csv(current_csv)

new_csv = f'CollectionData/{current_date}-Subject-Trial-Repetition-Comment.csv'
df.to_csv(new_csv, index=False)
print('Saved Data to New File')