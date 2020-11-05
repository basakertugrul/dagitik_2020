import sys
import string

import threading
import time
import multiprocessing
from multiprocessing import Lock, Process, Queue, current_process
import queue


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









done_queue=Queue()
exitFlag = 0

class myThread (threading.Thread):
    def __init__(self, threadID, name, q):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.q = q
    def run(self):
        process_data(self.name, self.q)
       

def process_data(threadName, q):
    while True:
        queueLock.acquire()
        if not q.empty():
            data = q.get()
            done_queue.put(encryption(data))
            queueLock.release()
            if data == "Quit":
                break
        else:
            queueLock.release()
        


threadList=[]
for x in range(n):
    threadList.append("Thread-%d"%(x))


queueLock = threading.Lock()
workQueue = Queue()
threads = []
threadID = 1

# Create new threads
for tName in threadList:
    thread = myThread(threadID, tName, workQueue)
    thread.start()
    threads.append(thread)
    threadID += 1
    
# Fill the queue
queueLock.acquire()
for word in plainList:
    workQueue.put(word)
queueLock.release()
    
# Wait for queue to empty
while not workQueue.empty():
    pass
    
# Notify threads it's time to exit
for tName in threadList:
    workQueue.put("Quit")
    
# Wait for all threads to complete
for t in threads:
    t.join()





lastList=[]
while not done_queue.empty():
    lastList.append(done_queue.get())
    
for x in range(n):
    lastList.pop()


lastString=""

filew = open("crypted_thread_19_10_32.txt", "w")

for item in lastList:
    for x in item:
        lastString=lastString+str(x)

filew.write(lastString)

filew.close()
