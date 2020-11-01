import numpy as np
import matplotlib.pyplot as plt



#grafik arasi bosluk yap
#try catch




f = open("lab8_3.91-6.11-1.57.mbd","r")


#firstpart
map = {}
map = {}
for line in f:
    couple = ""
    splittedLine=line.strip().split(",")
    couple = couple + splittedLine[1]
    couple = couple + " " +splittedLine[2]
    value = splittedLine[3]
        
        
    if couple in map:
        map[couple]=map[couple]+" "+ value
            
    else:
        map[couple] = value



for key in map:
    print(key)





for key in map:
    temp=[]
    temp=map[key].split()
    map[key]=temp

minmax={}
for key in map:
    minmax[key]=[max(map[key]),min(map[key])]

arrange={}
for key in map:
    arrange[key]=[]
    x=range(int(minmax[key][0]),int(minmax[key][1])+1)
    for n in x:
        arrange[key].append(n)

zeros={}
for key in arrange:
    zeros[key]=[]
    for item in arrange[key]:
        zeros[key].append(0)


for key in map:
    for item in map[key]:
        k=int(item)-arrange[key][0]
        zeros[key][k]=zeros[key][k]+1
            

list=[]
namelist=[]
for key in map:
    list.append(arrange[key])
    list.append(zeros[key])
    namelist.append(key)
    

plt.figure(figsize=(15,10))
x=0
plt.subplot(2, 4, 1)
plt.bar(list[x],list[x+1], color='orange', width = 0.75,edgecolor = "none")
plt.title(namelist[x/2],fontsize=10,fontweight='bold')
x=x+2
plt.subplot(2, 4, 2)
plt.bar(list[x],list[x+1], color='orange', width = 0.75,edgecolor = "none")
plt.title(namelist[x/2],fontsize=10,fontweight='bold')
x=x+2
plt.subplot(2, 4, 3)
plt.bar(list[x],list[x+1], color='orange', width = 0.75,edgecolor = "none")
plt.title(namelist[x/2],fontsize=10,fontweight='bold')
x=x+2
plt.subplot(2, 4, 4)
plt.bar(list[x],list[x+1], color='orange', width = 0.75,edgecolor = "none")
plt.title(namelist[x/2],fontsize=10,fontweight='bold')
x=x+2
plt.subplot(2, 4, 5)
plt.bar(list[x],list[x+1], color='orange', width = 0.75,edgecolor = "none")
plt.title(namelist[x/2],fontsize=10,fontweight='bold')
x=x+2
plt.subplot(2, 4, 6)
plt.bar(list[x],list[x+1], color='orange', width = 0.75,edgecolor = "none")
plt.title(namelist[x/2],fontsize=10,fontweight='bold')
x=x+2
plt.subplot(2, 4, 7)
plt.bar(list[x],list[x+1], color='orange', width = 0.75,edgecolor = "none")
plt.title(namelist[x/2],fontsize=10,fontweight='bold')
x=x+2
plt.subplot(2, 4, 8)
plt.bar(list[x],list[x+1], color='orange', width = 0.75,edgecolor = "none")
plt.title(namelist[x/2],fontsize=10,fontweight='bold')

plt.show()

f.close()




#secondpart

f = open("lab8_3.91-6.11-1.57.mbd","r")
w=100.0

def instFreq (Tt, Ttw):
    f=w/float(float(Ttw)-float(Tt))
    return f
    
    
time={}
time={}
for line in f:
    couple = ""
    splittedLine=line.strip().split(",")
    couple = couple + splittedLine[1]
    couple = couple + " " +splittedLine[2]
    value= splittedLine[0]
        
        
    if couple in time:
        time[couple]=time[couple]+" "+ value
            
    else:
        time[couple] = value
        
    

for key in time:
    temp=[]
    temp=time[key].split()
    time[key]=temp


frekans={}
for key in time:
    frekans[key]=[]
    


for key in time:
    window=[]
    if(len(window)<100):
        for x in range(100):
            window.append(time[key][x])
                
    if(len(window)==100):
        for y in range(100,len(time[key])):
            frekans[key].append(instFreq (window[0], window[99]))
            window.append(time[key][y])
            window.pop(0)




#Anlik frekans degisimleri
fig, ax=plt.subplots(2,4,figsize=(20, 10), tight_layout=True)
#fig.suptitle('Anlik frekans degisimleri',fontsize=20,fontweight='bold')

