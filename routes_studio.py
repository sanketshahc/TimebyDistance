import matplotlib.pyplot as plt
import requests
import numpy
import random

### REMEMBER THAT THIS TAKES LONGITUDE LATITTUDE

## Change these values to adjust
v1 = numpy.array([-73.994010, 40.731944]) # center
v2 = numpy.array([-73.982942, 40.743645]) #1 mi out
max_miles = 10
points = 10
##


# get random coordinates from each zone...even need other coordinates?
def coords(co,d):
    dx = d[0] * random.random()
    dy = d[1] * random.random()
    vd = numpy.array([dx,dy])
    c = co + vd
    return list(c)

m = [[coords(v1, i * (v2-v1)) for j in range(points)] for i in range(1, max_miles + 1)]
durations = []

for k, p in enumerate(m):
    coordinates = ''
    for i, j in enumerate(m[k]):
        coordinates = coordinates + str(m[k][i][0]) + ',' + str(m[k][i][1]) + ';'
    coordinates = coordinates[:-1]
    p = {
        'service': 'route',
        'version': 'v1',
        'profile': 'driving',
        'coordinates': coordinates,
    }
    params = {
        'geometries': 'geojson',
        'overview': 'false',
        'steps': 'false',
    }
    url = f'http://router.project-osrm.org/' \
          f'{p["service"]}/{p["version"]}/{p["profile"]}/{p["coordinates"]}'

    try:
        res = requests.get(url, params) # response object
        res.raise_for_status() # raise http error method
    except requests.exceptions.HTTPError as Er: # handle httperror class
        print("HTTPError!", Er)

    duration = 0
    for i, j in enumerate(res.json()['routes']): #each route
        for k, n in enumerate(res.json()['routes'][i]['legs']): # each leg
            duration += res.json()['routes'][i]['legs'][k]['duration']

    duration = duration / 60
    durations.append(round(duration,0))

#durations filled
labels = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10']

width = 0.35       # the width of the bars: can also be len(x) sequence
fig, ax = plt.subplots()
ax.bar(labels, durations, width)
ax.set_ylabel('Minutes')
ax.set_xlabel('Radius')
ax.set_title('Travel Time for 10 locations from Midtown Manhattan')

plt.show()