import zmq
import os
import json
import hashlib
from dotenv import load_dotenv
from Util import header, subscribe

load_dotenv()
NODES_PORT = os.getenv('NODES_PORT')
MAIN_DIRECTORY = os.getenv('MAIN_DIRECTORY')
BUF_SIZE = int(os.getenv('BUF_SIZE'))
MAX_RANGE = int(os.getenv('MAX_RANGE'))
context = zmq.Context()

def sendChunk(bytes, socket, name, size, npart, hashPart, magnetLink=False):

    if not magnetLink: 
        fullFileName = name.split('.')
        fielName = f"{fullFileName[0]}{npart}"
    else: 
        fielName = f"{name}magnetLink"
    hsJSON = header.sendChunkHeader(fielName, hashPart, size)
    headerJSON = json.dumps(hsJSON).encode()

    socket.send_multipart([headerJSON, bytes])
    message = socket.recv()

    print(message.decode(), end="")
    return hashPart

def sendFile(header, address, firtsNode):
    
    fullFileName = header["Name"]
    size = header["Size"]

    cs = (size // BUF_SIZE)+1
    hashes = []

    with open(f'{fullFileName}', 'rb') as inputFile:
        for parts in range(cs):
            hash = hashlib.sha256()
            bytes = inputFile.read(BUF_SIZE)
            hash.update(bytes)
            hashPart = hash.hexdigest()
            IDHashPart = int(hashPart, 16)%MAX_RANGE
            socketsub, addressnode, _, _, ms = subscribe.findPosition(firtsNode, address, IDHashPart)

            if ms == "Already find your position, but I already have that file.":
                print("Continue because the file already in the server.")
            else:
                eachsize = BUF_SIZE
                if parts == cs-1:
                    eachsize = size%(BUF_SIZE)
                    if cs == 0:
                        break
                newhash = sendChunk(bytes, socketsub, header["Name"], eachsize, parts, hashPart)
                
            hashes.append([hashPart, addressnode])

    return hashes

def getFile( socket, fileName):

    hs = header.getFile(fileName)
    headerJSON = json.dumps(hs).encode()

    socket.send_multipart([headerJSON, headerJSON])

    headerJSON, bytes = socket.recv_multipart()

    return bytes
    