list=[]
namelist=[]
for key in frekans:
    for item in frekans[key]:
        item=float(item)
      
for key in frekans:
    list.append(range(len(frekans[key])))
    list.append(frekans[key])
    namelist.append(key)
     
x=0
ax[0,0].plot(list[x],list[x+1],'orange')
ax[0, 0].set_title(namelist[x/2],fontsize=10,fontweight='bold')
x=x+2
ax[0,1].plot(list[x],list[x+1],'orange')
ax[0, 1].set_title(namelist[x/2],fontsize=10,fontweight='bold')
x=x+2
ax[0,2].plot(list[x],list[x+1],'orange')
ax[0, 2].set_title(namelist[x/2],fontsize=10,fontweight='bold')
x=x+2
ax[0,3].plot(list[x],list[x+1],'orange')
ax[0, 3].set_title(namelist[x/2],fontsize=10,fontweight='bold')
x=x+2
ax[1,0].plot(list[x],list[x+1],'orange')
ax[1, 0].set_title(namelist[x/2],fontsize=10,fontweight='bold')
x=x+2
ax[1,1].plot(list[x],list[x+1],'orange')
ax[1, 1].set_title(namelist[x/2],fontsize=10,fontweight='bold')
x=x+2
ax[1,2].plot(list[x],list[x+1],'orange')
ax[1, 2].set_title(namelist[x/2],fontsize=10,fontweight='bold')
x=x+2
ax[1,3].plot(list[x],list[x+1],'orange')
ax[1, 3].set_title(namelist[x/2],fontsize=10,fontweight='bold')

plt.show()
 
 
#Anlik frekans dagilimlari
interval=[]
def float_range(A, L=None, D=None):
    if L == None:
        L = A + 0.0
        A = 0.0
    if D == None:
        D = 1.0
    while True:
        if D > 0 and A >= L:
            break
        elif D < 0 and A <= L:
            break
        yield ("%g" % A)
        A = A + D
            

for i in float_range(1.5, 2.5, 0.05):
    interval.append(float(i))





zeros2={}
for key in frekans:
    zeros2[key]=[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]

for val in range(len(interval)):
    interval[val]=float(interval[val])
        

for key in frekans:
    for item in frekans[key]:
        for val in range(20):
            if item>interval[val] and item<interval[val+1]:
                zeros2[key][val]=zeros2[key][val]+1
                    
list=[]
namelist=[]
for key in frekans:
    list.append(interval)
    list.append(zeros2[key])
    namelist.append(key)





plt.figure(figsize=(15,10))
x=0
plt.subplot(2, 4, 1)
plt.bar(list[x],list[x+1], color='orange', width = 0.25,edgecolor = "none")
plt.title(namelist[x/2],fontsize=10,fontweight='bold')
x=x+2
plt.subplot(2, 4, 2)
plt.bar(list[x],list[x+1], color='orange', width = 0.25,edgecolor = "none")
plt.title(namelist[x/2],fontsize=10,fontweight='bold')
x=x+2
plt.subplot(2, 4, 3)
plt.bar(list[x],list[x+1], color='orange', width = 0.25,edgecolor = "none")
plt.title(namelist[x/2],fontsize=10,fontweight='bold')
x=x+2
plt.subplot(2, 4, 4)
plt.bar(list[x],list[x+1], color='orange', width = 0.25,edgecolor = "none")
plt.title(namelist[x/2],fontsize=10,fontweight='bold')
x=x+2
plt.subplot(2, 4, 5)
plt.bar(list[x],list[x+1], color='orange', width = 0.25,edgecolor = "none")
plt.title(namelist[x/2],fontsize=10,fontweight='bold')
x=x+2
plt.subplot(2, 4, 6)
plt.bar(list[x],list[x+1], color='orange', width = 0.25,edgecolor = "none")
plt.title(namelist[x/2],fontsize=10,fontweight='bold')
x=x+2
plt.subplot(2, 4, 7)
plt.bar(list[x],list[x+1], color='orange', width = 0.25,edgecolor = "none")
plt.title(namelist[x/2],fontsize=10,fontweight='bold')
x=x+2
plt.subplot(2, 4, 8)
plt.bar(list[x],list[x+1], color='orange', width = 0.25,edgecolor = "none")
plt.title(namelist[x/2],fontsize=10,fontweight='bold')


plt.show()








f.close()



 

 

