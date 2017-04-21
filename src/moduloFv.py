# coding: utf-8

import math
import constants
import bdModulos
import ModelloBase as MB
import companionSim as comp


"""
 riferito alle condizioni standard IEC
 temperatura della cella fotovoltaica pari a 25°C
 irraggiamento di 1000 W/m2 e velocità del vento di 1 m/s
 
 NOCT: Nominal Operating Cell Temperature

"""
class Modulo(object):
     
    def __init__(self, esp):
        self.esp = esp
        self.cell = esp["CaratteristicheMeccaniche"]["cell"]

        
        self.Pn = esp["datiElettrici"]["Pn"]
        self.Vmp = esp["datiElettrici"]["Vmp"]
        self.Imp = esp["datiElettrici"]["Imp"]
        self.Isc = esp["datiElettrici"]["Isc"]
        self.Voc = esp["datiElettrici"]["Voc"]

        self.cTVoc = esp["CoefficienteDiTemperatura"]["Voc"]
        self.cTPn = esp["CoefficienteDiTemperatura"]["Pn"]
        self.cTIsc = esp["CoefficienteDiTemperatura"]["Isc"]
        self.noct = esp["CoefficienteDiTemperatura"]["NOCT"]

        self.lungh = esp["CaratteristicheMeccaniche"]["lungh"]
        self.largh = esp["CaratteristicheMeccaniche"]["largh"]
        self.alt = esp["CaratteristicheMeccaniche"]["alt"]
        self.peso = esp["CaratteristicheMeccaniche"]["peso"]
        self.Ns = esp["CaratteristicheMeccaniche"]["cell"]

        self.area = self.lungh * self.largh
        self.vol = self.area * self.alt 
        self.pesoEsp = self.peso / self.vol
        self.PnArea = self.Pn / self.area
        self.cellArea = self.area / self.cell
        self.eff = (self.Pn / self.area) / 10

        self.modelli = []


        '''
        one diode model Rsh -> infinito
        An Improved Model-Based Maximum Power Point
        Tracker for Photovoltaic Panels
        IEEE TRANSACTIONS ON INSTRUMENTATION AND MEASUREMENT, VOL. 63, NO. 1,
        JANUARY 2014

        self.VT = (2*self.Vmp - self.Voc)* (self.Isc - self.Imp)/\
                  (self.Imp + (self.Isc - self.Imp)*math.log(1 - self.Imp/self.Isc))
        '''

    def __str__(self):
        str1 =("%s %s \n")%(self.esp["marca"], self.esp["modello"])
        str2 = ("Pn: %.3f Vmp: %.3f Imp: %.3f Voc: %.3f Isc: %.3f Cell: %d \n")%(self.Pn , self.Vmp , self.Imp ,\
                self.Voc, self.Isc, self.cell  )
        str3 = ("NOCT %s °C:   Voc %.3f  Pn %.3f  Isc %.3f\n")%(self.noct, self.cTVoc, self.cTPn, self.cTIsc) 

        str4 = ("largh: %.3f lungh: %.3f  alt: %.3f area: %.3f vol: %.3f peso: %.3f\n")%(self.largh, self.lungh,\
                self.alt, self.area, self.vol, self.peso)

        str5 = (" eff: %3f cellArea: %.3f  PnArea: %.3f pEsp: %.3f\n")%(\
                self.eff, self.cellArea, self.PnArea, self.pesoEsp)


        return str1 + " " + str2  +  " " + str3 + " " + str4 + str5 + "\n"

    def setAmbient(self, ambient):
        self.ambient = ambient

    '''
    An Improved Model-Based Maximum Power Point
    Tracker for Photovoltaic Panels
    IEEE TRANSACTIONS ON INSTRUMENTATION AND MEASUREMENT, VOL. 63, NO. 1,
    JANUARY 2014
    Cristaldi, Faifer, Rossi, Toscani
    '''
    def getVoc (self):
        T = self.ambient.getTemperatura(4)
        VT = self.VT * T / constants.Tref
        return self.Voc + self.cTVoc*(T - constants.Tref) + \
                   VT * math.log(self.ambient.Sa / constants.Sref)

    '''
      Parameter estimation of solar photovoltaic (PV) cells: A review
      Renewable and Sustainable Energy Reviews 61 (2016) 354–371
    '''
    def getVmp(self):
        T = self.ambient.getTemperatura(4)
        VT = self.VT * T / constants.Tref
        return self.Vmp + self.cTVoc*(T - constants.Tref) + \
                   VT * math.log(self.ambient.Sa / constants.Sref)

    def getImp(self):
        T = self.ambient.getTemperatura(4)
        return (self.Imp + self.cTIsc * (T - constants.Tref)) * self.ambient.Sa / constants.Sref

    '''
    Photovoltaic Module Simulink Model for a Stand-alone PV
    Physics Procedia 24 (2012) 94 – 100
    Chen Qi, Zhu Ming
    '''
    def getIph(self):
        T = self.ambient.getTemperatura(4)
        return (self.Isc + self.cTIsc * (T - constants.Tref)) * self.ambient.Sa / constants.Sref

   
    def getEg(self, T):
        #
        # ev to joule  1.60218e-19
        #
        return  (1.17 - (0.000473 *  T * T / (T + 636))) * 1.60218e-19

    def getI0(self, Iref):
        T = self.ambient.getTemperatura(4)
        Egref = self.getEg(constants.Tref + 273.16) / 298.16 
        Eg = self.getEg(T  + 273.16) /  (T + 273.16)

        I = Iref * ((T + 273.16)/298.16) * math.exp ((Egref  - Eg ) / constants.KK)
        return I


if __name__ == '__main__':
    pass
