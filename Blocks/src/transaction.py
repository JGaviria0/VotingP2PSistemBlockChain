import datetime
class Transaction:
    def __init__(self,voter:str,client:str,vote:str,*args,**kwargs)->object:
        self.raw_data = {
            "client":client,
            "vote":vote,
            "timestamp":datetime.datetime.now()
        }
        self.voter = voter

    def add_to_block(self,block:object)->None:
        block.add_transction(self)

    def export(self)->dict:
        return self.raw_data