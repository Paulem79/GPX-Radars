import csv
from gpx import GPX, Waypoint, Latitude, Longitude

# Numéro de radar;Type de radar;Date de mise en service;VMA ;Latitude; Longitude
donnees = []

with open('radars.csv', newline='\n', encoding='iso-8859-1') as csvfile:
    spamreader = csv.reader(csvfile, delimiter=';', quotechar='\"')
    for i, ligne in enumerate(spamreader):
        if i == 0:
            continue
        donnees.append(ligne)

class Radar:
    def __init__(self, identifiant: int, type_radar: str, date_service: str, vma: int, lat: str, long: str):
        self.identifiant = identifiant
        self.type_radar = type_radar
        self.date_service = date_service
        self.vma = 0 if vma == "NA" else int(vma)
        self.lat = lat
        self.long = long
        
    def to_waypoint(self) -> Waypoint:
        lat = Latitude(self.lat.replace(',', '.'))
        lon = Longitude(self.long.replace(',', '.'))
        wpt = Waypoint(lat=lat, lon=lon)
        wpt.name = f"Radar {self.identifiant}"
        return wpt
        
    def __eq__(self, other):
        return self.identifiant == other.identifiant and self.type_radar == other.type_radar and self.date_service == other.date_service and self.vma == other.vma and self.lat == other.lat and self.long == other.long
    
    def __hash__(self):
        return hash((self.identifiant, self.type_radar, self.date_service, self.vma, self.lat, self.long))
    
    def __str__(self):
        return f"{self.identifiant} {self.type_radar} ({self.date_service}, {self.vma}) en {self.lat} {self.long}"

radars = []

gpx = GPX()

for donnee in donnees:
    radar = Radar(donnee[0], donnee[1], donnee[2], donnee[3], donnee[4], donnee[5])
    waypoint = radar.to_waypoint()
    gpx.wpt.append(waypoint)

gpx.write_gpx("output.gpx")