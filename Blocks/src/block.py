import os
load_dotenv()
from dotenv import load_dotenv

MAX_TRANSACTIONS = os.getenv("MAX_TRANSACTIONS",10)

class Block:
    def __init__(self,previous_block:str="00000000",*args,**kwargs)->object:
        self.transactions = {}
        self.previous_block = previous_block
        self.signature = ""

    def add_transaction(self,block:object)->None:
        #Guard validation 
        if len(self.transactions) >= MAX_TRANSACTIONS:
            ## stash de la transaccion si se llena 
            self.signature = self.mine_block()
            self.add_to_chain()
            return
        if block.voter in  self.transactions.keys():
            raise ValueError("This voter has previous vote, invalid transaction")
        self.transactions[block.voter] = block.export
        #Guard validation
        if len(self.transactions) >= MAX_TRANSACTIONS:
            ## stash de la transaccion si se llena 
            self.signature = self.mine_block()
            self.add_to_chain()
        return

    def mine_block(self)->str:
        pass

    def add_to_chain(self)->None:
        pass

    def export(self)->dict:
        return {
            "previous_block":"",
            "transactions":self.transactions,
            "signature":self.signature
        }