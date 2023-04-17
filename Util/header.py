from email import header
import os
from Util import hashing
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
CONFIRM_SUSCRIPTION = os.getenv('CONFIRM_SUSCRIPTION')
ALL_GOOD = os.getenv('ALL_GOOD')
GET_UPLOAD_DATA_TYPE = os.getenv('GET_UPLOAD_DATA_TYPE')
MAGNET_LINK = os.getenv('MAGNET_LINK')
# ASK_NEXT_ONE = os.getenv('ASK_NEXT_ONE')
# ASK_NEXT_ONE = os.getenv('ASK_NEXT_ONE')
# ASK_NEXT_ONE = os.getenv('ASK_NEXT_ONE')

def createHeader( fileName, operationType, hash="", path=MAIN_DIRECTORY, dirnode="" ):
    fileSize = os.path.getsize(f"{dirnode}{fileName}")
    if hash == "":
        hash = hashing.hashfile(fileName, dirnode)

    #https://www.c-sharpcorner.com/blogs/how-to-find-ip-address-in-python
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    IPAddr = s.getsockname()[0]
    
    try:
        _, ext = fileName.split('.') 
    except:
        ext = ""
    header = {
        "OperationType": operationType,
        "Name": fileName,
        "Size": fileSize,
        "Hash": hash,
        "Source": IPAddr,
        "Ext": ext
    }

    return header

def getFile(fileName):

    header = {
        "OperationType" : DOWNLOAD_TYPE,
        "Name": fileName
    }

    return header

def sendChunkHeader(name, hash, size):

    header = {
        "OperationType": SEND_TYPE,
        "Name": name,
        "Size": size,
        "Hash": hash
    }

    return header

def sendMagnetLink(name, hash, size, parts):

    header = {
        "OperationType": MAGNET_LINK,
        "Name": name,
        "Size": size,
        "Hash": hash,
        "Parts": parts
    }

    return header

def subscription(myAddres, myID):

    header = {
        "OperationType" : FIND_POSITION_TYPE,
        "Address": myAddres,
        "MyId": myID
    }

    return header

def confirmSubscription(myAddres, myID):

    header = {
        "OperationType" : CONFIRM_SUSCRIPTION,
        "Address": myAddres,
        "MyId": myID
    }

    return header

def getPosition(preNode, responsabilityRange): 

    header = {
        "Code": SUCCESS_CODE, 
        "Message": "Already find your position, be ready to get the files.",
        "PreNode": (preNode, responsabilityRange[0])
    }

    return header

def fileAlreadyUpload(preNode, responsabilityRange):
    header = {
        "Code": SUCCESS_CODE, 
        "Message": "Already find your position, but I already have that file.",
        "PreNode": (preNode, responsabilityRange[0])
    }

    return header

def askNextOne(preNode): 

    header = {
        "Code": ASK_NEXT_ONE, 
        "Message": "I am not the responsable.",
        "PreNode": preNode
    }

    return header

def checkAllGood(): 

    header = {
        "Code": ALL_GOOD, 
        "Message": "Ok, all good, I will change my range responsability"
    }

    return header

def uploadFile( fileName, path=MAIN_DIRECTORY ):
    
    fileSize = os.path.getsize(f"{path}{fileName}")
    hash = hashing.hashfile(fileName, path)

    header = {
        "OperationType": GET_UPLOAD_DATA_TYPE,
        "Name": fileName,
        "Size": fileSize,
        "Hash": hash
    }

    return header