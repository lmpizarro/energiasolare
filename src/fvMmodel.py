
# coding: utf-8

import math
import constants

eschedaTecnica1 = {"datiElettrici" :{"Pn":320, "Vmp": 54.7, "Imp": 5.86, "Voc": 64.8, "Isc": 6.27},
        "CoefficienteDiTemperatura":{"NOCT": 45, "Pn": -1.056, "Voc": -0.16848, "Isc":0.003135},
        "CaratteristicheMeccaniche":{"lungh":1.559, "largh":1.046, "alt":0.046, "cell":96,\
                    "peso":18.6},

        "marca": "SunForte", "modello":"PM096B00"}

eschedaTecnica2 = {"datiElettrici" :{"Pn":320, "Vmp": 54.7, "Imp": 5.86, "Voc": 64.8, "Isc": 6.24},
        "CoefficienteDiTemperatura":{"NOCT": "ND", "Pn": -1.216, "Voc": -0.1766, "Isc":0.0035},
        "CaratteristicheMeccaniche":{"lungh":1.559, "largh":1.046, "alt":0.046, "cell":96,\
                    "peso":18.6},
        "marca": "SunPower", "modello":"E20-327"}

eschedaTecnica3 = {"datiElettrici" :{"Pn":280, "Vmp": 32.7, "Imp": 8.57, "Voc": 38.9, "Isc": 9.06},
        "CoefficienteDiTemperatura":{"NOCT": 46, "Pn": -1.176, "Voc": -0.1167, "Isc":0.00453},
        "CaratteristicheMeccaniche":{"lungh":1.640, "largh":0.992, "alt":0.035,\
                "cell":60, "peso": 10.5},
        "marca": "Benq", "modello":"Aer PM060M01"}


eschedaTecnica4 = {"datiElettrici" :{"Pn":235, "Vmp": 29.6, "Imp": 7.94, \
                                     "Voc": 36.8, "Isc": 8.40},
        "CoefficienteDiTemperatura":{"NOCT": 45, "Pn": -1.1985, "Voc": -0.12512,\
                "Isc":0.00294},
        "CaratteristicheMeccaniche":{"lungh":1.667, "largh":1.000, "alt":0.045,\
                "cell":60, "peso": 19.0},
        "marca": "BP Solar", "modello":"Q series",\
        "modelli": [{"Rs": 0.733, "nref": 0.25, "Rsh": 62.5481, "I0": 9.84E-42,
            "Iirr":8.5794, "source": "Laudani"},
            {"Rs": 0.6226, "nref": 0.44, "Rsh": 76.6973, "I0": 1.2434E-23,
                "Iirr":8.5488, "source": "Laudani"}
            ]}




"""
 riferito alle condizioni standard IEC
 temperatura della cella fotovoltaica pari a 25°C
 irraggiamento di 1000 W/m2 e velocità del vento di 1 m/s
 
 NOCT: Nominal Operating Cell Temperature

"""

class modelloB1(object):
    def __init__(self, m):
        vprima = m.Voc - m.Vmp
        self.Rsh = ((m.Isc * vprima / m.Imp) + m.Voc)/(2*m.Isc)
        self.Rs = (self.Rsh * m.Imp - vprima) / m.Imp
        self.Il = m.Voc / self.Rsh

    def __str__(self):    
        str1 = ("Rsh: %.3f Rs: %.3f IL: %.3f\n")% (self.Rsh, self.Rs, self.Il)
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

       
class Ambient(object):
    def __init__(self, Ta, Sa, Va):
        self.Ta = Ta
        self.Sa = Sa
        self.Va = Va


    def __str__(self):
        str_ = ("Ta: %.3f Sa: %.3f Va: %.3f")%(self.Ta, self.Sa, self.Va)


class OneDiodeModel(object):
    #{'Rsh': 62.5481, 'nref': 0.25, 'Rs': 0.733, 'I0': 9.84e-42, 'source':
    #        'Laudani', 'Iirr': 8.5794}
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

def test01():        
    md1 = Modulo(eschedaTecnica1)
    md2 = Modulo(eschedaTecnica2)
    md3 = Modulo(eschedaTecnica3)
    print (md1)
    print (md2)
    print (md3)

    mbcMd3 = modelloB1(md3)

    print(mbcMd3)

    cel1 = cella (md1)
    print (cel1)
    mbc = modelloB1(cel1)

    print (mbc)

    ca = cavio(100, 32.5, "Cu")
    print ( ca.R(70))

if __name__ == '__main__':
    # Rs, Rsh, n, I0, T
    Ta = 30
    Ws = 4
    Ss = 1500

    ambient = Ambient (Ta, Ss, Ws)

    md4 = Modulo(eschedaTecnica4)
    md4.setAmbient(ambient)
    T = md4.temperatura(4)

    odm = OneDiodeModel(eschedaTecnica4, 0, T + 273.0)

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

    print eschedaTecnica4["modelli"][0]

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
