import hashlib
import os
from dotenv import load_dotenv
load_dotenv()
BUF_SIZE = int(os.getenv('BUF_SIZE'))
MAIN_DIRECTORY = os.getenv('MAIN_DIRECTORY')

# https://stackoverflow.com/questions/22058048/hashing-a-file-in-python
def hashfile(fname, path = MAIN_DIRECTORY):
    sha256 = hashlib.sha256()

    with open(f'{path}{fname}', 'rb') as f:
        while True:
            data = f.read(BUF_SIZE)
            if not data:
                break
            sha256.update(data)
    return sha256.hexdigest()