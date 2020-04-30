import uuid
import dataset
import logging
from emale2 import Emale2
from flask import current_app
import sys
FORMAT = "[%(filename)s:%(lineno)s - %(funcName)10s() ] %(message)s"
logging.basicConfig(filename='output.log',format=FORMAT)
logger = logging.getLogger('root')
logger.setLevel(logging.DEBUG)
class EmaleDao:
    def __init__(self):
        self.connectString = 'sqlite:///inbox.db'
        self.db = dataset.connect(self.connectString)
        self.table = self.db['inbox']



    def rowToEmail(self,row):
        emale = Emale2(row['userid'],row['sentto'],row['subject'],row['message'],row['val'])
        return emale

    def emailToRow(self,emale):
        row = dict(userid = emale.userid,sentto = emale.sentto,subject=emale.subject,message = emale.message,val = emale.val)
        return row


    def insert(self,emale):
        self.table.insert(self.emailToRow(emale))
        self.db.commit()


    def selectByVal(self,emale):
        rows = self.table.find(val=val)
        return rows

    def getMessage(self,val):
        rows = self.table.find(val=val)
        result = []
        for i in rows:
            result.append(self.rowToEmail(i))
        
        return result


    def delete(self,val):
        self.table.delete(val=val)
        self.db.commit()

    def getInbox(self,userid):
        inbox = self.table.find(sentto=userid)
        #result = None
        #if inbox is not None:
        #    result = inbox

        result = []
        for i in inbox:
            result.append(self.rowToEmail(i))
            

        
        return result


    def getOutbox(self,userid):
        outbox = self.table.find(userid=userid)
        #result = None
        #if outbox is not None:
        #    result = outbox
        result = []
        for i in outbox:
            result.append(self.rowToEmail(i))




        return result


    def getVal(self):
        x = uuid.uuid4().hex[:10]
        return x

    def selectAllInbox(self,userid):
        inbox = self.table.find(userid=userid)
        return inbox

    def populate(self):
        x = self.getVal()
        y = self.getVal()
        z = self.getVal()
        a = self.getVal()
        f = self.getVal()
        self.table.insert(self.emailToRow(Emale2('tim','mike','subject 1','kjdfjdsfhsk',x)))
        self.table.insert(self.emailToRow(Emale2('mike','tim','subject 1','sdfdskjdfjdsfhsk',y)))
        self.table.insert(self.emailToRow(Emale2('john','tim','subject 1','dsfhsk',z)))
        self.table.insert(self.emailToRow(Emale2('tim','john','subject 1','trsttestkjdfjdsk',a)))
        self.table.insert(self.emailToRow(Emale2('john','mike','subject 1','AAAAAAA',f)))



dao = EmaleDao()

