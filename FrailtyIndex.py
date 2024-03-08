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

        print(self.UpParameters)
        print(self.MiddleParameters)
        self.PrintParameters()



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

