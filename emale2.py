class Emale2:
    def __init__(self,userid,sentto,subject,message,val):
        self.userid = userid
        self.sentto = sentto
        self.subject = subject
        self.message = message
        self.val = val
        
    def toString(self):
        return self.userid+"~"+self.sentto + "~" + self.subject + "~" + self.message + "~" + self.val

    
    def serialize(self):
        return {'userid': self.userid,'sentto': self.sentto,'subject': self.subject,'message': self.message,'val' : self.val }









                                                                            
