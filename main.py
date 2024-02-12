from MQTT import *
from FeatureClass import *
from DTW import *
import time




if __name__ == "__main__":
    mqtt_transmission()
    FilteredData = DataPreparation()
    AccZ = FilteredData.AccZ_Trimmed
    DataTimeWarping(AccZ)
    print("DTW")