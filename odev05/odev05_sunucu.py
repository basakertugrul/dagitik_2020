import socket
import sys
import threading
import time

class conThread(threading.Thread):

    def __init__(self, threadID,conn,c_addr):
        threading.Thread.__init__(self)
        self.threadID=threadID
        self.conn=conn
        self.c_adrr=c_addr
        
    def run(self):
        self.conn.send(("Saat su an: " + str(time.strftime("%H"))).encode())
        while True:
            data=self.conn.recv(1024)
            data_str=data.decode().strip()
            print(data_str)
            if(data_str=="Selam"):
                self.conn.send(("Selam"+" ").encode())
            elif(data_str=="Naber"):
                self.conn.send(("Iyiyim, sagol"+" ").encode())
            elif(data_str=="Hava"):
                self.conn.send(("Yagmurlu"+" ").encode())
            elif(data_str=="Haber"):
                self.conn.send(("Korona"+" ").encode())
            elif(data_str=="Kapan"):
                self.conn.send(("Gule gule"+" ").encode())
                break
            else:
                self.conn.send("Anlamadim ".encode())
        self.conn.close()
        print("Thread no:" + str(self.threadID) + " kapandi" )





s=socket.socket()
ip= "0.0.0.0"
port= int(sys.argv[1])
addr_server=(ip,port)
s.bind(addr_server)
s.listen(5)




count=0

while True:
    conn, adrr = s.accept()
    newConnThread=conThread(count,conn, adrr)
    count=count+1
    newConnThread.start()


    
s.close()

