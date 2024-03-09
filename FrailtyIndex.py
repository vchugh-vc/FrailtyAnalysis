import numpy

class Frailty:

    def __init__(self, up_data, middle_data):

        self.UpParameters = up_data.output2
        self.MiddleParameters = middle_data.output2
        self.MiddleSPARC = -self.MiddleParameters['SPARC RMS']
        self.MiddlePeakZAcc = self.MiddleParameters['Zpeak']
        self.MiddlePourTime = self.MiddleParameters['Zlength']
        self.UpRollRange = self.UpParameters['Rollrange']
        self.UpSPARC = - self.UpParameters['SPARC RMS']
        self.UpLiftDelta = self.UpParameters['Zdown peak time'] - self.UpParameters['Zup peak time']
        self.UpPeakZAcc = self.UpParameters['Zpeak']

        self.score = {}

        self.PrintParameters()
        self.DataThresholding()
        self.Scoring()

    def PrintParameters(self):

        print("\n----- UP Data -----")
        print(f"{self.UpPeakZAcc} Peak Z")
        print(f"{self.UpLiftDelta} Lift Delta")
        print(f"{self.UpSPARC} SPARC of Movement")
        print(f"{self.UpRollRange} Roll Range")

        print("\n----- Middle Data -----")
        print(f"{self.MiddlePourTime} Pouring Length")
        print(f"{self.MiddlePeakZAcc} Peak Z")
        print(f"{self.MiddleSPARC} SPARC of Movement")

    def DataThresholding(self):

        if self.UpSPARC < 1:
            self.score['UpSPARC'] = 1
        elif self.UpSPARC > 5:
            self.score['UpSPARC'] = 0
        else:
            self.score['UpSPARC'] = (5 - self.UpSPARC) / 4

        if self.MiddleSPARC < 4:
            self.score['MiddleSPARC'] = 1
        elif self.MiddleSPARC > 10:
            self.score['MiddleSPARC'] = 0
        else:
            self.score['MiddleSPARC'] = (10 - self.MiddleSPARC) / 6

        if self.UpRollRange < 5:
            self.score['UpRollRange'] = 1
        elif self.UpRollRange > 30:
            self.score['UpRollRange'] = 0
        else:
            self.score['UpRollRange'] = (30 - self.UpRollRange) / 25

        if self.MiddlePourTime < 450:
            self.score['MiddlePourTime'] = 1
        elif self.MiddlePourTime > 1000:
            self.score['MiddlePourTime'] = 0
        else:
            self.score['MiddlePourTime'] = (1000 - self.MiddlePourTime) / 550

        if self.UpLiftDelta < 0.25:
            self.score['UpLiftDelta'] = 1
        elif self.UpLiftDelta > 0.7:
            self.score['UpLiftDelta'] = 0
        else:
            self.score['UpLiftDelta'] = (0.7 - self.UpLiftDelta) / 0.45

        if self.UpPeakZAcc < 0.1:
            self.score['UpPeakZAcc'] = 0
        elif self.UpPeakZAcc < 0.25:
            self.score['UpPeakZAcc'] = (self.UpPeakZAcc - 0.1) / 0.15
        elif self.UpPeakZAcc < 0.27:
            self.score['UpPeakZAcc'] = 1
        else:
            self.score['UpPeakZAcc'] = (0.42 - self.UpPeakZAcc) / 0.15

        if self.MiddlePeakZAcc < 0.4:
            self.score['MiddlePeakZAcc'] = 0
        elif self.MiddlePeakZAcc < 0.55:
            self.score['MiddlePeakZAcc'] = (self.MiddlePeakZAcc - 0.4) / 0.15
        elif self.MiddlePeakZAcc < 0.6:
            self.score['MiddlePeakZAcc'] = 1
        else:
            self.score['MiddlePeakZAcc'] = (0.7 - self.MiddlePeakZAcc) / 0.1

        print(f"\n{self.score}")

    def Scoring(self):

        total = 0

        for key, value in self.score.items():
            total = total + value

        rough_score = 100 * (total / 7)
        FrailtyScore = numpy.round(rough_score, decimals=2)
        print(FrailtyScore)

