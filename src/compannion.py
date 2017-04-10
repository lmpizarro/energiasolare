
# coding: utf-8

import math
import constants

Gp = 1.0 / 116.140
I0 = 5.689E-14
nref = 0.74
Iirr = 8.51
Ns = 60
T = 300


def openCircuit():
    str1 = ("Gp: %.3f, I0: %.3e, nref: %.3f, Iirr: %.3f, Ns: %.3f")%(Gp, I0, nref, Iirr, Ns) 
    print str1

    Gd = I0 * constants.qq / (constants.KK * nref * Ns * T )

    id_ = 0.0
    v1 = Iirr / (Gd + Gp)

    print Gd, id_, v1

if __name__ == '__main__':
    openCircuit()
