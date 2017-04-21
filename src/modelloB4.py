
# coding: utf-8
import math
import modelloBase as MB
import moduloFv as mFV
import bdModulos
import constants
import modelloAmbiente as AMB

class modelloB4(MB.ModelloBase):
    def __init__(self, m, ambient):

        super(modelloB4, self).__init__(m, ambient)

        den1 = m.Imp + self.deltai * math.log(self.deltai/m.Isc)
        num1 = (2 * m.Vmp - m.Voc ) 

        self.Rs = m.Vmp / m.Imp - num1 / (den1)

        if self.Rs < 0:
             # massimo
             self.Rs = self.deltav / m.Imp

        '''
        one diode model Rsh -> infinito
        An Improved Model-Based Maximum Power Point
        Tracker for Photovoltaic Panels
        IEEE TRANSACTIONS ON INSTRUMENTATION AND MEASUREMENT, VOL. 63, NO. 1,
        JANUARY 2014
        '''
        self.Vt = num1 * self.deltai / den1 

        self.nref = self.Vt / (m.Ns * constants.KK * self.T / constants.qq)

        self.Rsh = (m.Vmp + m.Imp*self.Rs) / self.deltai

        self.Ii = m.Isc * (self.Rs + self.Rsh)/self.Rsh 

        def I0():
            den = math.exp ((self.Rs * m.Isc) / self.Vt) + math.exp(m.Voc /\
                    self.Vt)
            I0 = m.Isc / den
            return  I0 

        self.I0 = I0() 

        self.setModello()


def testB4():
    Ta = 30
    Ws = 4
    Ss = 1500

    ambient = AMB.Ambient (Ta, Ss, Ws)
    ambient.setModelo(4)

    md1 = mFV.Modulo(bdModulos.eschedaTecnica4)

    mbcMd3 = modelloB4(md1, ambient)
    print("modelloB4: ")
    print mbcMd3


if __name__ == '__main__':
    testB4()
