# mathusla_prototype
This project descibes the uvic MATHUSLA prototype geometry through a JSON file
## JSON format
The JSON file is structed as lists of dictionaries, Bars nested in fibres nested in layers, eg.

{Layers:[ {Fibres:[{Bars:[]}]}]}

Layers contain {ID, Direction, z, Fibres[]}
Fibres contain {ID, path, Interfaces[], Bars[], Loops[]}
Interfaces contain {ID, length, channel, bar}
Bars contain {ID, length, width, thickness, x, y}
Loops contain {ID, length, bar0, bar1}

The key,type(value) definitions are:
ID:string - a unique string identifier within a list
Direction:string - x or y for the direction the bars extend in
z:int - the height of the layer in cm
path:[strings] - An ordered list of ID's of objects the fiber passes through
length:int - the length of fibre in the specified object
channel:int - the SiPM channel the fibre connects to
bar:string - ID of the bar the fibre enters
width:int - the width of the bar in cm
thickness:int - the height/thickness of the bar in cm
x:int - the distance from the origin to the face of the bar in cm, defined on the side which connects to the SiPM 
y:int - the distance from the origin to the face of the bar in cm

other defintions:
origin: intersection of the DAQ and back wall at the height of the bottom layer