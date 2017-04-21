# coding: utf-8

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
