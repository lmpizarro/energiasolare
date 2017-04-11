
# coding: utf-8

import math
import constants
import bdModulos


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
        
            if math.fabs(err) < 0.00001:
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
            diffI = 100 * (self.Isc - il)/ self.Isc
            print ("error calc SHORT: %.3e  error pc Isc: %.3f")%(err, diffI)
        if circuit == "open":
            diffV = 100 * (self.Voc - v1) / self.Voc
            print ("error calc OPEN: %.3e  error pc Voc: %.3f")%(err, diffV)


    def solveGl(self, vd_init, gl):
        self.gl = gl
        return self.solver(vd_init)

    def __str__(self):
        str1 = (" MODEL     Gp: %.3e Gs: %.3e I0: %.3e nref: %.3e Iirr %.3e T: %.3f Ns: %d ")%\
                (self.Gp, self.Gs, self.I0, self.nref, self.Iirr, self.Temp, self.Ns)

        str2 = ("\n MODULLO   Voc: %.3f Isc: %.3f Imp: %.3f Vmp: %.3f Gmpp: %.3f Vt: %.3f")%\
                (self.Voc, self.Isc, self.Imp, self.Vmp, self.Gmpp, self.Vt)        
        return str1 + str2

def testCompanion():

    indexModel = 4
    T = 20
    
    for i in range(5):
        indexModel = i
        mod1 = Companion(bdModulos.eschedaTecnica4, indexModel, T)
        mod1.mppCircuit(40, "mpp")
        mod1.mppCircuit(40, "open")
        mod1.mppCircuit(40, "short")
    '''

    mod1 = Companion(bdModulos.eschedaTecnica4, indexModel, T)
    gl = 0
    for i in range (90):
       (v1, i1, err) =  mod1.solveGl(40, gl)
       print  gl, v1, i1
       gl = gl + 0.01

    '''
if __name__ == '__main__':
    testCompanion()
