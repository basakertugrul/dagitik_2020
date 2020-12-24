import socket
import sys
import threading
import time
import queue


fihrist={}
belediyelershotdown=False
logb=False

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
        if self.nickname in fihrist.keys():
            del fihrist[self.nickname]
        sss="Thread no: "+str(self.threadID)+" kapandi."
        self.logQueue.put(sss)
        sss=self.nickname+" cikti."
        self.logQueue.put(sss)
            
    
    def incoming_parser(self, data):
        msg = data.strip().split(" ")
        if msg[0] == "\x00":
            pass
            
            
        elif str(msg[0]) == "NIC":
            if str(msg[1]) in fihrist:
                s="REJ " + str(msg[1])
                self.threadQueue.put(s)
                sss=msg[1]+" adi kullanilmakta oldugu icin reddedildi."
                self.logQueue.put(sss)
                
            else:
                s="WEL " + str(msg[1])
                self.nickname= msg[1]
                fihrist[str(str(msg[1]))] = self.threadQueue
                self.tanitma=True
                ss="WRN "+ self.nickname + " geldi"
                for key in fihrist:
                    fihrist[key].put(ss)
                sss=msg[1]+" adi alindi."
                self.logQueue.put(sss)
                
                
        elif str(msg[0]) == "QUI":
            s="BYE "+self.nickname
            self.threadQueue.put(s)
            self.is_running=False
            
            
            
           
        elif msg[0] == "GLS":
            if self.tanitma==True:
                s=list(fihrist.keys())[0]
                for i in range (1,len(fihrist)):
                    s=s+":" +list(fihrist.keys())[i]
                self.threadQueue.put(s)
                sss=self.nickname+" isimleri listeledi."
                self.logQueue.put(sss)
            else:
                self.threadQueue.put("LRR")
                sss="Kendini tanitmayan biri isimleri listelemek istedi."
                self.logQueue.put(sss)
            
            
        elif str(msg[0]) == "PIN":
            self.threadQueue.put("PON")
            
            
        elif str(msg[0]) == "GNL":
            if ":" not in msg[1]:
                if self.tanitma==True:
                    self.threadQueue.put("OKG")
                    s=""
                    for i in range (1,len(msg)):
                        s=s+str(msg[i])+" "
                
                    mm="GNL "+self.nickname+":"+s
                    for key in fihrist:
                        fihrist[key].put(mm)
                    sss=self.nickname+ " " + s +"genel mesajini gonderdi."
                    self.logQueue.put(sss)
                else:
                    self.threadQueue.put("LRR")
                    sss="Kendini tanitmayan biri genel mesaj gondermek istedi."
                    self.logQueue.put(sss)
            else:
                self.threadQueue.put("msg")
        
        
        
      
        elif str(msg[0]) == "PRV":
            if self.nickname not in msg[1]:
                if self.tanitma==True:
                    messg=[]
                    messg= str(msg[1]).strip().split(":")
                    s= str(messg[1]+" ")
                    for i in range (2,len(msg)):
                        s=s+ str(msg[i])+" "
                 
                    mm="PRV "+self.nickname+":"+s
                    if messg[0] in fihrist.keys():
                        fihrist[str(messg[0])].put(mm)
                        sss=self.nickname + ", "+ messg[0]+ " adli kullaniciya" + s +" ozel mesajini gonderdi."
                        self.logQueue.put(sss)
                        self.threadQueue.put("OKP")
                    
                    else:
                        st="NOP "+ messg[0]
                        self.threadQueue.put(st)
                        sss=self.nickname + " "+ messg[0]+ " adli bulunamayan kullaniciya ozel mesaj gondermek istedi."
                        self.logQueue.put(sss)
                else:
                    self.threadQueue.put("LRR")
                    sss="Kendini tanitmayan biri ozel mesaj gondermek istedi."
                    self.logQueue.put(sss)
                    
                    
            if self.nickname in msg[1]:
                self.threadQueue.put(msg)
        
        
        
        elif str(msg[0]) == "OKP":
            pass
            
        
        elif str(msg[0]) == "OKW":
            pass
  
  
        elif str(msg[0]) == "TON":
            pass
  
  
        elif str(msg[0]) == "OKG":
            pass
  
  
        else:
            self.threadQueue.put("ERR")
        
        
        
  
  
  
  

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
            s="- "+ " Tarih: " + str(time.asctime( time.localtime(time.time()) )) +" "+ str(data) +  '\n'
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


s.close()
logb=True
        

