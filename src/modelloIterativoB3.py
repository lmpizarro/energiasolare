import math
import bdModulos
import constants
import moduloFv as fvm
import companionSim as comp
import modelloBase as MB
import modelloAmbiente as AMB

class modelloB3(MB.ModelloBase):

    def __init__(self, m, ambient):

        super(modelloB3, self).__init__(m, ambient)

        self.cIi = 1.00
        self.Rs = (self.deltav / self.m.Imp)  

        self.Rsh = self.m.Voc / self.deltai

        self.Ii = self.cIi * self.m.Isc

        self.nref = 1.0

        self.Vt = self.m.Ns * self.nref * constants.KK * self.T / constants.qq

        self.I0 = self.calcI0()

        m.esp["modelli"] = []

        
    def calcI0(self):
        return (self.Ii - (self.m.Voc / self.Rsh)) / (math.exp(self.m.Voc /self.Vt) - 1 )

    def calcCurrrent(self, I, V):
        Ii = self.Ii
        I0 = self.I0
        Rs = self.Rs
        Rsh = self.Rsh

        Vt = self.Vt

        return Ii - I0 * (math.exp((V + I * Rs) / Vt) - 1) - (V + I * Rs) / Rsh

    def calcDeltaIsc (self):
        return self.m.Isc  - (self.Ii - self.I0 * (math.exp(self.m.Isc * self.Rs / self.Vt) - 1) - \
                self.m.Isc * self.Rs / self.Rsh)

    def calcDeltaVoc (self):
        return self.m.Voc  - self.Rsh * (self.Ii - self.I0 *\
                (math.exp(self.m.Voc/self.Vt)-1))

    def calcDeltaImp (self):
        Imp = self.m.Imp
        Vmp = self.m.Vmp

        return self.m.Imp  - self.calcCurrrent(Imp, Vmp) 

    def ajustaIsc(self):

        deltaIsc = self.calcDeltaIsc()
        
        i = 0
        if deltaIsc > 0.0001:
            print "deltaIsc > 0.0001"
            while deltaIsc > 0.0001:
                self.cIi = self.cIi + 0.00001
                self.Ii = self.cIi * self.m.Isc
                self.I0 = self.calcI0()
                deltaIsc = self.calcDeltaIsc()

        if deltaIsc < -0.0001:
            print "deltaIsc < -0.0001"
            while deltaIsc < -0.0001:
                self.cIi = self.cIi - 0.00001
                self.Ii = self.cIi * self.m.Isc
                self.I0 = self.calcI0()
                deltaIsc = self.calcDeltaIsc()


    def ajustaVoc(self):
        deltaVoc =  self.calcDeltaVoc() 
        print "deltaVOC init", deltaVoc

        if deltaVoc < -0.0001:
            print "deltaVoc < -0.0001: ", deltaVoc
            while deltaVoc < -0.0001:
                self.nref = self.nref - 0.0001
                self.Vt = self.m.Ns * self.nref * constants.KK * self.T / constants.qq
                self.I0 = self.calcI0()
                #self.ajustaIsc()
                deltaVoc =  self.calcDeltaVoc()   

        if deltaVoc > 0.0001:
            print "deltaVoc > 0.0001: ", deltaVoc
            while deltaVoc > 0.0001:
                self.nref = self.nref + 0.0001
                self.Vt = self.m.Ns * self.nref * constants.KK * self.T / constants.qq
                self.I0 = self.calcI0()
                #self.ajustaIsc()
                deltaVoc =  self.calcDeltaVoc()   

    def ajustaMPP(self):
        deltaMPP = self.calcDeltaImp()

        if deltaMPP > 0.0:
            print "deltaMPP > 0", deltaMPP 
            while deltaMPP > 0:
                #print "deltaMPP > 0", deltaMPP 
                self.Rs = self.Rs - 0.001 
                self.Rsh = self.Rsh +   .1
                self.I0 = self.calcI0()
                #self.ajustaVoc()
                deltaMPP = self.calcDeltaImp()

    def ajusta (self):
        self.ajustaIsc()
        self.ajustaMPP()
        self.ajustaVoc()
        self.ajustaMPP()

        #self.ajustaVoc()
        self.m.esp["modelli"].append({"Rs":self.Rs, "Rsh": self.Rsh, "nref": self.nref,\
                "source": "B2", "Iirr": self.Ii, "I0": self.I0})

    def __str__(self):    
        str1 = ("Rsh: %.3f Rs: %.3f nref: %.3f Ii: %.3f I0: %.3e\n")%\
                (self.Rsh, self.Rs, self.nref, self.Ii, self.I0)
        return str1

def testB3():
    Ta = 30
    Ws = 4
    Ss = 1500

    ambient = AMB.Ambient (Ta, Ss, Ws)
    ambient.setModelo (4)

    md1 = fvm.Modulo(bdModulos.eschedaTecnica4)

    print (md1)
    mbcMd3 = modelloB3(md1, ambient)
    print(mbcMd3)

    mbcMd3.ajusta()
    mbcMd3.ajusta()

    print(mbcMd3)

    mod1 = comp.Companion(md1.esp, 1000, Ta)
    mod1.caclCircuit(80)

def testCompanionB3():

    indexModel = 4
    Ta = 20
    Ws = 4
    Ss = 1500

    ambient = fvm.Ambient (Ta, Ss, Ws)
    ambient.setModelo (4)

    md1 = fvm.Modulo(bdModulos.eschedaTecnica1)
    mbcMd3 = modelloB3(md1, ambient)
    print md1.esp 

    mod1 = comp.Companion(md1.esp, 1000, Ta)

    mod1.caclCircuit(80, "open")
    mod1.caclCircuit(80, "short")
    mod1.calcMpp()

if __name__ == '__main__':
    print ("testB3")
    testB3()
