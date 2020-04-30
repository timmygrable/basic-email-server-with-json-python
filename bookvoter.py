from jsonpickle import encode
import sys
from emale2 import Emale2
from flask import Flask
from flask import abort, redirect, url_for
from flask import request
from flask import render_template
from flask import session
from flask import jsonify
from emale2 import Emale2
import logging
from userdao import UserDao
from emaledao import EmaleDao
from user import User
FORMAT = "[%(filename)s:%(lineno)s - %(funcName)10s() ] %(message)s"
logging.basicConfig(filename='output.log',format=FORMAT)
logger = logging.getLogger('root')
logger.setLevel(logging.DEBUG)

app = Flask(__name__)

@app.route('/')
def index():
    return redirect(url_for('login'))


@app.route('/login',methods=['POST','GET'])
def login():
    error = None
    if('userid' in request.form):
        if isValid(request.form['userid'],request.form['password']):
            userid = request.form['userid']
            session['userid'] = userid
            return render_template('emale.html',**locals())

        else:
            error = 'Invalid Userid/Password'

    return render_template('login.html',**locals())



def isValid(userid,password):
    dao = UserDao()
    user = dao.selectByUserid(userid)
    if (user is not None) and (userid == user.userid) and (password == user.password):
        session['user'] = encode(user)
        return True
    else:
        return False




@app.route('/ajax_getinbox',methods=['POST','GET'])
def ajax_getinbox():
    error = None
    dao = EmaleDao()
    userid= session['userid']
    inbox = dao.getInbox(userid)
    #logger.debug("INBOX",inbox.userid)
    serialized_inbox = [emale2.serialize() for emale2 in inbox]
    return jsonify(serialized_inbox)
   # return
    
@app.route('/ajax_getoutbox',methods=['POST','GET'])
def ajax_getoutbox():
    error = None
    dao = EmaleDao()
    userid = session['userid']
    outbox = dao.getOutbox(userid)
    serialized_outbox = [emale2.serialize() for emale2 in outbox]
    return jsonify(serialized_outbox)
    



@app.route('/create',methods=['POST','GET'])
def create():
    error = None
    if('userid' in request.form) and ('password' in request.form):
        if(request.form['userid'] is not None) and (request.form['password'] is not None):
            dao = UserDao()
            userid = request.form['userid']
            password = request.form['password']
            dao.insert(User(userid,password))
            return login()
    return render_template('create.html',**locals())





@app.route('/compose',methods=['POST','GET'])
def compose():
        error = None
        current_user = session['userid']
        dao = UserDao()
        userids = dao.selectAllUsers()
        if('sentto' in request.form) and ('subject' in request.form) and ('message' in request.form):
            if(request.form['sentto'] is not None) and (request.form['subject'] is not None) and (request.form['message'] is not None):
                dao2 = EmaleDao()
                x = dao2.getVal()
                sentto = request.form['sentto']
                subject = request.form['subject']
                message = request.form['message']
                dao2.insert(Emale2(current_user,sentto,subject,message,x))
                inbox = dao2.getInbox(current_user)
                outbox = dao2.getOutbox(current_user)
                return render_template('emale.html',**locals())

        return render_template('compose.html',**locals())




@app.route('/ajax_getmessage',methods=['POST','GET'])
def getmessage():
    error = None
    val = request.args.get('val')
    dao = EmaleDao()
    message = dao.getMessage(val)
    serialized_message = [emale2.serialize() for emale2 in message]
    return jsonify(serialized_message)



@app.route('/ajax_deleteinbox',methods=['POST','GET'])
def deleteinbox():
    error = None
    val = request.args.get('val')
    dao = EmaleDao()
    dao.delete(val)
    userid = session['userid']
    inbox = dao.getInbox(userid)
    serialized_inbox = [emale2.serialize() for emale2 in inbox]
    return jsonify(serialized_inbox)


@app.route('/ajax_deleteoutbox',methods=['POST','GET'])
def deleteoutbox():
    error = None
    val = request.args.get('val')
    dao = EmaleDao()
    dao.delete(val)
    userid = session['userid']
    outbox = dao.getOutbox(userid)
    serialized_outbox = [emale2.serialize() for emale2 in outbox]
    return jsonify(serialized_outbox)
    

if __name__ == "__main__":
    app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'
    app.run(host = '0.0.0.0',port=8000,threaded=True,debug=True)
