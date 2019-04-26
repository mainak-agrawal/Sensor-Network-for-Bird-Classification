from python_speech_features import mfcc
import time
import matplotlib.pyplot as plt
import pickle
import serial
import socket
import ast
import numpy
import datetime
import csv
import usingmodel
from os import path
f=open("BirdRecord.txt","a")
#f=open("soundwithbreaks5.txt","w")
HOST = '10.17.50.55'
print(HOST)
PORT = 1234
sock=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect((HOST, PORT))
ser = serial.Serial('/dev/ttyUSB0',230400)
while True:
    s=""
    read_serial=ser.read_until(terminator=b'Location ')
    read_serial=ser.readline()
    xbeeid=(read_serial.decode('cp437'))[0]
    print(xbeeid)
    read_serial=ser.readline()
    s=(read_serial.decode('cp437'))
    #print((s))
    datalist=s.split(',')
    a=[]
    t=-1
    c=0
    prev=0.00
    for i in range(0,len(datalist)):
        try:
            j=int(datalist[i])
            if (j<1001) and (j>-1001):
                a.append(j)
                c=c+1
                if t!=-1:
                    a[t]=(prev+j)/2
            t=-1
            prev=j
        except:
            t=c
#    a=list(ast.literal_eval(s[0:len(s)-1]))
    print(len(a))
    if ((len(a))==0):
        pass
    else:
        plt.plot(a)
        title= "Location "+str(xbeeid)
        plt.title(title)
        plt.show()
#        plt.close('all')
#        f.write(str(a))
        rate=1600
        mfcc_feat = mfcc(numpy.asarray(a),rate,nfft=512)
        m=mfcc_feat.shape
        print(m)
        d={"id":xbeeid,"time":str(datetime.datetime.now()),"mat":mfcc_feat.tolist(),"bird":5}
       # final = pickle.dumps(d)
       # sock.sendall(final)
        filename="new.csv"
        rel_path=filename
        file_path=path.relpath(rel_path)
        with open(file_path,"w") as ff:
               #s2write=(str(d.get('id'))+" "+d.get('time')+" "+d.get('mat')+"\n")
               #f.write(s2write)
            writer=csv.writer(ff)
            writer.writerows(d.get('mat'))
        result=usingmodel.classify(filename)
        print("bird id is "+str(result[0]))
        f.write(d.get('id')+", "+d.get('time')+", "+str(result[0])+"\n")
        d['bird']=str((result.tolist())[0])
        final = pickle.dumps(d)
        sock.sendall(final)
socket.close(sock)
f.close()


