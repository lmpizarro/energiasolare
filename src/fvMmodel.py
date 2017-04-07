
# coding: utf-8

import math

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
        
class OneDiodeModel(object):
    qq = 1.6e-19 # electron charge  C
    KK = 1.23e-23 # boltzman constant J / °K
    def __init__(self, Ns, Rs, Rsh, n, I0, T):
        '''
        Ns: number of cells in serie
        Rs: R serie Ohm 
        Rsh: R shunt Ohm 
        I0: diode reverse saturation current Amp
        n: ideality factor
        T : ° Kelvin
        '''
        self.Ns = Ns
        self.Rs = Rs
        self.Rsh = Rsh
        self.n = n
        self.I0 = I0
        self.T = T
        self.A = self.qq / (self.n * self.KK * self.T)


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
    odm = OneDiodeModel(60, 0.7, 62.0, 0.25, 9.8e-42, 300.0)

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
