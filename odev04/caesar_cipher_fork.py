import sys
import string
import threading
import time
import multiprocessing
from multiprocessing import Lock, Process, Queue, current_process

alphabetString = string.ascii_lowercase
alphabet = list(alphabetString)

s=int(sys.argv[1])
n=int(sys.argv[2])
l=int(sys.argv[3])


def encryption(plainList):
    cryptedList=[]
    for item in plainList:
        temp=""
        for letter in item:
            if letter in alphabet:
                x=alphabet.index(letter)
                x=x+s
                x=x % 26
                temp=temp+alphabet[x]
            else:
                temp=temp+letter
                
        cryptedList.append(temp)
    return cryptedList
    

plainText=""
plainList=[]

cryptedText=""
cryptedList=[]


f = open("input.txt","r")
for i in f:
    plainText=plainText+i
f.close()

plainText=plainText.lower()
plainList=[plainText[i:i+l] for i in range(0, len(plainText), l)]









lock = multiprocessing.Lock()
def worker(work_queue, done_queue,lock):
    try:
        lock.acquire()
        for item in iter(work_queue.get, 'STOP'):
            done_queue.put(encryption(item))
    except Exception, e:
        done_queue.put("FAIL")
    finally:
        lock.release()
    return True


workers = n
work_queue = Queue()
done_queue = Queue()
processes = []


for item in plainList:
    work_queue.put(item)
        

for w in xrange(workers):
    p = Process(target=worker, args=(work_queue, done_queue,lock))
    p.start()
    processes.append(p)
    work_queue.put('STOP')
    
    
for p in processes:
    p.join()
    
done_queue.put('STOP')



lastList=[]
while not done_queue.empty():
    lastList.append(done_queue.get())
    
    
lastList.pop()
lastString=""
for item in lastList:
    for x in item:
        lastString=lastString+str(x)


filew = open("crypted_fork_12_12_8.txt", "w")
filew.write(lastString)

filew.close()
