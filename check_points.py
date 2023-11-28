import json
import geo_loader as gl
import numpy as np
import ast
#setup

fin = open('geo.json')
geo = json.load(fin)
fin.close()
the_detector = gl.detector(geo)
my_map=gl.build_ch_map(the_detector)

#get known_points

fin= open('knownpoints.txt')
lines=fin.read()
points=lines.split("\n")

for tests in points:
    res= ast.literal_eval(tests)
    knownhit = res[0]
    knowncoords = res[1]
    testxyz = gl.get_xyz(my_map,gl.get_dist(knownhit))

    dist = np.sqrt((knowncoords[0]-testxyz[0])**2+(knowncoords[1]-testxyz[1])**2+(knowncoords[2]-testxyz[2])**2)

    result = "Error: {offset:.1f} cm,  Known location {kxyz}, Reconstructed location {rxyz}"
    print(result.format(offset = dist, kxyz=knowncoords, rxyz=testxyz))
