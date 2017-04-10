
# coding: utf-8

import math
import constants

Gp = 1.0 / 116.140
Gs = 1.0 / 0.4759
I0 = 5.689E-14
nref = 0.74
Iirr = 8.51
Ns = 60
T = 300
Vt = Ns * nref * T  * constants.KK / constants.qq
Vmpp = 29.6
Impp = 7.94
Gmpp = Impp / Vmpp
Isc = 8.4
Voc = 36.8

str1 = ("Gmpp %.3f Gp: %.3f, I0: %.3e, nref: %.3f, Iirr: %.3f, Ns: %.3f Vt: %.3f")% \
        (Gmpp, Gp, I0, nref, Iirr, Ns, Vt) 
    
print str1

vd = 10.0
id_ = 0.0
Gd = (I0 / Vt) * math.exp(vd / Vt)


#print ("Gd: %.3e id: %.3e v1: %.3e \n")%(Gd, id_, v1)


def mppCircuit():
    global vd, Gd, id_

    gl = Gs * Gmpp / (Gs + Gmpp)


    v1 = (Iirr - (id_ - Gd * vd)) / (Gd + Gp + gl)

    for i in range(1000):
        err = vd
        id_ = I0 * (math.exp(vd / Vt) -  1)
        v1 = (Iirr - (id_ - Gd * vd)) / (Gd + Gp + gl)
        vd = v1
        Gd = (I0 / Vt) * math.exp(vd / Vt)
        err = err - vd
        il = vd * gl
        
        if math.fabs(err) < 0.0001:
            break

    print ("MPP Gd: %.3e id: %.3e v1: %.3e il: %.3e err:%.3e")%(Gd, id_, v1, il, err)

    diffV = Vmpp - v1
    diffI = Impp - il

    print diffV, diffI


def shortCircuit():
   
    global vd, Gd, id_

    v1 = (Iirr / 1.00 - (id_ - Gd * vd)) / (Gd + Gp + Gs)
    for i in range(1000):
        err = vd
        id_ = I0 * (math.exp(vd / Vt) - 1)
        v1 = (Iirr - (id_ - Gd * vd)) / (Gd + Gp + Gs)
        vd = v1
        Gd = (I0 / Vt) * math.exp(vd / Vt)
        err = err - vd
        il = vd * Gs
        
        if math.fabs(err) < 0.0001:
            break


    print ("SHORT Gd: %.3e id: %.3e v1: %.3e il: %.3e err:%.3e")%(Gd, id_, v1, il, err)

    diff = Isc - il 

    print diff



def openCircuit():

    #global vd, Gd, id_

    vd = 60.0
    id_ = 0.0

    Gd = (I0 / Vt) * math.exp(vd / Vt)
 

    v1 = (Iirr / 1.00 - (id_ - Gd * vd)) / (Gd + Gp)

    for i in range(1000):
        err = vd
        id_ = I0 * (math.exp(vd / Vt) - 1)
        v1 = (Iirr - (id_ - Gd * vd)) / (Gd + Gp)
        vd = v1
        print vd
        Gd = (I0 / Vt) * math.exp(vd / Vt)
        err = err - vd
        
        if math.fabs(err) < 0.0001:
            break


    print ("OPEN Gd: %.3e id: %.3e v1: %.3e err:%.3e")%(Gd, id_, v1, err)

    diff = Voc - v1

    print diff



if __name__ == '__main__':
    mppCircuit()
    shortCircuit()
    openCircuit()
