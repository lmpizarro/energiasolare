def declination_angle(d):
    return (23.45 * math.pi / 180) * math.sin(2.0*math.pi*((284.0 + float(d))/36.25))

# equation of time
def EOT(n):
    B = (math.pi / 180.0)  * (float(n)-81.0) * (360.0 / 365.0)
    return 9.87 * math.sin(2*B) - 7.53 * math.cos(B) - 1.5 * math.sin(B)
#
# http://pveducation.org/pvcdrom/2-properties-sunlight/solar-time
#
def HRA(d, LT, DGMT, long_): # LT in hours
    '''
    d: day of year
    LT: local hour of day
    DGMT: delta gmt
    long_ : longitude
    '''
    LSTM = 15 * DGMT
    Eot =EOT(d)

    # time correction factor
    TC = 4.0 * (long_  - LSTM) + Eot

    # local solar time
    LST = LT + TC/60.0

    return 15 * (LST - 12) 

def elevation_angle(d, LT, DGMT, long_, lat):
    Hra =  HRA(d, LT, DGMT, long_) * math.pi/ 180.0
    declination = declination_angle (d) 
    invalpha = math.sin(declination*math.pi/180.0) * math.sin(lat*math.pi / 180.0)\
            +  math.cos(declination*math.pi/180.0) * math.cos(lat*math.pi / 180.0)\
            * math.cos(Hra)

    return math.asin (invalpha) * 180 / math.pi

def test1():
    for n,i in enumerate(range(0,365,30)):
        print (n,i, declination_angle(i), EOT(i))

    # HRA(d, LT, DGMT, long_): # LT in hours
    for i,h in enumerate(range(0,24,1)):
        print (i, elevation_angle(1, h, -3, -60, -40), HRA(1, h, -3, -60))




