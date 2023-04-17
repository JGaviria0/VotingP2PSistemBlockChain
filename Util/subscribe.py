import zmq
import json
import os
from Util import header
from dotenv import load_dotenv

load_dotenv()
FIND_POSITION_TYPE = os.getenv('FIND_POSITION_TYPE')
SUCCESS_CODE = os.getenv('SUCCESS_CODE')
MAX_RANGE = int(os.getenv('MAX_RANGE'))

context = zmq.Context()

def findPosition(firtsNode, myAddres, myID):
    FindMyPosition = False
    try:
        while not FindMyPosition:
            socketsub = context.socket(zmq.REQ)
            socketsub.connect(f'tcp://{firtsNode}')

            hs = header.subscription(myAddres, myID)
            headerJSON = json.dumps(hs).encode()
            socketsub.send_multipart([headerJSON, headerJSON])
            res = socketsub.recv_multipart()
            message = json.loads(res[0])
            print(message)

            if message["Code"] == SUCCESS_CODE:
                FindMyPosition = True
                print(message["PreNode"])
                return socketsub, firtsNode, message["PreNode"][0], message["PreNode"][1], message["Message"]
            
            socketsub.close()
            firtsNode = message["PreNode"]

        print("Error, didn't find my position")
    except Exception as e: 
        print(e)
        print("Not possible to connect to the server.")

def isIn(responsabilityRange, value):

    if responsabilityRange[0] == responsabilityRange[1]:
        return True
    
    if responsabilityRange[0] > responsabilityRange[1]:
        if (responsabilityRange[0] < value and value < MAX_RANGE) or (0 <= value and value <= responsabilityRange[1]):
            return True
    
    if responsabilityRange[0] < value and value <= responsabilityRange[1]:
        return True

    return False


def getPosition(socket, responsabilityRange, NextOneID, preNode, posNode, address, myFiles): 
    NextOneID = int(NextOneID)
    print(NextOneID)

    if (isIn(responsabilityRange, NextOneID)): 
        hs = ""
        if NextOneID in myFiles:
            hs = header.fileAlreadyUpload(preNode, responsabilityRange)
        else:
            hs = header.getPosition(preNode, responsabilityRange)
        headerJSON = json.dumps(hs).encode()
        socket.send_multipart([headerJSON, headerJSON])

    else: 
        hs = header.askNextOne(preNode)
        headerJSON = json.dumps(hs).encode()
        socket.send_multipart([headerJSON, headerJSON])
        return -1, -1


