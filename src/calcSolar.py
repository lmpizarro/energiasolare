# coding: utf-8
import math
'''
http://www.itacanet.org/the-sun-as-a-source-of-energy/part-3-calculating-solar-angles/
http://www.pveducation.org/pvcdrom/properties-sunlight/solar-radiation-tilted-surface

calc solar angles 

'''
Isc = 1367 # W/m2
TO_RAD = math.pi / 180.0 
TO_DEG = 180.0 / math.pi

class SunPositionCalculator (object):
    def __init__(self, lat, long_, gmtOffset):
        self.lat = lat
        self.long_ = long_
        self.DGMT = gmtOffset
        self.LSTM =  15 * self.DGMT

    def declination_angle(self, day_of_year):
        dec =  23.45 * math.sin(2.0*math.pi*((float(day_of_year) - 80.0)/365.0))
        return dec

    # equation of time
    def EOT(self, d):
        B = TO_RAD * (float(d)-81.0) * (360.0 / 365.0)
        return 9.87 * math.sin(2*B) - 7.53 * math.cos(B) - 1.5 * math.sin(B)
    #
    # http://pveducation.org/pvcdrom/2-properties-sunlight/solar-time
    #
    def HRA(self, day_of_year, hourOfDay): # LT in hours
        '''
        d: day of year
        LT: local hour of day
        DGMT: delta gmt
        long_ : longitude
        '''
        Eot =self.EOT(day_of_year)

        hourOfDay = int(hourOfDay)

        if hourOfDay < 0:
            hourOfDay = 0.0

        if hourOfDay > 24:
            hourOfDay = 23.0


        hourOfDay = hourOfDay + 0.5
             

        # local solar time
        LST = hourOfDay + self.TC(day_of_year)/60.0

        return 15 * (LST - 12)

    def TC(self, day_of_year):
        eot = self.EOT(day_of_year) 
        # time correction factor
        TC = 4.0 * (self.long_  - self.LSTM) + eot
        return TC

    def elevation_angle(self, d, hourOfDay):
        Hra =  self.HRA(d, hourOfDay) * TO_RAD 
        declination = self.declination_angle (d) * TO_RAD 
        lat = self.lat * TO_RAD 

        invalpha = math.sin(declination) * math.sin(lat)\
                +  math.cos(declination) * math.cos(lat) * math.cos(Hra)

        alpha = math.asin (invalpha) * TO_DEG 
        return alpha

    def sun_rise (self,d):
        dec = self.declination_angle (d) * TO_RAD 
        lat = self.lat * TO_RAD
        tc = self.TC(d)

        c1 = -math.sin(lat)*math.sin(dec)
        c2 = math.cos(lat)*math.cos(dec)

        return 12.0 - (1.0 / 15.0) * math.acos( c1/c2 ) * TO_DEG - tc / 60

    def sun_set (self,day_of_year):
        dec = self.declination_angle (day_of_year) * TO_RAD 
        lat = self.lat * TO_RAD 
        eot = self.EOT(day_of_year)

        tc = self.TC(day_of_year)

        c1 = -math.sin(lat)*math.sin(dec)
        c2 = math.cos(lat)*math.cos(dec)

        return 12.0 + (1.0 / 15.0) * math.acos( c1/c2 ) * TO_DEG - tc / 60

    def angle_of_incidence_ec(self, day_of_year, hour, tilt_angle):
        '''
        1 < day_of_year < 365 
        0 < hour < 24
        0 < tilt_angle < 90
        output DEGREES
        '''
        tilt_angle = TO_RAD * tilt_angle
        HRA = self.HRA(day_of_year, hour) * TO_RAD
        declination = self.declination_angle (day_of_year) * TO_RAD


        if self.lat >= 0:
            sign = -1
        else:
            sign = 1

        c1 = math.cos(declination)*math.cos(self.lat + sign *  tilt_angle) *\
                math.cos(HRA)
        c2 =  math.sin(declination)*math.sin(self.lat + sign *  tilt_angle)        

        inc_angle = math.acos( (c1 + c2)) * TO_DEG 
        return inc_angle

def test2():
    lat = -40
    long_ = -60
    gmtOffset = -3
    day = 180
    ang_of_module = 41.0

    spc = SunPositionCalculator(lat, long_, gmtOffset)

    srise = spc.sun_rise(day)
    sset = spc.sun_set(day)

    print ("sr: ", srise , "ss: ", sset )
    # HRA(d, LT, DGMT, long_): # LT in hours

    #for i,h in enumerate(range(int(srise + .5) - 2,int(sset + 0.5) + 2,1)):
    for h in range(0, 24,1):
        el_angle = spc.elevation_angle(day, h)
        inc_angle = spc.angle_of_incidence_ec(day, h, ang_of_module)
        if h > srise and h < sset:
            print (("h:%d ele: %.3f hra: %.3f inc_angle: %.3f ")%(h,
                el_angle, spc.HRA(day, h), inc_angle))

def test_declination():
    lat = -40
    long_ = -60
    gmtOffset = -3
    day = 180
    ang_of_module = 65.0

    spc = SunPositionCalculator(lat, long_, gmtOffset)

    for i in range (1,365):
        print(i, spc.declination_angle (i))

if __name__ == '__main__':
    test2()
