#=================================================
#Geometry loader for MATHUSLA UVic Prototype
#by Caleb Miller and Charlie Chen
#
#Contains methods to convert JSON file to easily 
#referenceable channel maps as well as a xyz 
#coordiante finder for a given hit
#=================================================

import json

class detector:
    '''
    base detector object for constructing the prototype
    '''
    def __init__(self, geo_data):
        '''
        Builds the detector, this object contains a dict of 'layer' objects indexed by ID and fills with subobjects     
        '''
        self.layers = {}
        for lyr in geo_data["Layers"]:
            layer_in = layer(lyr["Direction"],lyr["z"])
            process_fibres(lyr, layer_in)
            self.layers[ lyr["ID"] ] = layer_in

    def __str__(self):
        msg="Detector size: %d Layer(s) \n" %(len(self.layers))
        for key,val in self.layers.items():
            msg+="\t"+str(val)
        return msg


class layer:
    '''
    layer class, contains the bar orientation, z posistion information, and a list of fibres indexed by ID
    '''
    def __init__(self, f_direction, f_z):
        self.direction = f_direction
        self.z = f_z
        self.fibres ={}
    
    def __str__(self):
        msg = "Layer height: {z}, Direction: {d} \n".format(z =self.z, d=self.direction)
        for key,val in self.fibres.items():
            msg+="\t"+str(val)
        return msg
    
    def get_path(self, f_channel):
        '''
        Takes a channel number and returns an ordered list of objects the fibre passes through starting at the channel given
        '''
        objs=[]
        for fibre_obj in self.fibres.values():  #find fibre with the channel
            if f_channel in fibre_obj.interfaces:
                for item in fibre_obj.path:  #loop over all items in the list, looking for the next one in the path, once found add to list and find next
                    for _,inter in fibre_obj.interfaces.items():
                        if(inter.ID == item):
                            objs.append(inter)
                    for _,bar in fibre_obj.bars.items():
                        if(bar.ID == item):
                            objs.append(bar)       
                    for _,loop in fibre_obj.loops.items():
                        if(loop.ID == item):
                            objs.append(loop)

                if(fibre_obj.interfaces[f_channel].ID=="I1"): #If the channel corresponds to 2nd interface, reverse list
                    objs.reverse()
        return objs
    
class fibre:
    '''
    The fibre object
    contains dictionaries of interfaces, bars, and loops
    Unique by ID, and contain a path which orders the above objects by ID
    '''
    def __init__(self):
        self.interfaces = {}
        self.bars = {}
        self.loops = {}
        self.ID = -1
        self.path = []
    def __str__(self):
        msg = "Fibre ID: {ID}, fibre path: {path}\n".format(ID=self.ID, path=self.path)
        for key,val in self.interfaces.items():
            msg+="\t\t"+"Interface to channel: {ch}".format(ch=key)
            msg+=str(val)
        for key,val in self.bars.items():
            msg+="\t\t"+"Bar: {bar}".format(bar=key)
            msg+=str(val)
        for key,val in self.loops.items():
            msg+="\t\t"+"Loop between: {ch}".format(ch=key)
            msg+=str(val)
        return msg
    
class interface:
    '''
    The interface object
    contains the length of fibre between a channel and a bar, as well as the channel and bar ID
    '''
    def __init__(self, f_length, f_bar, f_ID):
        self.length = f_length
        self.bar = f_bar
        self.ID = f_ID
    def __str__(self) -> str:
        return ", length: {leng}\n".format(leng=self.length)
    
class bar:
    '''
    The bar object
    contains the bar dimensions, a unique ID, and the x,y coordinate of the face along +x or -y (closest to SiPM)
    '''
    def __init__(self, f_length, f_width, f_thickness, f_x, f_y, f_ID):
        self.length = f_length
        self.width = f_width
        self.thickness = f_thickness
        self.x = f_x
        self.y = f_y
        self.ID = f_ID
    def __str__(self) -> str:
        msg=""
        msg+=", length :{var}".format(var=self.length)
        msg+=", width :{var}".format(var=self.width)
        msg+=", thickness :{var}".format(var=self.thickness)
        msg+=", x :{var}".format(var=self.x)
        msg+=", y :{var}".format(var=self.y)
        msg+="\n"
        return msg

class loop:
    '''
    The loop object
    contains the length of fibre between bars, a unique ID, and the linked bar IDs
    '''
    def __init__(self, f_length, f_ID, f_b0, f_b1):
        self.length = f_length
        self.ID = f_ID
        self.bar0 = f_b0
        self.bar1= f_b1
    def __str__(self) -> str:
        return ", length: {var}\n".format(var=self.length)

