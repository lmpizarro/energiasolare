# coding: utf-8

import math
import constants
import bdModulos


"""
 riferito alle condizioni standard IEC
 temperatura della cella fotovoltaica pari a 25°C
 irraggiamento di 1000 W/m2 e velocità del vento di 1 m/s
 
 NOCT: Nominal Operating Cell Temperature

"""


class modelloB2(object):
    def __init__(self, m, ambient):

        deltav = m.Voc - m.Vmp
        deltai = m.Isc - m.Imp

        #self.Rs = deltav / m.Imp

        #self.Rsh = m.Voc / deltai

        self.Rs = deltav / m.Isc

        self.Rsh = (m.Vmp + m.Imp*self.Rs) / deltai

        '''
        Parameter estimation of photovoltaic modules using iterative method
        and the Lambert W function: A comparative study
        Energy Conversion and Management 119 (2016) 37–48
        '''
        self.Ii = m.Isc * (self.Rs + self.Rsh)/self.Rsh 

        self.T =  ambient.Ta + 273.16

        self.Vt = constants.KK * self.T / constants.qq

        N = constants.Vthre / self.Vt

        self.Vt = m.Ns * self.Vt

        #self.nref = (m.Voc - self.Vt * N ) / (self.Vt * N)

        self.nref = m.Voc / (self.Vt * N)


        '''
        Parameter estimation of solar photovoltaic (PV) cells: A review
        Renewable and Sustainable Energy Reviews 61 (2016) 354–371
        A. Rezaee Jordehi 
        '''
        def I0():
            den = math.exp ((self.Rs * m.Isc) / self.Vt) + math.exp(m.Voc /\
                    self.Vt)
            I0 = m.Isc / den
            return  I0 

        self.I0 = I0() 

        m.esp["modelli"] = []

        
        m.esp["modelli"].append({"Rs":self.Rs, "Rsh": self.Rsh, "nref": self.nref,\
                "source": "B2", "Iirr": self.Ii, "I0": self.I0})
         


    def __str__(self):    
        str1 = ("Rsh: %.3f Rs: %.3f nref: %.3f Ii: %.3f I0: %.3e\n")%\
                (self.Rsh, self.Rs,self.nref, self.Ii, self.I0)
        return str1




class cavio(object):
   def __init__(self, l, s, m):
       self.l = l
       self.s = s
       self.m = m

   def __str__(self):
       str1= ("l: %.3f s: %.3f m: %s ")%(self.l, self.s, self.m)

       return str1

   def resistividad(self, T):
       '''
       20 °C
       cu 1.724 e-8 ohm m  4.29e -3 1/°C   0.393 % / °C         
       al 2.65 e-8 ohm m   3.80e -3 1/°C

       '''
       rhoCu = 0.00000001724 * 1000000 # ohmm * mm2/m
       rhoAl = 0.0000000265 * 1000000

       return rhoCu * ( 1 + 0.00429*(T - 20))

   def R(self, T):
       return (self.resistividad(T))*self.l/self.s

class cella(object):
    def __init__(self, modulo):
        self.Pn = modulo.Pn / modulo.cell
        self.Voc = modulo.Voc / modulo.cell
        self.Vmp = modulo.Vmp /modulo.cell
        self.Imp = modulo.Imp
        self.Isc = modulo.Isc

    def __str__(self):
        header = "cell\n"
        str1 = ("Pn: %.3f Voc: %.3f Isc: %.3f Vmp: %.3f Imp: %.3f\n")%\
                (self.Pn, self.Voc, self.Isc, self.Vmp, self.Imp)

        return (header + str1)


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

        self.VT = (2*self.Vmp - self.Voc)* (self.Isc - self.Imp)/\
                  (self.Imp + (self.Isc - self.Imp)*math.log(1 - self.Imp/self.Isc))

    def __str__(self):
        str1 =("%s %s \n")%(self.esp["marca"], self.esp["modello"])
        str2 = ("Pn: %.3f Vmp: %.3f Imp: %.3f Voc: %.3f Isc: %.3f Cell: %d \n")%(self.Pn , self.Vmp , self.Imp ,\
                self.Voc, self.Isc, self.cell  )
        str3 = ("NOCT %s °C:   Voc %.3f  Pn %.3f  Isc %.3f\n")%(self.noct, self.cTVoc, self.cTPn, self.cTIsc) 

        str4 = ("largh: %.3f lungh: %.3f  alt: %.3f area: %.3f vol: %.3f peso: %.3f\n")%(self.largh, self.lungh,\
                self.alt, self.area, self.vol, self.peso)

        str5 = (" eff: %3f cellArea: %.3f  PnArea: %.3f pEsp: %.3f\n")%(\
                self.eff, self.cellArea, self.PnArea, self.pesoEsp)

        str6 = ("VT: %.3f\n") %(self.VT)

        return str1 + " " + str2  +  " " + str3 + " " + str4 + str5 + str6 + "\n"

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


