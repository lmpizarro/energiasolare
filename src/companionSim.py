
# coding: utf-8

import math
import constants
import bdModulos
import fvMmodel

class Resultados:
    def __init__(self,m):
        self.Isc = m["Isc"]
        self.Voc = m["Voc"]
        self.Vmp = m["Vmp"]
        self.Imp = m["Imp"]

        self.isc = 0.0
        self.voc = 0.0
        self.vmp = 0.0
        self.imp = 0.0

    def calcSQRT(self):
        self.errvmpp = (self.vmpp - self.Vmp)
        self.errimpp = (self.impp - self.Imp)
        self.diffV = (self.Voc - self.voc) 
        self.diffI = (self.Isc - self.isc)

        self.errI = 100 * math.sqrt(self.errimpp * self.errimpp + self.diffI * self.diffI)/ \
                (self.Isc + self.Imp)
        self.errV = 100 * math.sqrt(self.errvmpp * self.errvmpp + self.diffV * self.diffV)/ \
                (self.Voc + self.Vmp)

    def calcPercent(self):
        self.errvmpp = self.errvmpp / self.Vmp
        self.errimpp = self.errimpp / self.Imp
        self.diffV /= self.Voc
        self.diffI /= self.Isc
    

    def __str__(self):
        self.calcSQRT()

        str4 = ("error I %.3e pc:\n")%(self.errI)
        str5 = ("error V %.3e pc:\n")%(self.errV)

        self.calcPercent()

        str1 = ("error Vmpp %.3e pc, error Impp %.3e pc\n")% \
                (self.errvmpp, self.errimpp)
        str2 =  ("error Isc: %.3e pc\n")%(self.diffI)
        str3 =  ("error Voc: %.3e pc\n")%(self.diffV)

        return str1+ str2+ str3+ str4 + str5      


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

        self.resultados = Resultados(self.modulo["datiElettrici"])


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

    def solveGl(self, vd_init, gl):
        self.gl = gl
        return self.solver(vd_init)

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


        self.resultados.vmpp = vmax
        self.resultados.impp = imax


    def caclCircuit(self, vd_init):
        
        # calc MPP
        self.calcMpp()

        # calc ISC
        self.gl = self.Gs
        (v1, il, err) = self.solver(vd_init)
        self.resultados.isc = il


        # calc VOC
        self.gl = 0.0
        (v1, il, err) = self.solver(vd_init)
        self.resultados.voc = v1



    def __str__(self):
        str1 = (" MODEL     Gp: %.3e Gs: %.3e I0: %.3e nref: %.3e Iirr %.3e T: %.3f Ns: %d ")%\
                (self.Gp, self.Gs, self.I0, self.nref, self.Iirr, self.Temp, self.Ns)

        str2 = ("\n MODULLO   Voc: %.3f Isc: %.3f Imp: %.3f Vmp: %.3f Gmpp: %.3f Vt: %.3f")%\
                (self.Voc, self.Isc, self.Imp, self.Vmp, self.Gmpp, self.Vt)        
        return str1 + str2


def testCompanionB2():

    indexModel = 4
    Ta = 20
    Ws = 4
    Ss = 1500

    ambient = fvMmodel.Ambient (Ta, Ss, Ws)

    md1 = fvMmodel.Modulo(bdModulos.eschedaTecnica1)
    mbcMd3 = fvMmodel.modelloB2(md1, ambient)
    mod1 = Companion(md1.esp, 1000, Ta)

    mod1.caclCircuit(40)

    print mod1.resultados

    print 

    md1 = fvMmodel.Modulo(bdModulos.eschedaTecnica2)
    mbcMd3 = fvMmodel.modelloB2(md1, ambient)
    mod1 = Companion(md1.esp, 1000, Ta)

    mod1.caclCircuit(40)

    print mod1.resultados
    print 

    md1 = fvMmodel.Modulo(bdModulos.eschedaTecnica3)
    mbcMd3 = fvMmodel.modelloB2(md1, ambient)
    mod1 = Companion(md1.esp, 1000, Ta)

    mod1.caclCircuit(40)

    print mod1.resultados
    print 

    md1 = fvMmodel.Modulo(bdModulos.eschedaTecnica4)
    mbcMd3 = fvMmodel.modelloB2(md1, ambient)
    mod1 = Companion(md1.esp, 1000, Ta)

    mod1.caclCircuit(40)
    print mod1.resultados

    md1.setAmbient(ambient)
    I0 = md1.esp["modelli"][-1]["I0"]
    print md1.getVoc(), md1.Voc, md1.getVmp(), md1.Vmp, md1.getImp(), md1.Imp,\
            md1.getI0(I0), I0



if __name__ == '__main__':
    print ("test B2")
    testCompanionB2()
