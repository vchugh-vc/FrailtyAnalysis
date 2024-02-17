


class Frailty:

    def __init__(self, parameters, label):

        self.Parameters = parameters.output2
        self.label = label
        self.score = 0
        self.FrailtyIndex()


    def FrailtyIndex(self):

        if self.label == 'up':
            print('up')
            self.score = self.Parameters['Zmin time'] - self.Parameters['Zmax time']
            print(self.Parameters['Zpeak'])
            print(self.Parameters['SPARC RMS'])

        elif self.label == 'middle':
            self.score = len(self.Parameters['length'])

        print(self.Parameters)
        print(self.score)

