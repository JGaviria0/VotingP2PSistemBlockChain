import os
from dotenv import load_dotenv

load_dotenv()
MAIN_DIRECTORY = os.getenv('MAIN_DIRECTORY')

def sendFile(socket, fileName, header, path=MAIN_DIRECTORY):
    try:
        print(f"{path}{fileName}")
        f = open(f"{path}{fileName}" ,'rb')
        bytes = f.read()
        socket.send_multipart([header, bytes])
    except Exception as e: 
        print(e)
        print("Error sending the file.")

def saveFile(fileName, binaryFile, path=MAIN_DIRECTORY):
    # try:
        f = open(f"{path}{fileName}", 'wb')
        f.write(binaryFile)
        f.close()
        return "Saving succesfully: "
    # except Exception as e: 
    #     print(e)
    #     print("Error saving file.")
    #     return ": Error saving the file."
