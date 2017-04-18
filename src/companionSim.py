
# coding: utf-8

import math
import constants
import bdModulos
import fvMmodel


class Companion(object):
    def __init__(self, modulo, index, Temp):
        self.modulo = modulo
        if index == 1000:
            self.modelli = self.modulo["modelli"][-1]
        else:    
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


    def calcMpp(self):
        glimit = 10  * self.Gmpp
        deltaG = glimit / 100
        gl = 0
        pmax = 0
        imax = 0
        vmax = 0
        err = 0
        for i in range (100):
           (v1, i1, err) =  self.solveGl(40, gl)
           err += err
           p = v1 * i1
           if p > pmax:
               pmax = p
               imax = i1
               vmax = v1
           gl = gl + deltaG 



        errvmpp = 100 * (vmax - self.Vmp) / self.Vmp
        errimpp = 100 * (imax - self.Imp) / self.Imp
        err = err / 100

        print ("error CALC MPP %.3e error pc Vmpp %.3f, error Impp %.3f")% \
                (err, errvmpp, errimpp)



    def caclCircuit(self, vd_init, circuit):

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
        mod1.caclCircuit(40, "mpp")
        mod1.caclCircuit(40, "open")
        mod1.caclCircuit(40, "short")
    '''

    mod1 = Companion(bdModulos.eschedaTecnica4, indexModel, T)
    gl = 0
    for i in range (90):
       (v1, i1, err) =  mod1.solveGl(40, gl)
       print  gl, v1, i1
       gl = gl + 0.01

    '''


def testCompanionB2():

    indexModel = 4
    Ta = 20
    Ws = 4
    Ss = 1500

    ambient = fvMmodel.Ambient (Ta, Ss, Ws)

    md1 = fvMmodel.Modulo(bdModulos.eschedaTecnica1)
    mbcMd3 = fvMmodel.modelloB2(md1, ambient)
    mod1 = Companion(md1.esp, 1000, Ta)

    mod1.caclCircuit(40, "open")
    mod1.caclCircuit(40, "short")
    mod1.calcMpp()

    print 

    md1 = fvMmodel.Modulo(bdModulos.eschedaTecnica2)
    mbcMd3 = fvMmodel.modelloB2(md1, ambient)
    mod1 = Companion(md1.esp, 1000, Ta)

    mod1.caclCircuit(40, "open")
    mod1.caclCircuit(40, "short")
    mod1.calcMpp()

    print 

    md1 = fvMmodel.Modulo(bdModulos.eschedaTecnica3)
    mbcMd3 = fvMmodel.modelloB2(md1, ambient)
    mod1 = Companion(md1.esp, 1000, Ta)

    mod1.caclCircuit(40, "open")
    mod1.caclCircuit(40, "short")
    mod1.calcMpp()

    print 

    md1 = fvMmodel.Modulo(bdModulos.eschedaTecnica4)
    mbcMd3 = fvMmodel.modelloB2(md1, ambient)
    mod1 = Companion(md1.esp, 1000, Ta)

    mod1.caclCircuit(40, "open")
    mod1.caclCircuit(40, "short")
    mod1.calcMpp()

    md1.setAmbient(ambient)
    I0 = md1.esp["modelli"][-1]["I0"]
    print md1.getVoc(), md1.Voc, md1.getVmp(), md1.Vmp, md1.getImp(), md1.Imp,\
            md1.getI0(I0), I0



    '''
    md1.esp["modelli"][0]["Iirr"] = md1.esp["modelli"][0]["Iirr"] * .95

    mod1 = Companion(md1.esp, 0, Ta)

    mod1.caclCircuit(40, "mpp")
    mod1.caclCircuit(40, "open")
    mod1.caclCircuit(40, "short")
    '''


if __name__ == '__main__':
    print ("test B2")
    testCompanionB2()
