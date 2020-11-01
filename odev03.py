import numpy as np
import matplotlib.pyplot as plt




f = open("lab8_3.91-6.11-1.57.mbd","r")


    #firstpart
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
            

for key in map:
    numbers=arrange[key]
    values=zeros[key]
    plt.bar(numbers, values, color ='orange', width = 0.75)
    plt.title(key)
    plt.show()

f.close()




#secondpart

f = open("lab8_3.91-6.11-1.57.mbd","r")
w=100.0

def instFreq (Tt, Ttw):
    f=w/float(float(Ttw)-float(Tt))
    return f

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
for key in frekans:
    for item in frekans[key]:
        item=float(item)
      
for key in frekans:
    xx = range(len(frekans[key]))
    x= xx
    y = frekans[key]
    plt.plot(x, y)
    plt.title(key)
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
                    

for key in frekans:
    numbers=interval
    values=zeros2[key]
    plt.bar(numbers, values, color ='orange', width = 0.05)
    plt.title(key)
    plt.show()


f.close()



 

 

