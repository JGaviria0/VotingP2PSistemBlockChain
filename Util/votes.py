from dotenv import load_dotenv
from datetime import datetime
from Util import hashing
import random

#Saquial
def addVote(votes, IDV, IP, IDC):

    header = {
        "Client": IP,
        "Vote": hashing.hashString(IDC),
        "Date": str(datetime.now())
    }

    Vot = hashing.hashString(IDV)
    if votes.get(Vot) is None:
        votes[Vot] = header

    return votes

def createBlock(prevBlock, votes):

    header = {
        "previous_block": prevBlock,
        "transactions": votes,
        "signature": ""
    }

    return header