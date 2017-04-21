# coding: utf-8

import math
import moduloFv as mFV
import bdModulos
import constants
import modelloAmbiente as AMB

class OneDiodeModel(object):
    def __init__(self, modulo, index, Temp):

        self.modulo = modulo

        if index == 1000:
            self.modello = self.modulo.esp["modelli"][-1]
        else:    
            self.modello = self.modulo.esp["modelli"][index]

        '''
        Ns: number of cells in serie
        Rs: R serie Ohm 
        Rsh: R shunt Ohm 
        I0: diode reverse saturation current Amp
        n: ideality factor
        T : ° Kelvin
        '''
        self.Ns = self.modulo.Ns 
        self.Rs = self.modello["Rs"]
        self.Rsh = self.modello["Rsh"]
        self.n = self.modello["nref"]
        self.I0 = self.modello["I0"]
        self.Ii = self.modello["Iirr"]
        self.Temp = Temp
        self.A = constants.qq / (self.n * constants.KK * self.Temp)

    def __str__(self):
        format_ = "Rs: %.3f Rsh: %.3f n: %.3f I0: %.3e T: %.3f A: %.3f"
        str1 = (format_)%(self.Rs, self.Rsh, self.n, self.I0, self.Temp, self.A)
        return (str1)

    def current01(self, V):
        return (self.Ii - self.I0*math.exp(self.A * V / self.Ns))

    def current02(self, V):
        a = self.Rsh / (self.Rsh + self.Rs)
        return a * (self.current01(V) - V/ self.Rsh)


def testOneDiodeModel():    
    # Rs, Rsh, n, I0, Temp
    Ta = 30
    Ws = 4
    Ss = 1500

    ambient = AMB.Ambient (Ta, Ss, Ws)

    md4 = mFV.Modulo(bdModulos.eschedaTecnica4)
    md4.setAmbient(ambient)
    T = ambient.getTemperatura(4)

    odm = OneDiodeModel(md4, 0, T + 273.16)

    V = 0.0
    Il = 0.0
    Wp = 0.0

    while Il >= 0:  
        Il = odm.current01(V)
        Il2 = odm.current02(V)
        Wp = V * Il
        print  ("%.3f %.3f %.3f %.3f %.3f")%(V, Il, Wp, Il2, Il2 * V)
        V = V + 0.01

if __name__ == '__main__':
    testOneDiodeModel()
