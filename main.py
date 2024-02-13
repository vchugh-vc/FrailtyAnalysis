from MQTT import *
from FeatureClass import *
from DTW import *




if __name__ == "__main__":
    mqtt_transmission()
    FilteredData = DataPreparation()
    AccZ = FilteredData.AccZ_Trimmed
    DTWPhases = DataTimeWarping(AccZ)
    up = [DTWPhases.movement_stamps[0],DTWPhases.movement_stamps[1]]
    middle = [DTWPhases.movement_stamps[1], DTWPhases.movement_stamps[2]]
    down = [DTWPhases.movement_stamps[2], DTWPhases.movement_stamps[3]]