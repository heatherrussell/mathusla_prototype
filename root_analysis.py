import ROOT, json
import geo_loader as gl
import matplotlib.pyplot as plt


fin = open('geo.json')
geo = json.load(fin)
fin.close()
the_detector = gl.detector(geo)
my_map=gl.build_ch_map(the_detector)

chlist =[10,8,7,50,12,11,14,2,1,15,0,5,4,19,6,9,25,21,24,13,30,17,31,27,18,16,28,23,26,44,20,22,40,41,52,43,58,45,46,47,32,33,60,35,29,37,38,39,56,57,3,59,34,61,62,63,48,49,36,51,42,53,54,55]

fin = ROOT.TFile.Open("clean.root")

hitlist=[]
events=[]
hit_xyz=[]
xyz_list=[]
for event in fin.tree:
    for i in range(len(event.Channels)):
        target=event.Channels[i]
        myToA = event.ToA[i]
        cnt=0
        for ch in event.Channels:
            if (ch == chlist[target]):
                if any(ch in sl for sl in hitlist):
                    break
                myhit=[[ch,target],[event.ToA[cnt],myToA]]
                hitlist.append(myhit)
                xyz_list.append(list(gl.get_xyz(my_map,gl.get_dist(myhit))))
                break
            cnt+=1
    events.append(hitlist)
    hitlist=[]

clean_hits=[]
for hit in xyz_list:
    if hit[0]>400 or hit[0]<-400:
        continue
    if hit[1]>400 or hit[1]<-400:
        continue
    clean_hits.append(hit)

#print(clean_hits)

fig = plt.figure()
ax = fig.add_subplot(projection='3d')

for hit in clean_hits:
    mycolor=''
    if(hit[2]==0): mycolor='red'
    elif(hit[2]==111): mycolor='green'
    elif(hit[2]==222): mycolor='blue'
    elif(hit[2]==333): mycolor='purple'

    ax.scatter(hit[0],hit[1],hit[2],color=mycolor,marker='.')

ax.set_xlabel("x")
ax.set_ylabel("y")
ax.set_zlabel("z")

plt.savefig("hitmap.png", bbox_inches='tight')

