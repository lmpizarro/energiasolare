
# coding: utf-8

import math
import constants
import bdModulos

Gp = 1.0 / 62.5481
Gs = 1.0 / 0.733


I0 = 9.84-42
nref = 0.25
Iirr = 8.5794
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
    
#print str1

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

    diffV = 100 * (Vmpp - v1) / Vmpp
    diffI = 100 * (Impp - il)/ Impp

    print ("error calc: %.3e error pc Vmp: %.3f error pc Imp: %.3f")%(err, diffV, diffI)



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
        Gd = (I0 / Vt) * math.exp(vd / Vt)
        err = err - vd
        
        if math.fabs(err) < 0.0001:
            break


    print ("OPEN Gd: %.3e id: %.3e v1: %.3e err:%.3e")%(Gd, id_, v1, err)

    diff = Voc - v1

    print diff


def test01 ():
    mppCircuit()
    shortCircuit()
    openCircuit()

class Companion(object):
    def __init__(self, modulo, index, Temp):
        self.modulo = modulo
        self.modelli = self.modulo["modelli"][index]


        self.Gp  = 1.0 / self.modelli["Rsh"] 
        self.Gs  = 1.0 / self.modelli["Rs"] 
        self.I0  = self.modelli["I0"]
        self.nref  = self.modelli["nref"]
        self.Iirr  = self.modelli["Iirr"]

        self.Ns = self.modulo["CaratteristicheMeccaniche"]["cell"] 
        
        self.Temp = Temp + 273
        self.Vt = self.Ns * self.nref * self.Temp  * constants.KK / constants.qq

        self.Imp = self.modulo["datiElettrici"]["Imp"]
        self.Vmp = self.modulo["datiElettrici"]["Vmp"]
   
        self.Isc = self.modulo["datiElettrici"]["Isc"]
        self.Voc = self.modulo["datiElettrici"]["Voc"]

        self.Gmpp = self.Imp / self.Vmp 


    def getId(self, vd):
        return self.I0 * (math.exp(vd / self.Vt) -  1)

    def getGd(self, vd):
        return (self.I0 / self.Vt) * math.exp(vd / self.Vt)


    def solver (self, vd_init):
        vd = vd_init 
        id_ = self.getId(vd) 
        Gd = self.getGd(vd) 

        v1 = (self.Iirr - (id_ - Gd * vd)) / (Gd + self.Gp + self.gl)

        for i in range(1000):
            err = vd
            id_ = self.getId(vd) 
            v1 = (self.Iirr - (id_ - Gd * vd)) / (Gd + self.Gp + self.gl)
            vd = v1
            Gd = self.getGd(vd) 
            err = err - vd
            il = vd * self.gl
        
            if math.fabs(err) < 0.0001:
                break
        return (v1, il, err)

    def mppCircuit(self, vd_init, circuit):

        if circuit == "mpp":
            self.gl = self.Gs * self.Gmpp / (self.Gs + self.Gmpp)
        elif circuit == "short":
            self.gl = self.Gs
        elif circuit == "open":
            self.gl = 0.0


        (v1, il, err) = self.solver(vd_init)

        #print ("MPP  v1: %.3e il: %.3e err:%.3e")%(v1, il, err)


        if circuit == "mpp":
            diffV = 100 * (self.Vmp - v1) / self.Vmp
            diffI = 100 * (self.Imp - il)/ self.Imp
            print ("error calc MPP: %.3e error pc Vmp: %.3f error pc Imp: %.3f")%(err, diffV, diffI)
        if circuit == "short":
            diffI = 100 * (self.Imp - il)/ self.Imp
            print ("error calc SHORT: %.3e  error pc Imp: %.3f")%(err, diffI)
        if circuit == "open":
            diffV = 100 * (self.Vmp - v1) / self.Vmp
            print ("error calc OPEN: %.3e  error pc Vmp: %.3f")%(err, diffV)




    def __str__(self):
        str1 = (" MODEL     Gp: %.3e Gs: %.3e I0: %.3e nref: %.3e Iirr %.3e T: %.3f Ns: %d ")%\
                (self.Gp, self.Gs, self.I0, self.nref, self.Iirr, self.Temp, self.Ns)

        str2 = ("\n MODULLO   Voc: %.3f Isc: %.3f Imp: %.3f Vmp: %.3f Gmpp: %.3f Vt: %.3f")%\
                (self.Voc, self.Isc, self.Imp, self.Vmp, self.Gmpp, self.Vt)        
        return str1 + str2

def testCompanion():
    indexModel = 1
    T = 25
    mod1 = Companion(bdModulos.eschedaTecnica4, indexModel, T)
    print mod1

    mod1.mppCircuit(30, "mpp")
    mod1.mppCircuit(30, "open")
    mod1.mppCircuit(30, "short")


if __name__ == '__main__':
    testCompanion()
