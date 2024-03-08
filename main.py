from MQTT import *
from FeatureClass import *
from DTW import *
from FrailtyIndex import *

if __name__ == "__main__":
    mqtt_transmission()
    FilteredData = DataPreparation()
    AccZ = FilteredData.AccZ_Trimmed
    AccX = FilteredData.AccX_Trimmed
    DTWPhases = DataTimeWarping(AccZ, AccX)
    TimeStamps = DTWPhases.movement_stamps
    up_data = Features(FilteredData, TimeStamps, 'up')
    middle_data = Features(FilteredData, TimeStamps, 'middle')
    Frailty(up_data, middle_data)
