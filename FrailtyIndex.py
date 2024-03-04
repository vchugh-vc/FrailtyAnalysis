class Frailty:

    def __init__(self, parameters, label):

        self.Parameters = parameters.output2
        self.label = label
        self.score = 0
        self.FrailtyIndex()

    def FrailtyIndex(self):

        if self.label == 'up':

            print("\n----- UP Data -----")
            lift_delta = self.Parameters['Zdown peak time'] - self.Parameters['Zup peak time']
            print(f"{self.Parameters['Zpeak']} Peak Z")
            print(f"{lift_delta} Lift Delta")
            print(f"{self.Parameters['SPARC RMS']} SPARC of Movement")
            print(f"{self.Parameters['Rollrange']} Roll Range")
            print(f"{self.Parameters['Zfreq']} Frequency")

        elif self.label == 'middle':
            print("\n----- Middle Data -----")
            print(f"{self.Parameters['Zlength']} Pouring Length")
            print(f"{self.Parameters['Zpeak']} Peak Z")
            print(f"{self.Parameters['SPARC RMS']} SPARC of Movement")
            print(f"{self.Parameters['Zfreq']} Frequency")
