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

    '''
    refs: 
       modelo = 1
             Photovoltaic Module Simulink Model for a Stand-alone PV Sytem
             Chen Qi, Zhu Ming  Physics Procedia 24 (2012) 94 – 100
             Simple Modeling and Simulation of Photovoltaic Panels
             Using Matlab/Simulink
             Jangwoo Park*, Hong-geun Kim, Yongyun Cho, Changsun Shin
             Advanced Science and Technology Letters
             Vol.73 (FGCN 2014), pp.147-155
             http://dx.doi.org/10.14257/astl.214.73.22
       modelo = 2  wind speed = 0
       modelo = 3
            Study of the operating temperature of a PV module
            Gail-Angee Migan
            Dept. of Energy Sciences, Faculty of Engineering,
            Lund University, Box 118, 22100 Lund, Sweden

       modelo = 4  Kurtz  
       modelo = 5  Koehl m-Si p-Si uc-Si
            Wind effect on PV module temperature: Analysis of different
            techniques for an accurate estimation
            Energy Procedia 40 (2013) 77 – 86

    '''
    def temperatura (self, modelo):
        '''
           S: is irradiance intensity ( W m2 );
           Ta: ambient temperature (°C)
           Va: local wind speed (m/s)

        '''
        S = self.ambient.Sa
        Ta = self.ambient.Ta
        Va = self.ambient.Va

        if modelo == 1:
           T = 31.2 + (0.25 * S /constants.Sn) + .899 * Ta - 1.3 * Va
        elif modelo == 2:
            T = Ta + 0.035 * S
        elif modelo ==  3:
            T = Ta + 0.32 * S / (8.91 + 2*Va)
        elif modelo == 4:
            T = Ta + S * math.exp(-3.473 - 0.0594 * Va)
        elif modelo == 5:
            U0 = 30.02
            U1 = 6.28
            T = Ta + S /(U0 + U1 * Va)
        else:
            T = Ta

        return T 

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
        T = self.temperatura(4)
        VT = self.VT * T / constants.Tref
        return self.Voc + self.cTVoc*(T - constants.Tref) + \
                   VT * math.log(self.ambient.Sa / constants.Sref)

    '''
      Parameter estimation of solar photovoltaic (PV) cells: A review
      Renewable and Sustainable Energy Reviews 61 (2016) 354–371
    '''
    def getVmp(self):
        T = self.temperatura(4)
        VT = self.VT * T / constants.Tref
        return self.Vmp + self.cTVoc*(T - constants.Tref) + \
                   VT * math.log(self.ambient.Sa / constants.Sref)

    def getImp(self):
        T = self.temperatura(4)
        return (self.Imp + self.cTIsc * (T - constants.Tref)) * self.ambient.Sa / constants.Sref

    '''
    Photovoltaic Module Simulink Model for a Stand-alone PV
    Physics Procedia 24 (2012) 94 – 100
    Chen Qi, Zhu Ming
    '''
    def getIph(self):
        T = self.temperatura(4)
        return (self.Isc + self.cTIsc * (T - constants.Tref)) * self.ambient.Sa / constants.Sref


   
    def getEg(self, T):
        #
        # ev to joule  1.60218e-19
        #
        return  (1.17 - (0.000473 *  T * T / (T + 636))) * 1.60218e-19

    def getI0(self, Iref):
        T = self.temperatura(4)
        Egref = self.getEg(constants.Tref + 273.16) / 298.16 
        Eg = self.getEg(T  + 273.16) /  (T + 273.16)

        I = Iref * ((T + 273.16)/298.16) * math.exp ((Egref  - Eg ) / constants.KK)
        return I

class Ambient(object):
    def __init__(self, Ta, Sa, Va):
        self.Ta = Ta
        self.Sa = Sa
        self.Va = Va



    def __str__(self):
        str_ = ("Ta: %.3f Sa: %.3f Va: %.3f")%(self.Ta, self.Sa, self.Va)


if __name__ == '__main__':
    pass
