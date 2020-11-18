import socket
import sys
import threading
import random

def RepresentsInt(s):
    try:
        int(s)
        return True
    except ValueError:
        return False


class conThread(threading.Thread):

    def __init__(self, threadID,conn,c_addr):
        threading.Thread.__init__(self)
        self.threadID=threadID
        self.conn=conn
        self.c_adrr=c_addr
        
    def run(self):
        self.conn.send("Sayi bulmaca oyununa hosgeldiniz!".encode())
        game=False
        self.conn.send("10 adet bilme hakkiniz var!".encode())
        hak=0
        while True:
            splitted=[]
            data=self.conn.recv(1024)
            data_str=data.decode()
            
            splitted=data_str.strip().split(" ")
            komut=splitted[0]
            
            if len(splitted)==2:
                parametre=splitted[1]
            
            if komut=="STA":
                game=True
                number=random.randint(1,99)
                self.conn.send("RDY".encode())
            
            elif komut=="TIC":
                self.conn.send("TOC".encode())
            
            elif komut =="QUI":
                self.conn.send("BYE".encode())
                break
            
            elif game==False and komut=="TRY":
                self.conn.send("GRR".encode())
            
            
            elif game==True and komut=="TRY":
                if RepresentsInt(parametre):
                    guess = int(parametre)
                    hak=hak+1
                    if(guess<number):
                        self.conn.send(("Oyundaki tahmin sayiniz:"+ str(hak) + " " + "LTH").encode())
                        if hak==10:
                            game=False
                            self.conn.send(("Oyunu kaybettiniz").encode())
                            hak=0
                    if(guess>number):
                        self.conn.send(("Oyundaki tahmin sayiniz:"+ str(hak) + " " + "GTH").encode())
                        if hak==10:
                            game=False
                            self.conn.send(("Oyunu kaybettiniz").encode())
                            hak=0
                    if(guess==number):
                        self.conn.send(("Oyundaki tahmin sayiniz:"+ str(hak) + " " + "WIN").encode())
                        game==False
                        hak=0
                            
                        
                        
                else:
                    self.conn.send("PRR".encode())
                
            else:
                self.conn.send("ERR".encode())
                
                
                
                
                
                
                
        self.conn.close()
        print("Thread no:" + str(self.threadID) + " kapaniyor \n" )



s=socket.socket()

ip= "0.0.0.0"
port= int(sys.argv[1])
addr_server=(ip,port)
 

s.bind(addr_server)


s.listen(5)

count=0
threads=[]

while True:
    conn, adrr = s.accept()

    newConnThread=conThread(count,conn, adrr)
    count=count+1
    threads.append(newConnThread)
    newConnThread.start()

print(threads)

    
s.close()

#Bonuslarin ikisini de yaptim
