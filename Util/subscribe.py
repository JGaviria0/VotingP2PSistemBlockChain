from matplotlib.font_manager import json_load
import zmq
import json
import os
from Util import header
from dotenv import load_dotenv

load_dotenv()
FIND_POSITION_TYPE = os.getenv('FIND_POSITION_TYPE')
SUCCESS_CODE = os.getenv('SUCCESS_CODE')

context = zmq.Context()

def responsabilityRangeFix(responsabilityRange, NextOneID):
    if (responsabilityRange[0][0] <= NextOneID and NextOneID <= responsabilityRange[0][1]):
        return ((responsabilityRange[0][0], NextOneID), (-1,-1))
    
    if (responsabilityRange[1][0] <= NextOneID and NextOneID < responsabilityRange[1][1]):
        return ( responsabilityRange[0], (responsabilityRange[1][0], NextOneID))



def findPosition(firtsNode, myAddres, myID):
    FindMyPosition = False
    try:
        while not FindMyPosition:
            socketsub = context.socket(zmq.REQ)
            socketsub.connect(f'tcp://{firtsNode}')

            hs = header.subscription(myAddres, myID)
            headerJSON = json.dumps(hs).encode()
            socketsub.send_multipart([headerJSON, headerJSON])
            
            message = json.loads(socketsub.recv())
            print(message)

            if message["Code"] == SUCCESS_CODE:
                FindMyPosition = True
                lastRange = message["MaxResponsabilityRange"]
                return socketsub, firtsNode, message["PosNode"], lastRange
            
            socketsub.close()
            firtsNode = message["PosNode"]

        print("Error, didn't find my position")
    except Exception as e: 
        print(e)
        print("Not possible to connect to the server.")

def getPosition(socket, responsabilityRange, NextOneID, posNode): 
    NextOneID = int(NextOneID)
    print(NextOneID)

    if (responsabilityRange[0][0] <= NextOneID and NextOneID <= responsabilityRange[0][1]) or (responsabilityRange[1][0] <= NextOneID and NextOneID < responsabilityRange[1][1]): 
        hs = header.getPosition(posNode, responsabilityRange)
        headerJSON = json.dumps(hs).encode()
        socket.send_multipart([headerJSON, headerJSON])
        responsabilityRange = responsabilityRangeFix(responsabilityRange, NextOneID)
        return NextOneID, responsabilityRange

    else: 
        hs = header.askNextOne(posNode)
        headerJSON = json.dumps(hs).encode()
        socket.send_multipart([headerJSON, headerJSON])


