import dataset
from user import User

class UserDao:
        def __init__(self):
            self.connectString = 'sqlite:///users.db'
            self.db = dataset.connect(self.connectString)
            self.table = self.db['users']
            
        def rowToUser(self,row):
            user = User(row['userid'], row['password'])
            return user
        
        def userToRow(self,user):
            row = dict(userid=user.userid, password=user.password)
            return row
        
        def selectByUserid(self,userid):
            row = self.table.find_one(userid = userid)
            result = None
            if(row is not None):
                result = self.rowToUser(row)
            return result
        
        def selectAll(self):
            table = self.db['users']
            rows   = table.all()
            
            result = []
            for row in rows:
                result.append(self.rowToUser(row))
                
            return result
        


        def selectAllUsers(self):
                rows = self.table.all()
                results = []
                for row in rows:
                        userid = row['userid']
                        results.append(userid)
                return results


        def insert(self,user):
            self.table.insert(self.userToRow(user))
            self.db.commit()
            
        def update(self,user):
            self.table.update(self.userToRow(user),['userid'])
            self.db.commit()
            
        def delete(self,user):
            self.table.delete(userid=userid)
            self.db.commit()

        def populate(self):
            self.table.insert(self.userToRow(User('tim','test')))
            self.table.insert(self.userToRow(User('john','second')))
            self.table.insert(self.userToRow(User('mike','csrocks')))
            self.db.commit()


dao = UserDao()


