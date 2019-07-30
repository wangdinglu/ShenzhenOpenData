import math

x_pi = 3.14159265358979324 * 3000.0 / 180.0
PI = 3.14159265358979324
def transformGCJ2WGS(gcj):
    d = delta(gcj['lat'], gcj['lon'])
    return {
        'lon': gcj['lon'] - d['lon'],
        'lat': gcj['lat'] - d['lat']
    }


def delta(lat, lon) :
    a = 6378245.0
    ee = 0.00669342162296594323
    dLat = transformLat(lon - 105.0, lat - 35.0)
    dLon = transformLon(lon - 105.0, lat - 35.0)
    radLat = lat / 180.0 * PI
    magic = math.sin(radLat)
    magic = 1 - ee * magic * magic
    sqrtMagic = math.sqrt(magic)
    dLat = (dLat * 180.0) / ((a * (1 - ee)) / (magic * sqrtMagic) * PI)
    dLon = (dLon * 180.0) / (a / sqrtMagic * math.cos(radLat) * PI)
    return {
      'lat': dLat,
      'lon': dLon
    }

def transformLat(x, y):
    ret = -100.0 + 2.0 * x + 3.0 * y + 0.2 * y * y + 0.1 * x * y + 0.2 * math.sqrt(math.fabs(x))
    ret += (20.0 * math.sin(6.0 * x * PI) + 20.0 * math.sin(2.0 * x * PI)) * 2.0 / 3.0
    ret += (20.0 * math.sin(y * PI) + 40.0 * math.sin(y / 3.0 * PI)) * 2.0 / 3.0
    ret += (160.0 * math.sin(y / 12.0 * PI) + 320 * math.sin(y * PI / 30.0)) * 2.0 / 3.0
    return ret

def transformLon(x, y) :
    ret = 300.0 + x + 2.0 * y + 0.1 * x * x + 0.1 * x * y + 0.1 * math.sqrt(math.fabs(x))
    ret += (20.0 * math.sin(6.0 * x * PI) + 20.0 * math.sin(2.0 * x * PI)) * 2.0 / 3.0
    ret += (20.0 * math.sin(x * PI) + 40.0 * math.sin(x / 3.0 * PI)) * 2.0 / 3.0
    ret += (150.0 * math.sin(x / 12.0 * PI) + 300.0 * math.sin(x / 30.0 * PI)) * 2.0 / 3.0
    return ret


def baiduTomars(baidu_point):
    mars_point={'lon':0.0,'lat':0.0}
    x = baidu_point['lon']-0.0065
    y = baidu_point['lat']-0.006
    z = math.sqrt(x*x+y*y)- 0.00002 * math.sin(y * x_pi)
    theta = math.atan2(y, x) - 0.000003 * math.cos(x * x_pi)
    mars_point['lon'] = z * math.cos(theta)
    mars_point['lat'] = z * math.sin(theta)
    return mars_point

def baiduToWSG84(lon,lat):
    baidu_point={'lon':lon,'lat':lat}
    mars_point=baiduTomars(baidu_point)
    gps_point=transformGCJ2WGS(mars_point)
    return gps_point['lon'], gps_point['lat']
