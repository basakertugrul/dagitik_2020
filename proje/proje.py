import socket
import sys
import threading
import time
import queue


belediyelershotdown=False
logb=False

def RepresentsInt(s):
    try:
        int(s)
        return True
    except ValueError:
        return False

>>> print RepresentsInt("+123")
True
>>> print RepresentsInt("10.0")
False



#fihrist={"Basak": ["password",kuyruk, ["oda1","oda2"]]}
#odalar={"oda1":[["admin1rumuz","admin2rumuz"],["admin1rumuz","admin2rumuz","Basak","Omer"],["banned1"]]}
fihrist={"BASAK": ["11",False, ["ROOM1"]],"OMER": ["11",False, ["ROOM1"]]}
odalar={"ROOM1":[["BASAK"],["BASAK","OMER"],[]]}
class readThread(threading.Thread):
    def __init__(self, threadID, conn, addr, threadQueue,logQueue):
        threading.Thread.__init__(self)
        self.threadID=threadID
        self.conn=conn
        self.adrr=addr
        self.threadQueue = threadQueue
        self.tanitma=False
        self.nickname=""
        self.is_running = True
        self.logQueue = logQueue


    def run(self):
        while (self.is_running):
            if belediyelershotdown==True:
                break
            data=self.conn.recv(1024)
            data_str=data.decode().strip()
            
            self.incoming_parser(data.decode())
        self.tanitma=False
        if self.nickname in fihrist:
            fihrist[self.nickname][1]=False
            
        sss="Thread no: "+str(self.threadID)+" kapandi."
        self.logQueue.put(sss)
        sss=self.nickname+" cikti."
        self.logQueue.put(sss)
        
        
        
            
    
    def incoming_parser(self, data):
        msg = data.strip().split(" ")
        if msg[0] == "\x00":
            pass
            
            
        elif str(msg[0]) == "RGS" and len(msg)==3:
            if str(msg[1]) in fihrist:
                s="REJ " + str(msg[1])
                self.threadQueue.put(s)
                sss=msg[1]+" adli kullanici kayitli oldugu icin reddedildi."
                self.logQueue.put(sss)
                
            else:
                if RepresentsInt(msg[2]):
                    fihrist[msg[1]]= [msg[2], False, []]
                    s="REG " + str(msg[1])
                    self.threadQueue.put(s)
                    ss="WRN "+ str(msg[1]) + " kayit oldu"
                    for key in fihrist:
                        if fihrist[key][1] !=  False:
                            fihrist[key][1].put(ss)
                    sss=str(msg[1])+" kayit oldu."
                    self.logQueue.put(sss)
                else:
                    self.threadQueue.put("NON ")
                    sss=msg[1]+" adli kullanici sifre sayilardan olusmadigi icin reddedildi."
                    self.logQueue.put(sss)
                    
                
        elif str(msg[0]) == "ENT" and len(msg)==3:
            if str(msg[1]) in fihrist:
                if str(msg[2]) == fihrist[msg[1]][0]:
                    self.nickname = msg[1]
                    self.tanitma=True
                    ss="WRN "+ str(msg[1]) + " online oldu"
                    for key in fihrist:
                        if fihrist[key][1] !=  False:
                            fihrist[key][1].put(ss)
                    sss=str(msg[1]) + " online oldu"
                    self.logQueue.put(sss)
                    fihrist[self.nickname][1] =self.threadQueue
                    s="WEL"
                    self.threadQueue.put(s)
                    #threadqueuenin oldugu yer bos degilse online olmus
                else:
                    s="ERE"
                    self.threadQueue.put(s)
            else:
                s="ERL"
                self.threadQueue.put(s)
             
             
        elif msg[0] == "OPN" and len(msg)==2:
            
            if self.tanitma==True:
                if msg[1] not in odalar:
                    s="OKO"
                    self.threadQueue.put(s)
                    sss=self.nickname+", "+ msg[1] +" adli odayi kurdu."
                    self.logQueue.put(sss)
                    ss = "WRN "
                    ss = ss+sss
                    for key in fihrist:
                    #online olma check edilmesi (Kuyruk yerine false varsa)
                        if key[1] != False:
                            fihrist[key][1].put(ss)
                      
                    odalar[msg[1]] = [[self.nickname],[self.nickname],[]]
                    fihrist[self.nickname][2].append(msg[1])
                else:
                    s="ERO"
                    self.threadQueue.put(s)
                    sss=self.nickname+", zaten varolan "+ msg[1] +" adli odayi kurmak istedi."
                    self.logQueue.put(sss)
                    
            else:
                self.threadQueue.put("LRR")
                sss="Login olunmadan oda kurulmak istendi."
                self.logQueue.put(sss)
                
        elif msg[0] == "CHN" and len(msg)==3:
            
            if self.tanitma==True:
                if msg[1] == fihrist[self.nickname][0]:
                    if RepresentsInt(msg[2]):
                    #sayi check etme
                        s="OKC"
                        self.threadQueue.put(s)
                        sss=self.username + " sifre degistirdi."
                        self.logQueue.put(sss)
                        fihrist[self.nickname][0] = msg[2]
                    else:
                        self.threadQueue.put("NON")
                        sss= self.username + " sifre degistirmek istedi ama yeni sifre sayilardan olusmuyor."
                        self.logQueue.put(sss)
                else:
                    self.threadQueue.put("NOP")
                    sss= self.username + " sifre degistirmek istedi ama eski sifresini yanlis girdi."
                    self.logQueue.put(sss)
                    
            else:
                self.threadQueue.put("LRR")
                sss="Login olunmadan sifre degistirilmesi istendi."
                self.logQueue.put(sss)
        
        
        elif msg[0] == "LSR" and len(msg)==1:
            if self.tanitma==True:
                s="OKL "
                k=False
                for key in odalar:
                    if k==False:
                        s=s+key
                    else:
                        s=s+": " + key
                    k=True
                self.threadQueue.put(s)
            else:
                self.threadQueue.put("LRR")
                sss="Login olunmadan odalar listelensin istendi."
                self.logQueue.put(sss)
         
        
        elif msg[0] == "ENR" and len(msg)==2:
            if self.tanitma==True:
                if msg[1] in odalar:
                    if self.nickname not in odalar[msg[1]][2]:
                        if self.nickname not in odalar[msg[1]][1]:
                            sss= self.nickname + " " + msg[1] +" adli odaya girdi"
                            self.logQueue.put(sss)
                            self.threadQueue.put("WER ")
                            odalar[msg[1]][1].append(self.nickname)
                            fihrist[self.nickname][2].append(msg[1])
                            sss= "WRN " + self.nickname + ", odaya girdi"
                            for item in odalar[msg[1]][1]:
                                fihrist[item][1].put(sss)
                        else:
                            #Kurucu admin direkt odaya uye olmus sayiliyor zaten:
                            sss= self.nickname + " zaten icinde oldugu " + msg[1] +" adli odaya girmek istedi"
                            self.logQueue.put(sss)
                            self.threadQueue.put("ERR")
                    else:
                        sss= self.nickname + " banlandigi " + msg[1] +" adli odaya girmek istedi"
                        self.logQueue.put(sss)
                        sss = "WRN " + sss
                        for item in odalar[msg[1]][0]:
                            item.put(sss)
                        #Banli oldugu yere girmek isterse biri, adminlere gidiyor
                        self.threadQueue.put("BAN")
                else:
                    sss= self.nickname + ", olmayan " + msg[1] +" adli odaya girmek istedi"
                    self.logQueue.put(sss)
                    self.threadQueue.put("WNM")
         
            else:
                self.threadQueue.put("LRR")
                sss="Login olunmadan "+ msg[1]+" adli odaya girilmek istendi."
                self.logQueue.put(sss)
         
        
        elif msg[0] == "LSR" and len(msg)==2:
            if self.tanitma==True:
                if str(msg[1]) in odalar:
                    if self.nickname in odalar[msg[1]][1]:
                        s="OKL "
                        k=False
                        for key in odalar[msg[1]][1]:
                            if k==False:
                                s=s+key
                            else:
                                s=s+": " + key
                            k=True
                        self.threadQueue.put(s)
                    else:
                        self.threadQueue.put("ERL")
                        sss=self.nickname + " icinde olmadigi " + msg[1] + " adli odadaki insanlar listelensin istendi."
                        self.logQueue.put(sss)
                else:
                    self.threadQueue.put("WRN")
                    sss=self.nickname + " var olmayan " + msg[1] + " adli odadaki insanlar listelensin istendi."
                    self.logQueue.put(sss)
            else:
                self.threadQueue.put("LRR")
                sss="Login olunmadan " + msg[1] + " adli odadaki insanlar listelensin istendi."
                self.logQueue.put(sss)
        
        
        elif str(msg[0]) == "QUI" and len(msg)==2:
            if self.tanitma==True:
                if msg[1] in odalar:
                    if self.nickname not in odalar[msg[1]][0]:
                        s="BYE from " + msg[1]
                        self.threadQueue.put(s)
                        fihrist[self.nickname][2].remove(msg[1])
                        odalar[msg[1]][1].remove(self.nickname)
                        sss=self.nickname+", " + msg[1] + " adli odadan cikti."
                        self.logQueue.put(sss)
                    elif self.nickname in odalar[msg[1]][0] and len(odalar[msg[1]][0]) != 1:
                        s="BYE from " + msg[1]
                        self.threadQueue.put(s)
                        fihrist[self.nickname][2].remove(msg[1])
                        odalar[msg[1]][1].remove(msg[self.nickname])
                        odalar[msg[1]][0].remove(msg[self.nickname])
                        sss=self.nickname+", " + msg[1] + " adli odadan cikti."
                        self.logQueue.put(sss)
                    elif self.nickname in odalar[msg[1]][0] and len(odalar[msg[1]][0]) == 1:
                        self.threadQueue.put("LAY")
                        sss=self.nickname+", " + msg[1] + " adli odadan cikamadi cunku tek admin."
                        self.logQueue.put(sss)
                    else:
                        self.threadQueue.put("WRO")
                        sss=self.nickname+", " + msg[1] + " adli odadan cikamadi cunku odaya kayitli degil."
                        self.logQueue.put(sss)
                else:
                    self.threadQueue.put("WRR")
                    sss=self.nickname+", " + msg[1] + " adli odadan cikamadi cunku oda ismi yanlis."
                    self.logQueue.put(sss)
                        
            else:
                self.threadQueue.put("LRR")
                sss="Login olunmadan " + msg[1] + " adli odadan cikilmak istendi."
                self.logQueue.put(sss)
        
        elif str(msg[0]) == "LSM" and len(msg)==1:
            if self.tanitma==True:
                s="OKL "
                k=False
                for item in fihrist[self.nickname][2]:
                    if k==False:
                        s=s+item
                    else:
                        s=s+": " + item
                    k=True
                self.threadQueue.put(s)
            else:
                self.threadQueue.put("LRR")
                sss="Login olunmadan icinde bulundugu odalar listelensin istenildi."
                self.logQueue.put(sss)
        
        
        elif str(msg[0]) == "KIC" and len(msg)==3:
            room=msg[1]
            person=msg[2]
            if self.tanitma==True:
                if room in odalar:
                    if self.nickname in odalar[room][0]:
                        if person in odalar[room][1]:
                            odalar[room][1].remove(person)
                            fihrist[person][2].remove(room)
                            self.threadQueue.put("OKK")
                            sss=self.nickname + ", " + person +" adli kullanici " + room +" adli odadan atti."
                            self.logQueue.put(sss)
                            sss="WRN " + self.nickname +" adli kullanici " + room +" adli odadan sizi atti."
                            if fihrist[person][1] != False:
                                fihrist[person][1].put(sss)
                        else:
                            self.threadQueue.put("WPN")
                            sss=self.nickname + ", " + person +" adli odada olmayan kullanici " + room +" adli odadan atmak istedi."
                            self.logQueue.put(sss)
                        
                    else:
                        self.threadQueue.put("WNA")
                        sss=self.nickname + ", " + person +" adli kullanici " + room +" adli admini olmadigi odadan atmak istedi."
                        self.logQueue.put(sss)
                    
                else:
                    self.threadQueue.put("WNM")
                    sss=self.nickname + ", " + person +" adli kullanici " + room +" adli olmayan odadan atmak istedi."
                    self.logQueue.put(sss)
            else:
                self.threadQueue.put("LRR")
                sss="Login olunmadan," + person +" adli kullanici " + room +" adli odadan atilmak istenildi."
                self.logQueue.put(sss)
        
        
        elif msg[0] == "DEL" and len(msg)==2:
            room=msg[1]
            if self.tanitma==True:
                if room in odalar:
                    if self.nickname in odalar[room][0]:
                        sss= "WRN " + room + " adli oda " + self.nickname+ " tarafindan kapatildi."
                        for item in odalar[room][1]:
                            fihrist[item][1].put(sss)
                        del odalar[room]
                        for key in fihrist:
                            if room in key[2]:
                                key[2].remove(room)
                                
                        self.threadQueue.put("OKD")
                        sss=self.nickname + ", " + room + " adli odayı sildi."
                        self.logQueue.put(sss)
                    else:
                        self.threadQueue.put("WRN")
                        sss=self.nickname + ", " + room + " adli admini olmadigi odayı silmek istedi."
                        self.logQueue.put(sss)
                else:
                    self.threadQueue.put("WNM")
                    sss=self.nickname + ", " + room + " adli olmayan odayı silmek istedi."
                    self.logQueue.put(sss)
            else:
                self.threadQueue.put("LRR")
                sss="Login olunmadan " + room + " adli oda silinsin istenildi."
                self.logQueue.put(sss)
        
        
        
        elif str(msg[0]) == "BAN" and len(msg)==3:
            room=msg[1]
            person=msg[2]
            if self.tanitma==True:
                if room in odalar:
                    if self.nickname in odalar[room][0]:
                        if person in odalar[room][1]:
                            self.threadQueue.put("OKK")
                            sss=self.nickname + ", " + person +" adli kullaniciyi " + room +" adli odadan banladi."
                            self.logQueue.put(sss)
                            sss="WRN " + self.nickname +" adli kullanici " + room +" adli odadan sizi banladi."
                            if fihrist[person][1] != False:
                                fihrist[person][1].put(sss)
                            odalar[room][2].append(person)
                        else:
                            self.threadQueue.put("WPN")
                            sss=self.nickname + ", " + person +" adli odada olmayan kullaniciyi " + room +" adli odadan banlamak istedi."
                            self.logQueue.put(sss)
                        
                    else:
                        self.threadQueue.put("WNA")
                        sss=self.nickname + ", " + person +" adli kullaniciyi " + room +" adli admini olmadigi odadan banlamak istedi."
                        self.logQueue.put(sss)
                    
                else:
                    self.threadQueue.put("WNM")
                    sss=self.nickname + ", " + person +" adli kullaniciyi " + room +" adli olmayan odadan banlamak istedi."
                    self.logQueue.put(sss)
            else:
                self.threadQueue.put("LRR")
                sss="Login olunmadan," + person +" adli kullanici " + room +" adli odadan banlanilmak istendi."
                self.logQueue.put(sss)
        
        
        elif str(msg[0]) == "YON" and len(msg)==3:
            room=msg[1]
            person=msg[2]
            if self.tanitma==True:
                if room in odalar:
                    if self.nickname in odalar[room][0]:
                        if person in odalar[room][0]:
                            #odada olmayan biri de admin yapilabiliniyor, direkt uye de oluyor
                            self.threadQueue.put("OKK")
                            sss=self.nickname + ", " + person +" adli kullaniciyi " + room +" adli odaya admin yapti."
                            self.logQueue.put(sss)
                            sss="WRN " + self.nickname +" adli kullanici " + room +" adli odaya sizi admin yapti."
                            if fihrist[person][1] != False:
                                fihrist[person][1].put(sss)
                            odalar[room][0].append(person)
                            fihrist[person][2].append(room)
                            
                        else:
                            self.threadQueue.put("WPA")
                            sss=self.nickname + ", " + room +" adli odaya admin yapmak istedi."
                            self.logQueue.put(sss)
                        
                    else:
                        self.threadQueue.put("WNA")
                        sss=self.nickname + ", " + person +" adli kullaniciyi " + room +" adli admini olmadigi odaya admin yapmak istedi."
                        self.logQueue.put(sss)
                    
                else:
                    self.threadQueue.put("WNM")
                    sss=self.nickname + ", " + person +" adli kullaniciyi " + room +" adli olmayan odaya admin yapmak istedi."
                    self.logQueue.put(sss)
            else:
                self.threadQueue.put("LRR")
                sss="Login olunmadan," + person +" adli kullaniciyi " + room +" adli odaya admin yaptirmak istendi."
                self.logQueue.put(sss)
        
        
        elif str(msg[0]) == "PIN" and len(msg)==1:
            self.threadQueue.put("PON")
        
        
        elif str(msg[0]) == "QUI" and len(msg)==1:
            s="BYE "+self.nickname
            self.threadQueue.put(s)
            self.is_running=False
            
        elif str(msg[0]) == "OKP" and len(msg)==1:
            pass
        elif str(msg[0]) == "OKW" and len(msg)==1:
            pass
        elif str(msg[0]) == "TON" and len(msg)==1:
            pass
        elif str(msg[0]) == "OKG" and len(msg)==1:
            pass
            
            
        elif str(msg[0]) == "GNL" and len(msg) >= 2 and ":" in msg[1]:
            m=[]
            m= str(msg[1]).strip().split(":")
            room = m[0]
            mesaj = m[1] + " "
            for i in range (2,len(msg)):
                mesaj = mesaj + msg[i] + " "
        
            if self.tanitma==True:
                if room in odalar:
                    if self.nickname not in odalar[room][2]:
                        self.threadQueue.put("OKG")
                        
                        mm="GNL "+self.nickname+": "+ room + ": " + mesaj
                        for item in odalar[room][1]:
                            if fihrist[item][1] != False:
                            #online olma durumu check
                                fihrist[item][1].put(mm)
                            
                        sss=self.nickname+ " " + room +" adli odaya, " + mesaj +"genel mesajini gonderdi."
                        self.logQueue.put(sss)
                
                    else:
                        self.threadQueue.put("WER")
                        sss=self.nickname + ", " + room +" adli odaya, " + mesaj +" genel mesajini gonderemedi cunku odaya kayitli degil."
                        self.logQueue.put(sss)
                else:
                    self.threadQueue.put("WNM")
                    sss=self.nickname + ", " + room +" adli olmayan odaya, " + mesaj +" genel mesajini gondermek istedi."
                    self.logQueue.put(sss)
            else:
                    self.threadQueue.put("LRR")
                    sss="Kendini tanitmayan biri " + room +" adli odaya genel mesaj gondermek istedi."
                    self.logQueue.put(sss)
        
                
        elif str(msg[0]) == "PRV" and len(msg) >= 2 and ":" in msg[1]:
                if self.tanitma==True:
                    messg=[]
                    messg= str(msg[1]).strip().split(":")
                    s= str(messg[1]+" ")
                    for i in range (2,len(msg)):
                        s=s+ str(msg[i])+" "
                 
                    mm="PRV "+self.nickname+": "+s
                    if messg[0] in fihrist:
                        if fihrist[messg[0]][1] != False:
                            #online olma durumu check
                            fihrist[messg[0]][1].put(mm)
                            sss=self.nickname + ", "+ messg[0]+ " adli kullaniciya" + s +" ozel mesajini gonderdi."
                            self.logQueue.put(sss)
                            self.threadQueue.put("OKP")
                        else:
                            st="WRW "
                            self.threadQueue.put(st)
                            sss=self.nickname + " "+ messg[0]+ " adli online olmayan kullaniciya ozel mesaj gondermek istedi."
                            self.logQueue.put(sss)
                        
                    else:
                        st="WWW "
                        self.threadQueue.put(st)
                        sss=self.nickname + " "+ messg[0]+ " adli bulunamayan kullaniciya ozel mesaj gondermek istedi."
                        self.logQueue.put(sss)
                else:
                    self.threadQueue.put("LRR")
                    sss="Kendini tanitmayan biri ozel mesaj gondermek istedi."
                    self.logQueue.put(sss)
        
        
        else:
            self.threadQueue.put("WTF")
  

