import math, time

def getLatLong():
    "Returns URL for day/night picture"
    # Define some 'constants'
    ClientRecieveTime=time.time() * 1000
    # QueryTimeZone = 10
    QueryTimeZone = -time.timezone/3600
    QueryTimeZoneOffsetMin = QueryTimeZone * 60
    NISTSendTimeGMTms = ClientRecieveTime - ( QueryTimeZoneOffsetMin * 60 * 1000 )

    # NIST start time in the query time zone
    QueryTimeZoneOffset = ( QueryTimeZoneOffsetMin * 60 * 1000 )
    # Replace this with "QueryTimeZoneOffset = ( -time.timezone * 60 * 1000 )"

    # Client start time in some time zone
    ClientRecieveTimems = ClientRecieveTime

    # what timezone does your computer think it is? - in minutes
    ClientTimeZone = QueryTimeZoneOffsetMin;
    ClientNISTDelta = math.floor(NISTSendTimeGMTms - ClientRecieveTimems)

    currTime = ClientRecieveTime + ClientNISTDelta # ThisMilliseconds
    gmtTime = time.gmtime()
    ssue = currTime / 1000
    TwoPi = 2 * math.pi
    EpochStart = 631065600
    DaysSinceEpoch = (ssue - EpochStart)/ (24*3600)
    RadsPerDay = TwoPi / 365.242191
    Epsilon_g = 279.403303 * (TwoPi / 360)
    OmegaBar_g = 282.768422 * (TwoPi / 360)
    Eccentricity = 0.016713
    MeanObliquity = 23.440592 * (TwoPi / 360);
    # Calculate sun_ecliptic_longitude
    N = RadsPerDay * DaysSinceEpoch
    N = N % TwoPi
    if N < 0:
        N += TwoPi # This should never be executed, but never mind
    M_Sun = N + Epsilon_g - OmegaBar_g
    if M_Sun < 0:
        M_Sun += TwoPi # This should never be executed either
    # Now we solve keplers equation. For those who are interested keplers 
    # equation is all about plotting the orbit of an object on the 
    # elliptic plane.
    E = M_Sun
    while 1:
        delta = E - (Eccentricity*math.sin(E)) - M_Sun
        if (abs(delta) <= 1E-10):
            break
        E -= delta / (1 - (Eccentricity*math.cos(E)))
    # End of the keplers equation solution
    myLambda = OmegaBar_g + (2 * math.atan(math.sqrt((1+Eccentricity) / (1-Eccentricity)) * math.tan(E/2)))
    # There, finished calculating the sun ecliptic longitude
    # Now we calculate the ecliptic to equatorial (something or other)
    sin_e = math.sin(MeanObliquity)
    cos_e = math.cos(MeanObliquity)
    alpha = math.atan2(math.sin(myLambda)*cos_e, math.cos(myLambda))
    delta = math.asin(sin_e*math.sin(myLambda));
    # End of ecliptic to equatorial
    # We calculate the Julian date here, Python could probably do this better
    # I leave it to the casual observer to replace the following few lines
    y = gmtTime[0] # Year
    m = gmtTime[1] # Month number
    z = gmtTime[2] # Day number
    A = y / 100
    B = 2 - A + (A/4)
    C = 365.25 * y
    D = 30.6001 * (m+1)
    JD = B + C + D + z + 1720994.5
    T = (JD - 2451545) / 36525
    T0 = ((((T + 2.5862E-5) * T) + 2400.051336) * T) + 6.697374558
    T0 = T0 % 24
    if T0 < 0:
        T0 += 24
    UT = (float(gmtTime[3])) + ((float(gmtTime[4]) + (float(gmtTime[5]) / 60)) / 60)
    T0 += UT * 1.002737909
    T0 = T0 % 24
    if T0 < 0:
        T0 += 24

    tmp = alpha - ((TwoPi/24)*T0);
    while tmp < -math.pi:
        tmp += TwoPi
    while tmp > math.pi:
        tmp -= TwoPi

    # Now calculate our longitude and latitude
    lon = tmp * (360/TwoPi)
    lat = delta * (360/TwoPi)

    # Generate the path of the appropriate xearth image
    lon = round(lon)
    
    if (lon % 2 != 0):
      if (lon > 0):
        lon -= 1
      else:
        lon += 1

    lon = round(lon/2) * 2
    if lon <= -181:
        lon = -180
    if lon >= 181:
        lon = 180
    # lat is odd
    lat = round(lat)
    if (lat % 2 == 0):
        if lat > 0:
            lat -= 1
        else:
            lat += 1
    # Need to do different calculations for negative and positive values of lat
    # to emulate the way javascript handles rounding
    if lat < 0:
        lat = (round(int(lat/2) - 1) * 2) + 1
    else:
        lat = (round(lat/2 - 1) * 2) + 1
  
    if lat <= -24:
        lat = -23
    if lat >= 24:
        lat = 23

    if lat < 0:
        latStr = str(int(-lat)) + "S"
    else:
        latStr = str(int(lat)) + "N"
    if lon < 0:
        lonStr = str(int(-lon)) + "S"
    else:
        lonStr = str(int(lon)) + "N"
    # url = "http://www.time.gov/" + getLatLong()
    # return 'http://www.time.gov/images/xearths/11N/154N.jpg'
    return "images/xearths/" + latStr + "/" + lonStr + ".jpg"
