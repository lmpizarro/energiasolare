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
                "Iirr":8.5488, "source": "Laudani"},
            {"Rs": 0.4759, "nref": 0.74, "Rsh": 116.1465, "I0": 5.689E-14,
                "Iirr":8.5147, "source": "Laudani"},
            {"Rs": 0.3496, "nref": 1.04, "Rsh": 229.2422, "I0": 7.021E-10,
                "Iirr":8.4929, "source": "Laudani"},
            {"Rs": 0.2371, "nref": 1.34, "Rsh": 4393.8, "I0": 1.2857E-7,
                "Iirr":8.4805, "source": "Laudani"}
            ]}

BD = [eschedaTecnica1, eschedaTecnica2, eschedaTecnica3, eschedaTecnica4]

class BDPFV(object):
    def __init__(self, BD):
        self.BD = BD
        self.query = []

    def getWPMa(self, wpl):
        a = []
        for e in self.BD:
            if e["datiElettrici"]["Pn"] > wpl:
               a.append(e) 
        self.query =  a        

    def getWPMe(self, wpl):
        a = []
        for e in self.BD:
            if e["datiElettrici"]["Pn"] < wpl:
               a.append(e) 
        self.query =  a        

    def getWPEq(self, wpl):
        a = []
        for e in self.BD:
            if e["datiElettrici"]["Pn"] == wpl:
               a.append(e) 
        self.query =  a


    def getAll(self):
        a = []
        for e in self.BD:
               a.append(e) 
        self.query =  a




    def __str__(self):
        format1 = "%.3f %.3f %.3f %.3f %.3f \n" 

        str1 = "Wp:     Voc:   Isc:  Vmp:   Imp:\n"
        for e in self.query:
            a  = e["datiElettrici"] 
            str1 +=  (format1)%(a["Pn"], a["Voc"], a["Isc"], a["Vmp"], a["Imp"])

        return str1    

def testBD():
    bd = BDPFV(BD)

    a = bd.getWPMa(300)
    print bd

    print 
    a = bd.getWPMe(280)
    print bd

    print 
    a = bd.getWPEq(320)
    print bd

    print 
    a = bd.getAll()
    print bd


if __name__ == '__main__':
    testBD()       
