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

        # massimo
        self.Rs = self.deltav / m.Imp

        self.Ii = m.Isc * (self.Rs + self.Rsh)/self.Rsh 
 
        self.Vt = m.Ns * constants.KK * self.T / constants.qq

        self.nref =  1.0

        self.I0 = (self.Ii - m.Voc / self.Rsh) / (math.exp(m.Voc / self.Vt) - 1)


    def __str__(self):    
        str1 = ("Rsh: %.3f Rs: %.3f nref: %.3f Ii: %.3f I0: %.3e\n")%\
                (self.Rsh, self.Rs,self.nref, self.Ii, self.I0)
        return str1

    def setModello(self):

        if "modelli" not in self.m.esp.keys():
            self.m.esp["modelli"] = []

        self.m.esp["modelli"].append({"Rs":self.Rs, "Rsh": self.Rsh, "nref": self.nref,\
                "source": "B2", "Iirr": self.Ii, "I0": self.I0})
 
