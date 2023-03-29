import zmq
import random
import json
import os
import sys
from dotenv import load_dotenv
import socket
import argparse

load_dotenv()
PRINCIPAL_PATH = os.getenv('PRINCIPAL_PATH')
UPLOAD_TYPE = os.getenv('UPLOAD_TYPE')
DOWNLOAD_TYPE = os.getenv('DOWNLOAD_TYPE')
SUCCESS_CODE = os.getenv('SUCCESS_CODE')
MAX_RANGE = int(os.getenv('MAX_RANGE'))
FIND_POSITION_TYPE = os.getenv('FIND_POSITION_TYPE')

sys.path.insert(0, PRINCIPAL_PATH)
from Util import header, subscribe
context = zmq.Context()
preNode = ""
posNode = ""
responsabilityRange = ((0, MAX_RANGE), (0, 0))

def getMyIP():  
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    IPAddr = s.getsockname()[0]
    return IPAddr

def getMyID(): 
    return random.randint(0, MAX_RANGE)

def getPosition(socket,responsability, id, postNode):
    global preNode, posNode, responsabilityRange
    posNode, responsabilityRange = subscribe.getPosition(socket,responsability, id, postNode)

def main():
    global preNode, posNode, responsabilityRange

    parser = argparse.ArgumentParser(
        description='Example with nonoptional arguments',
    )

    parser.add_argument('-address', action="store", type=str, default="localhost:0000")
    parser.add_argument('-port', action="store", type=str)
    parser.add_argument('--firstNode', action="store_true", default=False)
    data = parser.parse_args()
    portra = data.port
    socket = context.socket(zmq.REP)
    socket.bind(f"tcp://*:{portra}")
    myAddress = f"{getMyIP()}:{portra}"


    firtsNode = f"{data.address}" if not data.firstNode else myAddress
    print("FirstNode-> ", firtsNode)
    print("My Address-> ", myAddress)
    preNode = myAddress
    preNodeSocket = 0
    posNode = myAddress
    myID = getMyID()
    responsabilityRange = ((myID, MAX_RANGE), (0, myID))
    
    if not data.firstNode: 
        preNodeSocket, preNode, posNode, maxRange= subscribe.findPosition(firtsNode, myAddress, myID)
        if max(maxRange[0], maxRange[1]) == MAX_RANGE: 
            responsabilityRange = ((myID, MAX_RANGE),(0,maxRange[1])) 
        else:
            responsabilityRange = ((myID, maxRange[0]),(-1,-1))

        # posNode = linkage(preNode, portra)
    
    while True: 
        print(myAddress, myID, preNode, posNode, responsabilityRange)
        headerJSON, binaryFile = socket.recv_multipart()
        heade = json.loads(headerJSON)
        print(heade)

        menu = {
            FIND_POSITION_TYPE: getPosition(socket,responsabilityRange, heade["MyId"], posNode)
        }


        menu[heade["OperationType"]]


        
        


main()