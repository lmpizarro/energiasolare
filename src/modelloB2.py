
# coding: utf-8
import math
import ModelloBase as MB
import moduloFv as mFV
import bdModulos
import constants
import modelloAmbiente as AMB

import companionSim as comp

class modelloB2(MB.ModelloBase):
    def __init__(self, m, ambient):

        super(modelloB2, self).__init__(m, ambient)

        # massimo
        self.Rs = self.deltav / m.Imp

        self.RsM =  self.Rs
       
        # minimo
        #self.Rsh = (m.Vmp) / self.deltai
        '''
        (2) y (1) Parameter estimation of photovoltaic modules using iterative method
        and the Lambert W function: A comparative study
        Energy Conversion and Management 119 (2016) 37–48

        '''

        self.Rsh = (self.m.Vmp) / self.deltai - self.deltav / m.Imp
        '''
        (2) Comprehensive Approach to Modeling and
        Simulation of Photovoltaic Arrays
        IEEE TRANSACTIONS ON POWER ELECTRONICS, VOL. 24, NO. 5, MAY 2009

        '''
        self.calcIi ()


        self.Vt = constants.KK * self.T / constants.qq

        N = constants.Vthre / self.Vt

        self.Vt = m.Ns * self.Vt

        #self.nref = (m.Voc - self.Vt * N ) / (self.Vt * N)

        self.nref = m.Voc / (self.Vt * N)

        self.calcI0()

        self.calcRs()

        self.setModello()


    def calcI0(self):        
        '''
        Parameter estimation of solar photovoltaic (PV) cells: A review
        Renewable and Sustainable Energy Reviews 61 (2016) 354–371
        A. Rezaee Jordehi 
        '''
        def I0():
            den = math.exp ((self.Rs * self.m.Isc) / self.Vt) + math.exp(self.m.Voc /\
                    self.Vt)
            I0 = self.m.Isc / den
            return  I0 

        self.I0 = I0()

    def calcDiff(self,rs):
        vd = self.m.Vmp + self.m.Imp * rs
        a = self.I0 * (math.exp(vd/self.Vt) - 1)
        i = self.Ii  - a  - vd / self.Rsh
        return self.m.Imp - i

  

    def calcRs(self):

        rs = 0.0

        diff = self.calcDiff(rs) 

        if diff > 0:
            rs = 0.0
        else:
            while diff < 0.0 and rs < self.RsM: 
               rs += 0.001 
               diff = self.calcDiff(rs) 
        self.Rs =  rs

def testB2():
    Ta = 30
    Ws = 4
    Ss = 1500

    ambient = AMB.Ambient (Ta, Ss, Ws)

    md1 = mFV.Modulo(bdModulos.eschedaTecnica4)

    print (md1)
    mbcMd3 = modelloB2(md1, ambient)
    print(mbcMd3)

    md2 = mFV.Modulo(bdModulos.eschedaTecnica2)
    print (md2)

    mbcMd3 = modelloB2(md2, ambient)
    print(mbcMd3)

    print

    md3 = mFV.Modulo(bdModulos.eschedaTecnica3)
    print (md3)

    mbcMd3 = modelloB2(md3, ambient)
    print("modelloB2 ")
    print mbcMd3

    mbcMd3 = modelloB2(md2, ambient)
    print("modelloB2 ")
    print mbcMd3

    mbcMd3 = modelloB2(md1, ambient)
    print("modelloB2 ")
    print mbcMd3

    mod1 = comp.Companion(md1.esp, 1000, Ta)
    mod1.caclCircuit(80)
    print mod1.resultados

    mbcMd3 = MB.ModelloBase(md3, ambient)
    print("modelloBase: ")
    print mbcMd3

    '''
    cel1 = cella (md1)
    print (cel1)

    mbc = modelloB2(cel1, ambient)

    print (mbc)
    '''




if __name__ == '__main__':
    testB2()
