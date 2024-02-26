class Frailty:

    def __init__(self, parameters, label):

        self.Parameters = parameters.output2
        self.label = label
        self.score = 0
        self.FrailtyIndex()

    def FrailtyIndex(self):

        if self.label == 'up':

            lift_delta =  self.Parameters['Zmin time'] - self.Parameters['Zmax time']
            print(f"{self.Parameters['Zpeak']} Peak Z")
            print(f"{lift_delta} Lift Delta")
            print(f"{self.Parameters['SPARC RMS']} SPARC of Movement")
            print(f"{self.Parameters['Rollrange']} Roll Range")

        elif self.label == 'middle':
            print(f"{self.Parameters['Zlength']} Pouring Length")
            print(f"{self.Parameters['Zpeak']} Peak Z")
            print(f"{self.Parameters['SPARC RMS']} SPARC of Movement")
