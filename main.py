import json
import geo_loader as gl

#setup

fin = open('geo.json')
geo = json.load(fin)
fin.close()
the_detector = gl.detector(geo)
my_map=gl.build_ch_map(the_detector)

#analyst code starts here:

my_hit= [[2,7],[12,17]] # currently the onus is on the analyst to pick out channel pairs and ToA [ chpair, ToAs ], should be a larger "pass event" function later

ch_dist = gl.get_dist(my_hit) # returns a [ch, dist] pair, where dist is the distance in cm from the channel

x,y,z=gl.get_xyz(my_map,ch_dist)
listtest = list(gl.get_xyz(my_map,ch_dist))

print(listtest)
print(x,y,z)