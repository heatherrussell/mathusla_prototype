import json
import geo_loader as gl

fin = open('geo.json')
geo = json.load(fin)

the_detector = gl.detector(geo)
my_map=gl.build_ch_map(the_detector)

x,y,z=gl.get_xyz(my_map,0,264) #5 is array posistion for ch39 currently
print(x,y,z)
#print(the_detector)
#gl.get_xyz_using_channel_length(the_detector,0,234)



#print(my_map)