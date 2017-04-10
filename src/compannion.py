
# coding: utf-8

import math
import constants

Gp = 1.0 / 116.140
I0 = 5.689E-14
nref = 0.815
Iirr = 8.51
Ns = 60
T = 300


def openCircuit():
    Vt = Ns * nref * T  * constants.KK / constants.qq

    str1 = ("Gp: %.3f, I0: %.3e, nref: %.3f, Iirr: %.3f, Ns: %.3f Vt: %.3f")% \
            (Gp, I0, nref, Iirr, Ns, Vt) 
    
    print str1


    vd = 60
    id_ = 0.0

    Gd = (I0 / Vt) * math.exp(vd / Vt)

    v1 = (Iirr / 1.00 - (id_ - Gd * vd)) / (Gd + Gp)

    print ("Gd: %.3e id: %.3e v1: %.3e")%(Gd, id_, v1)

    for i in range(1000):
        err = vd
        #id_ = id_ + Gd * (v1 - vd)
        id_ = I0 * (math.exp(vd / Vt))
        v1 = (Iirr /1.00 - (id_ - Gd * vd)) / (Gd + Gp)
        vd = v1
        Gd = (I0 / Vt) * math.exp(vd / Vt)
        err = err - vd
        
        if math.fabs(err) < 0.0001:
            break

        print ("Gd: %.3e id: %.3e v1: %.3e err:%.3e")%(Gd, id_, v1, err)

    print i        

if __name__ == '__main__':
    openCircuit()
