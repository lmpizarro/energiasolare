# coding: utf-8

import math


class Ambient(object):
    def __init__(self, Ta, Sa, Va):
        self.Ta = Ta
        self.Sa = Sa
        self.Va = Va

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
        S = self.Sa
        Ta = self.Ta
        Va = self.Va

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



    def __str__(self):
        str_ = ("Ta: %.3f Sa: %.3f Va: %.3f")%(self.Ta, self.Sa, self.Va)


