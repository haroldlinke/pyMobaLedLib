
// KEA
// The two main functions use global variables, so we have to
// set all this up unless the functions are going to get changed.

var ClientRecieveTime=new Date();

var QueryTimeZone = -7;
var QueryTimeZoneOffsetMin = QueryTimeZone * 60 // -420

var NISTSendTimeGMTms = ClientRecieveTime.getTime() - ( QueryTimeZoneOffsetMin * 60 * 1000 );


// NIST start time in the query time zone
var QueryTimeZoneOffset = ( QueryTimeZoneOffsetMin * 60 * 1000 ) ;

// Client start time in some time zone
var ClientRecieveTimems = ClientRecieveTime.getTime() ;

// what timezone does your computer think it is? - in minutes
//var ClientTimeZone = Math.floor(NISTSendTime.getTimezoneOffset()) ;
var ClientTimeZone = QueryTimeZoneOffsetMin;

var ClientNISTDelta = Math.floor(NISTSendTimeGMTms - ClientRecieveTimems);

//WScript.echo(QueryTimeZoneOffset)
//WScript.echo(" ")
//WScript.echo(ClientRecieveTime)
//WScript.echo(" ")
//WScript.echo(ClientTimeZone)
//WScript.echo(" ")
//WScript.echo(ClientNISTDelta)
//WScript.echo(" ")

WScript.echo(updatexearthImage());


function updatexearthImage() {

  // get the computer's date
  var Thisdate = new Date();
  // convert to NIST date, using offset calculated in ClientNISTDelta
  ThisMilliseconds =  Thisdate.getTime() + ClientNISTDelta ;

  // KEA get rid of reference to DOM, just return the data
  // document.images['xearth'].src = xearthSrc(ThisMilliseconds);
  return xearthSrc(ThisMilliseconds);

  // setTimeout("updatexearthImage()", 10000);
}


function xearthSrc(ThisMilliseconds) {

var ssue = ThisMilliseconds / 1000;
var TWOPI = 2 * Math.PI;
var EpochStart = 631065600;
var DaysSinceEpoch = (ssue - EpochStart) / (24*3600);

var RadsPerDay = TWOPI / 365.242191;

var Epsilon_g = 279.403303 * (TWOPI / 360);
var OmegaBar_g = 282.768422 * (TWOPI / 360);
var Eccentricity = 0.016713;

var MeanObliquity = 23.440592 * (TWOPI / 360);

//Compute lambda = sun_ecliptic_longitude(ssue)
//Begin sun_ecliptic_longitude
  var D = DaysSinceEpoch;
  var N = RadsPerDay * D;
  N = N % TWOPI;
  if (N < 0) N += TWOPI;

  var M_sun = N + Epsilon_g - OmegaBar_g;
  if (M_sun < 0) M_sun += TWOPI;

  //Compute var E = solve_keplers_equation(M_sun);
  //Begin solve_keplers_equation
    var E = M_sun;
    var delta;
    while (1) {
      delta = E - (Eccentricity*Math.sin(E)) - M_sun;
      if (Math.abs(delta) <= 1E-10) break;
      E -= delta / (1 - (Eccentricity*Math.cos(E)));
    }
  //End solve_keplers_equation

  var lambda = OmegaBar_g + (2 * Math.atan(Math.sqrt((1+Eccentricity) / (1-Eccentricity)) * Math.tan(E/2)));
//End sun_ecliptic_longitude


//Compute ecliptic_to_equatorial(lambda, 0.0, alpha, delta)
  var sin_e = Math.sin(MeanObliquity);
  var cos_e = Math.cos(MeanObliquity);
  var alpha = Math.atan2(Math.sin(lambda)*cos_e, Math.cos(lambda));
  var delta = Math.asin(sin_e*Math.sin(lambda));
//End ecliptic_to_equatorial

//Compute GST(ssue)
  //Compute JD = julian_date(year, month, day)
    var TmpDate = new Date(ThisMilliseconds);
	var OffsetMilliseconds = ThisMilliseconds ; //+ (60000*TmpDate.getTimezoneOffset());
    var ThisDate = new Date(OffsetMilliseconds);
    var y = ThisDate.getYear();
      if (y < 1000) y += 1900;
    var m = ThisDate.getMonth() + 1;
    var z = ThisDate.getDate();
    
//	if ((m==1) || (m==2)) {
//	  y -= 1;
//	  m += 12; }

	var A = y / 100;
	var B = 2 - A + (A/4);
	var C = 365.25 * y;
	var D = 30.6001 * (m+1);

	var JD = B + C + D + z + 1720994.5;
  //End julian_date

  var T = (JD - 2451545) / 36525;
  var T0 = ((((T + 2.5862E-5) * T) + 2400.051336) * T) + 6.697374558;

  T0 = T0 % 24;
  if (T0 < 0) T0 += 24;

  var UT = ThisDate.getHours() + ((ThisDate.getMinutes() + (ThisDate.getSeconds() / 60)) / 60);
 
  T0 += UT * 1.002737909;
  T0 = T0 % 24;
  if (T0 < 0) T0 += 24;
//End GST

var tmp = alpha - ((TWOPI/24)*T0);
while (tmp < -Math.PI) {tmp += TWOPI;};
while (tmp > Math.PI) {tmp -= TWOPI;};

var lon = tmp * (360/TWOPI);
var lat = delta * (360/TWOPI);

//Generate the path of the appropriate xearth image

//lon is even
lon = Math.round(lon);
//if (lon & 1 != 0) {
if (lon % 2 != 0) {
  if (lon > 0) {
    lon -= 1;
    }
  else {
    lon += 1;
    }
  }
  
  // force even for mozilla 4.01-4.05
  // Consolidate lines, 4/5/01 - PRF
  lon = Math.round(lon/2) * 2;
  
if (lon <= -181) lon = -180;
if (lon >= 181) lon = 180;

//lat is odd
lat = Math.round(lat);
//if (lat & 1 == 0) {
if (lat % 2 == 0) {
  if (lat > 0) {
    lat -= 1;
    }
  else {
    lat += 1;
    }
  }
  
  // force odd for mozilla 4.01-4.05
  // Fixed broken algorithm, 4/5/01 - PRF
  lat =  (Math.round(lat/2 - 1) * 2) + 1;
  
  
if (lat <= -24) lat = -23;
if (lat >= 24) lat = 23;

var latStr; var lonStr;
if (lat < 0) 
  latStr = (-lat) + "S";
else 
  latStr = lat + "N";

if (lon < 0) 
  lonStr = (-lon) + "S";
else 
  lonStr = lon + "N";

return "images/xearths/" + latStr + "/" + lonStr + ".jpg";
//return lon;
}
