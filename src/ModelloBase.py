# coding: utf-8
import math
import constants

class ModelloBase(object):
    def __init__(self, m, ambient):
        self.m = m
        self.T =  ambient.Ta + 273.16

        self.deltav = m.Voc - m.Vmp
        self.deltai = m.Isc - m.Imp

        # minimo
        self.Rsh = (m.Vmp) / self.deltai

        self.Vt = m.Ns * constants.KK * self.T / constants.qq

        self.Rs = self.deltav / self.m.Imp
        self.RsM =  self.Rs

        self.calcIi ()

        self.calcI0()        

        self.calcRs()

 

        self.nref =  1.0


    def calcIi(self):
        Ii =  self.m.Isc * (self.Rs + self.Rsh)/self.Rsh

        if Ii > self.m.Isc:
            self.Ii = Ii
        else:
            self.Ii = Ii * 1.001

    def calcI0(self):        
        self.I0 = (self.Ii - self.m.Voc / self.Rsh) / (math.exp(self.m.Voc / self.Vt) - 1)

    def calcRs(self):   
        # massimo
        pass
        

    def __str__(self):    
        str1 = ("Rsh: %.3f Rs: %.3f nref: %.3f Ii: %.3f I0: %.3e\n")%\
                (self.Rsh, self.Rs,self.nref, self.Ii, self.I0)
        return str1

    def setModello(self):

        if "modelli" not in self.m.esp.keys():
            self.m.esp["modelli"] = []

        self.m.esp["modelli"].append({"Rs":self.Rs, "Rsh": self.Rsh, "nref": self.nref,\
                "source": "B2", "Iirr": self.Ii, "I0": self.I0})

def testB4():
    pass

if __name__ == '__main__':
    testB4()