class writeThread(threading.Thread):
    def __init__(self, threadID,conn,addr, threadQueue,logQueue):
        threading.Thread.__init__(self)
        self.threadID=threadID
        self.conn=conn
        self.adrr=addr
        self.threadQueue = threadQueue
        self.running = True
        self.logQueue=logQueue
        
    def run(self):
        while True:
            data = self.threadQueue.get()
            #msg=data.split(' ')
            if data[0] == "BYE":
                self.conn.send(str(data).encode())
                break
            else:
                self.conn.send(data.encode())
            if belediyelershotdown==True:
                break
        
        sss="Thread no: "+str(self.threadID)+" kapandi."
        self.logQueue.put(sss)
        self.conn.close()


class loggerThread(threading.Thread):
    def __init__(self,logQueue):
        threading.Thread.__init__(self)
        self.logQueue = logQueue
        
    def run(self):
       
        while True:
            f = open('logf.txt', 'a+')
            data = self.logQueue.get()
            s="- "+ " Tarih: " + str(time.asctime( time.localtime(time.time()) )) +"   "+ str(data) +  '\n'
            f.write(s)
            f.close()
            if logb==True:
                break
        
            
            


s=socket.socket()
ip="0.0.0.0"
port=int(sys.argv[1])
addr=(ip,port)
s.bind(addr)
s.listen(5)
    

logQueue=queue.Queue()
    
newloggerThread=loggerThread(logQueue)
newloggerThread.start()
    
threads=[newloggerThread]
    

        

count=1
dongu=True
while dongu:
    try:
        threadQueue=queue.Queue()
        conn, adrr = s.accept()
        newwriteThread=writeThread(count, conn, addr,threadQueue,logQueue)
        count=count+1
        sss="Thread no: "+str(count)+" acildi."
        logQueue.put(sss)
        newreadThread=readThread(count, conn, addr,threadQueue,logQueue)
        count=count+1
        sss="Thread no: "+str(count)+" acildi."
        logQueue.put(sss)
        newwriteThread.start()
        newreadThread.start()
        threads.append(newwriteThread)
        threads.append(newreadThread)
        
    except KeyboardInterrupt:
        belediyelershotdown=True
        dongu=False

newwriteThread.join()
newreadThread.join()
s.close()
logb=True
        
