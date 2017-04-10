
# coding: utf-8

import math
import constants

Gp = 1.0 / 116.140
Gs = 1.0 / 0.4759
I0 = 5.689E-14
nref = 0.815
Iirr = 8.51
Ns = 60
T = 300
Vt = Ns * nref * T  * constants.KK / constants.qq
Vmpp = 29.6
Impp = 7.94
Gmpp = Impp / Vmpp

str1 = ("Gmpp %.3f Gp: %.3f, I0: %.3e, nref: %.3f, Iirr: %.3f, Ns: %.3f Vt: %.3f")% \
        (Gmpp, Gp, I0, nref, Iirr, Ns, Vt) 
    
print str1



def shortCircuit():
    vd = 60
    id_ = 0.0

    Gd = (I0 / Vt) * math.exp(vd / Vt)

    v1 = (Iirr / 1.00 - (id_ - Gd * vd)) / (Gd + Gp + Gs)

    print ("Gd: %.3e id: %.3e v1: %.3e")%(Gd, id_, v1)

    for i in range(1000):
        err = vd
        id_ = I0 * (math.exp(vd / Vt))
        v1 = (Iirr /1.00 - (id_ - Gd * vd)) / (Gd + Gp + Gs)
        vd = v1
        Gd = (I0 / Vt) * math.exp(vd / Vt)
        err = err - vd
        il = vd * Gs
        
        print ("Gd: %.3e id: %.3e v1: %.3e il: %.3e err:%.3e")%(Gd, id_, v1, il, err)
        if math.fabs(err) < 0.0001:
            break


    print i        


def openCircuit():


    vd = 60
    id_ = 0.0

    Gd = (I0 / Vt) * math.exp(vd / Vt)

    v1 = (Iirr / 1.00 - (id_ - Gd * vd)) / (Gd + Gp)

    print ("Gd: %.3e id: %.3e v1: %.3e")%(Gd, id_, v1)

    for i in range(1000):
        err = vd
        id_ = I0 * (math.exp(vd / Vt))
        v1 = (Iirr /1.00 - (id_ - Gd * vd)) / (Gd + Gp)
        vd = v1
        Gd = (I0 / Vt) * math.exp(vd / Vt)
        err = err - vd
        
        print ("Gd: %.3e id: %.3e v1: %.3e err:%.3e")%(Gd, id_, v1, err)
        if math.fabs(err) < 0.0001:
            break


    print i        



if __name__ == '__main__':
    shortCircuit()
