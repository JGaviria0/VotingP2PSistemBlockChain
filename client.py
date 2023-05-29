from Util import header, broker, subscribe, socketsRepo, votes
import json
import argparse
import zmq
import random
import json
import os
import sys
import hashlib
from dotenv import load_dotenv
import socket as so

#Saquial
import string

load_dotenv()

MAX_RANGE = int(os.getenv('MAX_RANGE'))
SUCCESS_CODE = os.getenv('SUCCESS_CODE')
SUCCESS_CODE_ALREADY_HAVE_FILE = os.getenv('SUCCESS_CODE_ALREADY_HAVE_FILE')

context = zmq.Context()

def getMyIP():  
    s = so.socket(so.AF_INET, so.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    IPAddr = s.getsockname()[0]
    return IPAddr

def upload(fileName, address, firstNode, myAddress): 

    #Test file

    headerJSON = header.uploadFile(fileName, path="")
    hashes = broker.sendFile(headerJSON, address, firstNode)
    hs = header.sendMagnetLink(fileName, headerJSON["Hash"], headerJSON["Size"], hashes)
    magnetLink = json.dumps(hs).encode()
    sha256 = hashlib.sha256()
    sha256.update(magnetLink)
    magnetLinkHash = sha256.hexdigest()
    fileID = int(magnetLinkHash, 16)%MAX_RANGE
    socketsub, _, _, _, _= subscribe.findPosition(firstNode, myAddress, fileID)
    broker.sendChunk(magnetLink, socketsub, headerJSON["Name"], headerJSON["Size"], 0, magnetLinkHash, magnetLink=True)
    print(magnetLink)
    info = f'\n\n The magnetLink for {headerJSON["Name"]} es: \n\n{magnetLinkHash}\n\n'
    print(info)

def download(res, firstNode, myAddress):
    # res = json.loads(res)
    print(res)
    # totalBytes = b"" 
    try: 
        fileFullName, ext = res["Name"].split('.')
    except:
        ext = ""
        fileFullName = res["Name"]
    for parts in res["Parts"]:
        fileName, _ = parts
        print(parts)
        fileID = int(fileName, 16)%MAX_RANGE
        socketsub, _, _, _, _= subscribe.findPosition(firstNode, myAddress, fileID)
        bytes = broker.getFile(socketsub, fileName)
        # totalBytes += 
        file1 = open(f"{fileFullName}2.{ext}", "ab")  # append mode
        file1.write(bytes)
        file1.close()
    
    print("Saving succesfully: ")
    
    # res = socketsRepo.saveFile( f'{fileName}2.{ext}', totalBytes, path="") 
    # print(res)

def getMagnetLink(magnetLink, myAddress, firstNode): 
    try:
        fileID = int(magnetLink, 16)%MAX_RANGE
        socketsub, _, _, _, code = subscribe.findPosition(firstNode, myAddress, fileID)
        if code != SUCCESS_CODE:
            bytes = broker.getFile(socketsub, magnetLink)
            bytesJson = json.loads(bytes)
            res = socketsRepo.saveFile( f'{bytesJson["Name"]}MagnetLink.txt', bytes, path="") 
            print(res)
            return bytesJson
        else: 
            print("Error geting the magnetLink, it does't exist")
            return False

    except Exception as e: 
        print(e)
        print("Error geting download data")


#Saquial
def getVote(vote, candidates, myAddress):
    Name = ''.join(random.choices(string.ascii_lowercase, k=20)) #https://flexiple.com/python/generate-random-string-python/ 
    vote = votes.addVote(vote, Name, myAddress, candidates[random.randint(0, 2)])
    return vote



def main():

    parser = argparse.ArgumentParser(
        description='Example with nonoptional arguments',
    )

    parser.add_argument('-address', action="store", type=str, default="localhost:0000")
    parser.add_argument('--upload', action="store_true", default=False)
    parser.add_argument('--download', action="store_true", default=False)
    parser.add_argument('--vote', action="store_true", default=False) #Saquial
    parser.add_argument('-fileName', action="store", type=str, default="")
    parser.add_argument('-magnetLink', action="store", type=str, default="")
    # parser.add_argument('-magnetFile', action="store", type=str, default="")

    data = parser.parse_args()
    if data.upload and data.fileName == "":
        print("--upload flag, must to specify -fileName")
        return

    if data.download and data.magnetLink == "":
        print("--download flag, must to specify -magnetLink")
        return

    firtsNode = data.address
    fileName = data.fileName
    magnetLink = data.magnetLink

    myAddress = getMyIP()


    if data.upload:
        upload(fileName, myAddress, firtsNode, myAddress)
    
    if data.download:
        res= getMagnetLink(magnetLink, myAddress, firtsNode)
        if res: 
            download(res, firtsNode, myAddress)

    #Saquial
    if data.vote:
        candidates = []
        vote = {}

        i = 0
        while (i < 3):
            candidates.append(''.join(random.choices(string.ascii_lowercase, k=20)))
            i += 1
        
        i = 0
        while (i < 10):
            getVote(vote, candidates, myAddress)
            i += 1

        block = votes.createBlock("", vote)

        print(block)
            



main()