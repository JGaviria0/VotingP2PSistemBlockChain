import os
from dotenv import load_dotenv

load_dotenv()
MAIN_DIRECTORY = os.getenv('MAIN_DIRECTORY')

def sendFile(socket, fileName, header, path=MAIN_DIRECTORY, dirNode=""):
    try:
        print(f"{dirNode}{fileName}")
        f = open(f"{dirNode}{fileName}" ,'rb')
        bytes = f.read()
        socket.send_multipart([header, bytes])
    except Exception as e: 
        print(e)
        print("Error sending the file.")

def saveFile(fileName, binaryFile, path=MAIN_DIRECTORY, dirNode=""):
    # try:
        print(f"{dirNode}{fileName}")
        f = open(f"{dirNode}{fileName}", 'wb')
        f.write(binaryFile)
        f.close()
        return "Saving succesfully: "
    # except Exception as e: 
    #     print(e)
    #     print("Error saving file.")
    #     return ": Error saving the file."
