import socket
import csv
import pickle
from os import path
import makemap
HOST = '10.17.50.55'
PORT = 1234
print( HOST)
birdlist = [5,5,5,5,5]
f=open('SoundFile.txt','w')
s= socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
s.bind((HOST, PORT))
print("BINDING DONE")
s.listen(5)
print("LISTENING DONE, NOW ACCEPTING")
(conn,(a,b))  = s.accept()
print('Connected by ',a)
while True:
    print("new 10 sec sound")
    data = conn.recv(4196)
    if not data:
        conn.close()
        print( "NO DATA SO CLOSING CONNECTION")
        break
    else:
      #  print "WRITING DATA INTO FILE"
      #  f.write(data)
      #  a=data[1:len(data)-2]
       # b=a.split(',')
      #  for i in b:
       #     i=int(i)
       # print b
        while True:
            try:
               d=pickle.loads(data)
               print( d.get('id'))
               foldername = "xbee"+str(d.get('id'))
               filename = str(d.get('bird'))+"_"+d.get('time')+'.csv'
               rel_path="dataReceived/"+foldername+'/'+filename
               file_path=path.relpath(rel_path)
               with open(file_path,"w") as ff: 
               #s2write=(str(d.get('id'))+" "+d.get('time')+" "+d.get('mat')+"\n")
               #f.write(s2write)
                   writer=csv.writer(ff)
                   writer.writerows(d.get('mat'))
               print("Successfully written to file")
               birdlist[(int(d.get('id'))-1)]=int(d.get('bird'))
               makemap.make(birdlist)
               break
            except EOFError:
               data= data+conn.recv(4196)            
f.close()