def process_interfaces(f_fibre, f_fibre_obj):
    '''
    Takes in a fibre dictionary from JSON and a 'fibre' object
    creates an interface object and adds it to the fibre, indexed by channel number
    '''
    for i in f_fibre[ "Interfaces" ]:
        input_interface = interface(i[ "length" ], i[ "bar" ], i["ID"] )
        f_fibre_obj.interfaces[ i[ "channel" ] ] = input_interface

def process_bars(f_fibre, f_fibre_obj):
    '''
    Takes in a fibre dictionary from JSON and a 'fibre' object
    creates an bar object and adds it to the fibre, indexed by bar ID
    '''
    for b in f_fibre[ "Bars" ]:
        input_bar = bar(b[ "length" ], b[ "width" ], b[ "thickness" ], b[ "x" ], b[ "y" ], b["ID"])
        f_fibre_obj.bars[ b[ "ID" ] ] = input_bar

def process_loops(f_fibre, f_fibre_obj):
    '''
    Takes in a fibre dictionary from JSON and a 'fibre' object
    creates a loop object and adds it to the fibre, indexed by ID
    '''
    for l in f_fibre[ "Loops" ]:
        input_loop = loop(l[ "length" ], l["ID"], l["bar0"], l["bar1"])
        f_fibre_obj.loops[ l[ "ID"] ] = input_loop

def process_fibres(f_layer, f_layer_obj):
    '''
    Takes a dict f_layer from json and a 'layer' object and builds fibre objects from the details and adds to the layer object
    fibres indexed by ID
    '''
    for f in f_layer[ "Fibres" ]:
        input_fibre = fibre()
        input_fibre.ID = f['ID']
        input_fibre.path = f['path']
        process_interfaces(f, input_fibre)
        process_bars(f, input_fibre)
        process_loops(f, input_fibre)
        f_layer_obj.fibres[ f[ "ID" ] ] = input_fibre

def build_ch_map(the_dect):
    '''
    takes the detector object and returns a list of objects (path) the fibre passes through for each channel
    '''
    map=[]
    for ch in range(64):
        obj_list=[]
        for _, layer_obj in the_dect.layers.items():
            temp=layer_obj.get_path(ch)
            if len(temp)==0:
                continue
            else:
                map.append([temp,layer_obj.z,layer_obj.direction])
                break
    return map

def get_xyz(map, f_chdist):
    '''
    given the channel map and distance along the fibre, returns the x,y,z coordinates
    '''
    f_ch,f_len=f_chdist #decouples input pair into channel and distance
    my_x=None
    my_y=None
    thepath=map[f_ch][0] #retrieves the path, z coordinate, and layer orientation (this line and next) for the given channel
    my_z=map[f_ch][1]
    dir=map[f_ch][2]
    cnt=0

    for item in thepath: 
        cnt+=1
        f_len=f_len-item.length #subtract the length of the current object from the total
        if(f_len<0): #If the remaining length is postive goto next object, if negative stop and calcualte posistion in object
            if(cnt%2==0): #cnt is odd for interfaces,loops and even for bars
                if((cnt/2)%2==0): # bars have a reference coordinate on the side entered if cnt%4!=0 and on side exited in cnt%4=0
                    if(dir=='x'):
                        my_x=item.x-f_len
                        my_y=item.y
                    else: #orientated in y
                        my_x=item.x
                        my_y=item.y-f_len
                    return my_x,my_y,my_z
                else:
                    if(dir=='x'):
                        my_x=item.x+f_len+item.length
                        my_y=item.y
                    else:
                        my_x=item.x
                        my_y=item.y+f_len+item.length
                    return my_x,my_y,my_z
            else:
                return 0,0,0
    return my_x,my_y,my_z

def get_dist(hitinfo):
    '''
    given a channel pair and ToA pair [[ch0,ch1],[ToA0,ToA1]] calculates a reference channel and distance from it
    '''
    ch0,ch1=hitinfo[0]
    t0,t1=hitinfo[1]
    c=30 #cm/ns
    n=1.5 #refractive index

    if(t0==-1): t0=0
    if(t1==-1): t1=0
    if(t0>100): return(ch0,0)
    if(t1>100): return(ch1,0)


    tdiff =t0-t1
    dist= 300-(c/n)*abs(tdiff) #assumes 6m fibre
    
    if(tdiff<0):
        return [ch0,dist]
    else:
        return [ch1,dist]

    