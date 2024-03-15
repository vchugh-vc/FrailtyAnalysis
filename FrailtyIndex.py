import numpy
import pandas as pd
import csv
from datetime import datetime

current_time = datetime.now()
formatted_date_time = current_time.strftime("%Y-%m-%d-%H:%M:%S")



file = 'FrailtyParameters.csv'


class Frailty:

    def __init__(self, up_data, middle_data):

        self.UpParameters = up_data.output2
        self.MiddleParameters = middle_data.output2
        self.MiddleSPARC = -self.MiddleParameters['SPARC RMS']
        self.MiddlePeakZAcc = self.MiddleParameters['Zpeak']
        self.MiddlePourTime = self.MiddleParameters['Zlength']
        self.UpRollRange = self.UpParameters['Rollrange']
        self.UpPitchRange = self.UpParameters['Pitchrange']
        self.UpSPARC = - self.UpParameters['SPARC RMS']
        self.UpLiftDelta = self.UpParameters['Zdown peak time'] - self.UpParameters['Zup peak time']
        self.UpPeakZAcc = self.UpParameters['Zpeak']

        self.ScoreData = {}

        self.PrintParameters()
        self.DataFrameParameters()
        self.DataThresholding()

        self.Scoring()

    def DataFrameParameters(self):

        parameters = ['UpAccZ', 'UpDelta', 'UpSPARC', 'UpRoll', 'UpPitch', 'MiddleDelta', 'MiddleAccZ', 'MiddleSPARC']

        for i in parameters:
            self.ScoreData[i] = {'value': 0, 'score': 0}

        self.ScoreData['UpAccZ']['value'] = self.UpPeakZAcc
        self.ScoreData['UpDelta']['value'] = self.UpLiftDelta
        self.ScoreData['UpSPARC']['value'] = self.UpSPARC
        self.ScoreData['UpRoll']['value'] = self.UpRollRange
        self.ScoreData['UpPitch']['value'] = self.UpPitchRange

        self.ScoreData['MiddleDelta']['value'] = self.MiddlePourTime
        self.ScoreData['MiddleAccZ']['value'] = self.MiddlePeakZAcc
        self.ScoreData['MiddleSPARC']['value'] = self.MiddleSPARC

    def PrintParameters(self):

        print("\n----- UP Data -----")
        print(f"{self.UpPeakZAcc} Peak Z")
        print(f"{self.UpLiftDelta} Lift Delta")
        print(f"{self.UpSPARC} SPARC of Movement")
        print(f"{self.UpRollRange} Roll Range")
        print(f"{self.UpPitchRange} Pitch Range")

        print("\n----- Middle Data -----")
        print(f"{self.MiddlePourTime} Pouring Length")
        print(f"{self.MiddlePeakZAcc} Peak Z")
        print(f"{self.MiddleSPARC} SPARC of Movement")

    def DataThresholding(self):

        if self.UpSPARC < 1:
            self.ScoreData['UpSPARC']['score'] = 1
        elif self.UpSPARC > 5:
            self.ScoreData['UpSPARC']['score'] = 0
        else:
            self.ScoreData['UpSPARC']['score'] = (5 - self.UpSPARC) / 4

        if self.MiddleSPARC < 4:
            self.ScoreData['MiddleSPARC']['score'] = 1
        elif self.MiddleSPARC > 10:
            self.ScoreData['MiddleSPARC']['score'] = 0
        else:
            self.ScoreData['MiddleSPARC']['score'] = (10 - self.MiddleSPARC) / 6

        if self.UpRollRange < 5:
            self.ScoreData['UpRoll']['score'] = 1
        elif self.UpRollRange > 20:
            self.ScoreData['UpRoll']['score'] = 0
        else:
            self.ScoreData['UpRoll']['score'] = (20 - self.UpRollRange) / 15

        if self.UpPitchRange < 8:
            self.ScoreData['UpPitch']['score'] = 1
        elif self.UpPitchRange > 25:
            self.ScoreData['UpPitch']['score'] = 0
        else:
            self.ScoreData['UpPitch']['score'] = (25 - self.UpPitchRange) / 17

        if self.MiddlePourTime < 450:
            self.ScoreData['MiddleDelta']['score'] = 1
        elif self.MiddlePourTime > 1000:
            self.ScoreData['MiddleDelta']['score'] = 0
        else:
            self.ScoreData['MiddleDelta']['score'] = (1000 - self.MiddlePourTime) / 550

        if self.UpLiftDelta < 0.25:
            self.ScoreData['UpDelta']['score'] = 1
        elif self.UpLiftDelta > 0.7:
            self.ScoreData['UpDelta']['score'] = 0
        else:
            self.ScoreData['UpDelta']['score'] = (0.7 - self.UpLiftDelta) / 0.45

        if self.UpPeakZAcc < 0.1:
            self.ScoreData['UpAccZ']['score'] = 0
        elif self.UpPeakZAcc < 0.25:
            self.ScoreData['UpAccZ']['score'] = (self.UpPeakZAcc - 0.1) / 0.15
        elif self.UpPeakZAcc < 0.27:
            self.ScoreData['UpAccZ']['score'] = 1
        else:
            self.ScoreData['UpAccZ']['score'] = (0.42 - self.UpPeakZAcc) / 0.15

        if self.MiddlePeakZAcc < 0.4:
            self.ScoreData['MiddleAccZ']['score'] = 0
        elif self.MiddlePeakZAcc < 0.6:
            self.ScoreData['MiddleAccZ']['score'] = (self.MiddlePeakZAcc - 0.4) / 0.2
        elif self.MiddlePeakZAcc < 0.61:
            self.ScoreData['MiddleAccZ']['score'] = 1
        elif self.MiddlePeakZAcc < 0.7:
            self.ScoreData['MiddleAccZ']['score'] = (0.7 - self.MiddlePeakZAcc) / 0.09
        else:
            self.ScoreData['MiddleAccZ']['score'] = 0

        print(self.ScoreData)

    def Scoring(self):

        total = 0
        scores = [formatted_date_time]

        for outer_key, inner_dict in self.ScoreData.items():
            total = total + inner_dict['score']
            scores.append(round(inner_dict['score'],3))

        rough_score = 100 * (total / 8)
        FrailtyScore = numpy.round(rough_score, decimals=2)
        print(FrailtyScore)

        storage = input("Do you want to save the data long term? (Yes/No) ")

        if storage == 'Yes':
            with open(file, 'a', newline='') as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow(scores)