class OneDiodeModel(object):
    def __init__(self,eschedaTecnica, model, T):
        '''
        Ns: number of cells in serie
        Rs: R serie Ohm 
        Rsh: R shunt Ohm 
        I0: diode reverse saturation current Amp
        n: ideality factor
        T : ° Kelvin
        '''
        Ns = eschedaTecnica["CaratteristicheMeccaniche"]["cell"]
        modelli = eschedaTecnica["modelli"][model]
        self.Ns = Ns
        self.Rs = modelli["Rs"]
        self.Rsh = modelli["Rsh"]
        self.n = modelli["nref"]
        self.I0 = modelli["I0"]
        self.T = T
        self.A = constants.qq / (self.n * constants.KK * self.T)

    def __str__(self):
        format_ = "Rs: %.3f Rsh: %.3f n: %.3f I0: %.3e T: %.3f A: %.3f"
        str1 = (format_)%(self.Rs, self.Rsh, self.n, self.I0, self.T, self.A)
        return (str1)

    def current01(self, V):
        return (self.Iph - self.I0*math.exp(self.A * V / self.Ns))

    def current02(self, V):
        a = self.Rsh / (self.Rsh + self.Rs)
        return a * (self.current01(V) - V/ self.Rsh)

    def setIph (self, Iph):
        self.Iph = Iph


def testB2():

    Ta = 30
    Ws = 4
    Ss = 1500

    ambient = Ambient (Ta, Ss, Ws)

    md1 = Modulo(bdModulos.eschedaTecnica4)

    print (md1)
    mbcMd3 = modelloB2(md1, ambient)
    print(mbcMd3)


    md2 = Modulo(bdModulos.eschedaTecnica2)
    print (md2)

    mbcMd3 = modelloB2(md2, ambient)
    print(mbcMd3)

    print


    md3 = Modulo(bdModulos.eschedaTecnica3)
    print (md3)



    mbcMd3 = modelloB2(md3, ambient)
    print(mbcMd3)


    '''
    cel1 = cella (md1)
    print (cel1)

    mbc = modelloB2(cel1, ambient)

    print (mbc)
    '''

def testOneDiodeModel():    
    # Rs, Rsh, n, I0, T
    Ta = 30
    Ws = 4
    Ss = 1500

    ambient = Ambient (Ta, Ss, Ws)

    md4 = Modulo(bdModulos.eschedaTecnica4)
    md4.setAmbient(ambient)
    T = md4.temperatura(4)

    odm = OneDiodeModel(bdModulos.eschedaTecnica4, 0, T + 273.16)

    V = 0.0
    Il = 0.0
    Wp = 0.0
    odm.setIph(8.6)

    while Il >= 0:  
        Il = odm.current01(V)
        Il2 = odm.current02(V)
        Wp = V * Il
        print  ("%.3f %.3f %.3f %.3f %.3f")%(V, Il, Wp, Il2, Il2 * V)
        V = V + 0.01

    print bdModulos.eschedaTecnica4["modelli"][0]

    for i in range(1,6):
        T = md4.temperatura(i)
        print T
    T = -25
    for i in range(10):
        T = T + 5 
        ambient.Ta = T
        md4.setAmbient(ambient)
        print (T, md4.getVoc())

    print(md4)        

if __name__ == '__main__':
    testB2()
