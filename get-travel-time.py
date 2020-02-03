import geoip2.database
import argparse
import math

def haversine(coord1, coord2):
    R = 6372800  # Earth radius in meters
    lat1, lon1 = coord1
    lat2, lon2 = coord2
    
    phi1, phi2 = math.radians(lat1), math.radians(lat2) 
    dphi       = math.radians(lat2 - lat1)
    dlambda    = math.radians(lon2 - lon1)
    
    a = math.sin(dphi/2)**2 + \
        math.cos(phi1)*math.cos(phi2)*math.sin(dlambda/2)**2
    
    return 2*R*math.atan2(math.sqrt(a), math.sqrt(1 - a))

parser = argparse.ArgumentParser()
parser.add_argument("firstIP")
parser.add_argument("secondIP")
parser.add_argument("-k", "--kmph", help="Speed (in kmph)", default="930")
args = parser.parse_args()

reader = geoip2.database.Reader('./GeoLite2-City.mmdb')

coord1 = reader.city(args.firstIP)
coord2 = reader.city(args.secondIP)

R = 6372800
phi1, phi2 = math.radians(coord1.location.latitude), \
    math.radians(coord2.location.latitude)
dphi = math.radians(coord2.location.latitude - coord1.location.latitude)
dlambda = math.radians(coord2.location.longitude - coord1.location.longitude)

a = math.sin(dphi/2)**2 + \
    math.cos(phi1)*math.cos(phi2)*math.sin(dlambda/2)**2

distance = 2*R*math.atan2(math.sqrt(a), math.sqrt(1 - a)) / 1000

hours = math.floor(distance / int(args.kmph))
minutes = math.floor(((distance / int(args.kmph)) * 60) % 60)

print("Time to travel " + str(math.floor(distance)) + \
    " kilometers (Hours:Minutes)\n-> " + str(hours)[:-2] + ":" + str(minutes)[:-2])
reader.close()
