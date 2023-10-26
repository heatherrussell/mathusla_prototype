import json

class detector:
    def __init__(self, geo_data):
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
        objs=[]
        for fibre_obj in self.fibres.values():
            if f_channel in fibre_obj.interfaces:
                for item in fibre_obj.path:
                    for _,inter in fibre_obj.interfaces.items():
                        if(inter.ID == item):
                            objs.append(inter)
                    for _,bar in fibre_obj.bars.items():
                        if(bar.ID == item):
                            objs.append(bar)       
                    for _,loop in fibre_obj.loops.items():
                        if(loop.ID == item):
                            objs.append(loop)

                if(fibre_obj.interfaces[f_channel].ID=="I1"):
                    objs.reverse()
        return objs
    
class fibre:
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
    def __init__(self, f_length, f_bar, f_ID):
        self.length = f_length
        self.bar = f_bar
        self.ID = f_ID
    def __str__(self) -> str:
        return ", length: {leng}\n".format(leng=self.length)
    
class bar:
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
    def __init__(self, f_length, f_ID):
        self.length = f_length
        self.ID = f_ID
    def __str__(self) -> str:
        return ", length: {var}\n".format(var=self.length)

def process_interfaces(f_fibre, f_fibre_obj):
    for i in f_fibre[ "Interfaces" ]:
        input_interface = interface(i[ "length" ], i[ "bar" ], i["ID"] )
        f_fibre_obj.interfaces[ i[ "channel" ] ] = input_interface

def process_bars(f_fibre, f_fibre_obj):
    for b in f_fibre[ "Bars" ]:
        input_bar = bar(b[ "length" ], b[ "width" ], b[ "thickness" ], b[ "x" ], b[ "y" ], b["ID"])
        f_fibre_obj.bars[ b[ "ID" ] ] = input_bar

def process_loops(f_fibre, f_fibre_obj):
    for l in f_fibre[ "Loops" ]:
        input_loop = loop(l[ "length" ], l["ID"])
        f_fibre_obj.loops[ (l[ "bar0" ], l[ "bar1" ]) ] = input_loop

def process_fibres(f_layer, f_layer_obj):
    for f in f_layer[ "Fibres" ]:
        input_fibre = fibre()
        input_fibre.ID = f['ID']
        input_fibre.path = f['path']
        process_interfaces(f, input_fibre)
        process_bars(f, input_fibre)
        process_loops(f, input_fibre)
        f_layer_obj.fibres[ f[ "ID" ] ] = input_fibre

def build_ch_map(the_dect):
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
    f_ch,f_len=f_chdist
    my_x=None
    my_y=None
    thepath=map[f_ch][0]
    my_z=map[f_ch][1]
    dir=map[f_ch][2]
    cnt=0

    for item in thepath:
        cnt+=1
        f_len=f_len-item.length
        if(f_len<0):
            if(cnt%2==0):
                if((cnt/2)%2==0):
                    if(dir=='x'):
                        my_x=item.x-f_len
                        my_y=item.y
                    else:
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
    return my_x,my_y,my_z

def get_dist(hitinfo):
    ch0,ch1=hitinfo[0]
    t0,t1=hitinfo[1]
    c=30 #cm/ns
    n=1.5 #refractive index

    tdiff =t0-t1
    dist= 300-(c/n)*abs(tdiff)
    
    if(tdiff<0):
        return [ch0,dist]
    else:
        return [ch1,dist]

    