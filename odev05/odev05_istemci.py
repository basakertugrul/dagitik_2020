import sys
import socket


s=socket.socket()



ip_host= str(sys.argv[1])
port= int(sys.argv[2])

s.connect((ip_host, port))


while True:
    data=s.recv(1024)
    print(data)
    datatosend = str(input())
    s.send(datatosend.encode())
    if(datatosend=="Kapan"):
        data=s.recv(1024)
        print(data)
        break
    


s.close()
