from email import header
import os
# from util import hashing
import socket
from dotenv import load_dotenv
import random

load_dotenv()
UPLOAD_TYPE = os.getenv('UPLOAD_TYPE')
DOWNLOAD_TYPE = os.getenv('DOWNLOAD_TYPE')
LIST_TYPE = os.getenv('LIST_TYPE')
FIND_POSITION_TYPE = os.getenv('FIND_POSITION_TYPE')
MAIN_DIRECTORY = os.getenv('MAIN_DIRECTORY')
SEND_FILE_CODE = os.getenv('SEND_FILE_CODE')
DOWNLOAD_FILE_CODE = os.getenv('DOWNLOAD_FILE_CODE')
FILE_ALREADY_EXITS_CODE = os.getenv('FILE_ALREADY_EXITS_CODE')
FILE_SAVED = os.getenv('FILE_SAVED')
SEND_TYPE = os.getenv('SEND_TYPE')
GET_UPLOAD_DATA_TYPE = os.getenv('GET_UPLOAD_DATA_TYPE')
SUCCESS_CODE = os.getenv('SUCCESS_CODE')
ASK_NEXT_ONE = os.getenv('ASK_NEXT_ONE')
MAX_RANGE = os.getenv('MAX_RANGE')
# ASK_NEXT_ONE = os.getenv('ASK_NEXT_ONE')
# ASK_NEXT_ONE = os.getenv('ASK_NEXT_ONE')
# ASK_NEXT_ONE = os.getenv('ASK_NEXT_ONE')
# ASK_NEXT_ONE = os.getenv('ASK_NEXT_ONE')
# ASK_NEXT_ONE = os.getenv('ASK_NEXT_ONE')
# ASK_NEXT_ONE = os.getenv('ASK_NEXT_ONE')
# ASK_NEXT_ONE = os.getenv('ASK_NEXT_ONE')

def subscription(myAddres, myID):

    header = {
        "OperationType" : FIND_POSITION_TYPE,
        "Address": myAddres,
        "MyId": myID
    }

    return header

def getPosition(posNode, responsabilityRange): 

    header = {
        "Code": SUCCESS_CODE, 
        "Message": "Already find your position, be ready to get the files.",
        "PosNode": posNode,
        "MaxResponsabilityRange": (responsabilityRange[1][1], responsabilityRange[0][1])
    }

    return header

def askNextOne(posNode): 

    header = {
        "Code": ASK_NEXT_ONE, 
        "Message": "I am not the responsable.",
        "PosNode": posNode
    }

    return header