# coding: utf-8

import math
import moduloFv as mFV
import bdModulos
import constants

class OneDiodeModel(object):
    def __init__(self,eschedaTecnica, model, T):
        '''
        Ns: number of cells in serie
        Rs: R serie Ohm 
        Rsh: R shunt Ohm 
        I0: diode reverse saturation current Amp
        n: ideality factor
        T : ° Kelvin
        '''
        Ns = eschedaTecnica["CaratteristicheMeccaniche"]["cell"]
        modelli = eschedaTecnica["modelli"][model]
        self.Ns = Ns
        self.Rs = modelli["Rs"]
        self.Rsh = modelli["Rsh"]
        self.n = modelli["nref"]
        self.I0 = modelli["I0"]
        self.T = T
        self.A = constants.qq / (self.n * constants.KK * self.T)

    def __str__(self):
        format_ = "Rs: %.3f Rsh: %.3f n: %.3f I0: %.3e T: %.3f A: %.3f"
        str1 = (format_)%(self.Rs, self.Rsh, self.n, self.I0, self.T, self.A)
        return (str1)

    def current01(self, V):
        return (self.Iph - self.I0*math.exp(self.A * V / self.Ns))

    def current02(self, V):
        a = self.Rsh / (self.Rsh + self.Rs)
        return a * (self.current01(V) - V/ self.Rsh)

    def setIph (self, Iph):
        self.Iph = Iph


def testOneDiodeModel():    
    # Rs, Rsh, n, I0, T
    Ta = 30
    Ws = 4
    Ss = 1500

    ambient = mFV.Ambient (Ta, Ss, Ws)

    md4 = mFV.Modulo(bdModulos.eschedaTecnica4)
    md4.setAmbient(ambient)
    T = md4.temperatura(4)

    odm = OneDiodeModel(bdModulos.eschedaTecnica4, 0, T + 273.16)

    V = 0.0
    Il = 0.0
    Wp = 0.0
    odm.setIph(8.6)

    while Il >= 0:  
        Il = odm.current01(V)
        Il2 = odm.current02(V)
        Wp = V * Il
        print  ("%.3f %.3f %.3f %.3f %.3f")%(V, Il, Wp, Il2, Il2 * V)
        V = V + 0.01

    print bdModulos.eschedaTecnica4["modelli"][0]

    for i in range(1,6):
        T = md4.temperatura(i)
        print T
    T = -25
    for i in range(10):
        T = T + 5 
        ambient.Ta = T
        md4.setAmbient(ambient)
        #print (T, md4.getVoc())

    print(md4)        

if __name__ == '__main__':
    testOneDiodeModel()
