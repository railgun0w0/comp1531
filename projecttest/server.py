import random
import time
import re 
import jwt
import hashlib
import sys
from channelutil import *
from flask_cors import CORS
from json import dumps
from flask import Flask, request, jsonify
from werkzeug.exceptions import HTTPException
from flask_mail import Mail, Message

gpasw = {"gpass":"T13B_404"}

def isValidChanelId(channelid):
    data = getData()
    for channel in data['channels']:
        if channelid == channel['channel_id']:
            return True
    return False

def defaultHandler(err):
    response = err.get_response()
    response.data = dumps({
        "code": err.code,
        "name": "System Error",
        "message": err.get_description(),
    })
    response.content_type = 'application/json'
    return response


APP = Flask(__name__)
CORS(APP)


APP.config['TRAP_HTTP_EXCEPTIONS'] = True
APP.register_error_handler(Exception, defaultHandler)
CORS(APP)

class ValueError(HTTPException):
    code = 400
    message = 'No message specified'

class AccessError(HTTPException):
    code = 400
    message = 'No message specified'
    
APP.config.update(
    MAIL_SERVER='smtp.gmail.com',
    MAIL_PORT=465,
    MAIL_USE_SSL=True,
    MAIL_USERNAME = 'liyunchuanm9@gmail.com',
    MAIL_PASSWORD = gpasw['gpass'],
)


# GLOBAL VARIABLE BELOW
data = {
    'users' : [{
        'email' : "liyunchuanm9@gmail.com",
        'password' : hashlib.sha256("12345645".encode()).hexdigest(),#"387a3bcfe80f5addac15b1f72ac8f50200d965cd59b0d786439155b8431c0229",
        'name_first' : 'first',
        'name_last' : 'last',
        'permission_id' : 1,
        'u_id' : 1,
        'loginstat' : ["eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJlbWFpbCI6ImxpeXVuY2h1YW5tOUBnbWFpbC5jb20ifQ.lij1dwIkLqY-LKTicIbSU5VDJ2yXY9CTnuUuZ8bHK0c"],
        'handle' : "nobody",   
    }],
    'channels' : [],
    'messages' : []
}
uid = 1
#SECRET = "comp1531"
SECRET = 'peach'
regex = '^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$'
randomStr = ""
remail = ""
channel_id = 0
m_id = 0
# GLOBAL VARIABLE ABOVE

def getData():
    global data
    return data
    
def getuid():
    global uid
    uid += 1
    return uid
    
def sendSuccess(data):
    return dumps(data)
    
    
def sendError(message):
    return dumps({
        'error_exists' : message,
    })
    
def generateToken(email):
    global SECRET
    preset = {
        "email" : email,
        #"timestamp" : time.time(),
    }
    encoded = jwt.encode(preset, SECRET, algorithm='HS256')
    return encoded.decode('utf-8')

def getUserFromToken(token):
    global SECRET
    decoded = jwt.decode(token, SECRET, algorithm=['HS256'])
    return decoded['email']
    #return decoded
    
# return account dic based on email or uid or token
# comment need to be "email", "uid" or "token"
# return None if cannot found target in data["users"]
def findUser(user, comment):
    data = getData()
    print("!!!FINDUSE!!!")
    print(user)
    print(comment)
    
    if (comment == "email") :
        for u in data['users']:
            if u['email'] == user:
                return u
        return None
            
    elif (comment == "uid"):
        print("1")
        for u in data['users']:
            print("2")
            print(u['u_id'])
            if (int(u['u_id']) == int(user)):
                print("3")
                print(u)
                return u
        print("4")
        return None
            
    elif (comment == "token"):
        for u in data['users']:
            for t in u['loginstat']:
                if user == t:
                    return u
        return None
    
    return None
#####  
    
def hashpassword(password):
    return hashlib.sha256(password.encode()).hexdigest()

def isinvalidemail(email):
    if(re.search(regex,email)):  
        return False
    else:  
        return True
        
def isvalidemail(email):
    if(re.search(regex,email)):  
        return True
    else:  
        return False
        
def isemailexist(email):
    if findUser(email, "email") is not None:
        return True
    else:
        return False

def fromtokentouid(token):
    data = getData()
    userdic1 = findUser(token, "token")
    return userdic1['u_id']
    
        
def isvalidtoken(token):
    if findUser(token, "token") is not None:
        return True
    else:
        return False

def newRand():
    global randomStr
    randomStr = ''.join(random.sample(['a','b','c','d','e','f','g','h','i','j', 'k', 'l','m', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z'], 4))
    return randomStr
    
def isChannelMember(u_id, channel_id):
    data = getData()
    for channel in data['channels']:
        if channel_id == channel['channel_id']:
            break
    
    for member in channel['members']:
        if u_id == member:
            return True
    return False

def hasUserReacted(u_id, message_id, react_id):
    data = getData()
    react = messageReacted(message_id, react_id)
    if react == False:
        return False
    '''    
    for message in data['messages']
        if message_id == message['message_id']:
            break
    for react in message['reacts']:
        if react_id == react['react_id']:
            break
    '''  
    for u_id_reacted in react['u_ids']:
        if u_id == u_id_reacted:
            return True
    return False

##################################

@APP.route('/auth/register', methods=['POST'])
def auth_register():
    email = request.form.get('email')
    password = request.form.get('password')
    first = request.form.get('firstname')
    last = request.form.get('lastname')
    S = {}
    S = auth_register_back(email, password, first, last)
    print(S)
    return dumps(S)

def auth_register_back(email, password, first, last):
    # input email
    data = getData()
    print("##################")
    print(data)
    #email = request.form.get('email')
    
    print(email)
    
    if (isinvalidemail(email)) :
        raise ValueError(description="invalid email")
    if (isemailexist(email)) :
        raise ValueError(description="email has been used by another user")
    
    # inut password
    #password = request.form.get('password')
    if (len(password) < 6):
        raise ValueError(description="invalid password")
    
    # input name
    #first = request.form.get('firstname')
    #last = request.form.get('lastname')
    if (len(first) > 6 or len(last) > 6 or len(first) < 1 or len(last) < 1) :
        raise ValueError(description="invalid name")
    
    print(email)
    print(password)
    print(hashpassword(password))
    print(first)
    print(last)
    
    # all test pass, inserting data
    data = getData()
    u = getuid()
    print(uid)
    
    data['users'].append({
        'email' : email,
        'password' : hashpassword(password),
        'first_name' : first,
        'last_name' : last,
        'permission_id' : 3,
        'u_id' : u,
        'loginstat' : [],
        'handle' : "nobody",
    })
    
    print(data)
    return {
        'u_id' : u,
        'token': generateToken(email),
    }



@APP.route('/auth/login', methods=['POST'])
def auth_login():
    # input email
    email = request.form.get('email')
    # inut password
    password = request.form.get('password')
    
    return auth_login_back(email, password)



def auth_login_back(email, password):
    data = getData()
    
    # input email
    #email = request.form.get('email')
    if (isinvalidemail(email)) :
        raise ValueError(description="invalid email")
    
    # inut password
    #password = request.form.get('password')
    
    if (isemailexist(email)):
        print("4556897948")
        userdic = findUser(email, "email")
        
        if hashpassword(password) != userdic["password"] :
            print(data)
            raise ValueError(description="Username or password incorrect")
        else:
            newtoken = generateToken(email)
            userdic["loginstat"].append(newtoken)
            print(data)
            return sendSuccess({
                "u_id" : fromtokentouid(newtoken),
                "token" : newtoken,
            })
            
                    
    raise ValueError(description="Username or password incorrect")

  
@APP.route('/auth/logout', methods=['POST'])
def auth_logout():
    tk = request.form.get('token')
    return auth_logout_back(tk)


def auth_logout_back(tk):
    print("Logging out user")
    data = getData()
    print(data)
    tk = request.form.get('token')
    print(tk)
    email = getUserFromToken(tk)
    print(email)
    userdic = findUser(email, "email")
    print(userdic)
    
    
    if userdic is not None:
        print("Logging out user")
        userdic["loginstat"].remove(request.form.get('token'))
        print(data)
        print("########")
        return sendSuccess({"is_success" : True})
    else:
        return sendSuccess({"is_success" : False})
    

@APP.route('/auth/passwordreset/request', methods=['POST'])
def auth_passwordreset_request():
    # input email
    email = request.form.get('email')
    return auth_passwordreset_request_back(email)


def auth_passwordreset_request_back(email):
    global randomStr
    # input email
    #email = request.form.get('email')
    global remail
    remail = email
    if (isinvalidemail(email)) :
        raise ValueError(description="invalid email")
    if (isemailexist(email)) :
        pass
    else:
        raise ValueError(description="wrong email")
    
    mail = Mail(APP)
    try:
        sendtitle = "Send Mail Test!"
        senditem = newRand()
        msg = Message(sendtitle,
            sender="liyunchuanm9@gmail.com",
            recipients=[email])
        msg.body = senditem
        print(randomStr)
        print(remail)
        mail.send(msg)
        return 'Mail sent!'
    except Exception as e:
        return (str(e))


@APP.route('/auth/passwordreset/reset', methods=['POST'])
def auth_password_reset():
    # inut reset_code
    rcode = request.form.get('reset_code')
    # inut password
    rpassword = request.form.get('new_password')



def auth_password_reset_back():
    
    global randomStr
    global remail
    
    # inut reset_code
    rcode = request.form.get('reset_code')
    # inut password
    rpassword = request.form.get('new_password')
    
    if (rcode != randomStr) :
        raise ValueError(description="Reset code incorrect")
        
    if (len(rpassword) < 6):
        raise ValueError(description="invalid password")
        
    userdic = findUser(remail, "email")
    
    userdic["password"] = hashpassword(rpassword)
    
    return sendSuccess({})
    
    
    
@APP.route('/search', methods=['GET'])
def search():
    tk = request.args.get('token')
    target = request.args.get('query_str')
    return search_back(tk, target)


def search_back(tk, target):
    print("search")
    tk = request.args.get('token')
    target = request.args.get('query_str')
    userdic = findUser(tk, "token")
    
    targetchannel = []
    messages = []
    
    for c in data["channel"]:
        if userdic['u_id'] == c['owner']:
            targetchannel.append(c['channel_id'])
        else :
            for u in c['member']:
                if userdic['u_id'] == u:
                    targetchannel.append(c['channel_id'])
                    break
    
    for m in data['message']:
        if m[channel_id] in targetchannel:
            if target.find(m['message']) != -1:
                mes = {}
                mes['message_id'] = m['message_id']
                mes['u_id'] = m['u_id']
                mes['message'] = m['message']
                mes['time_created'] = m['time_created']
                mes['reacts'] = m['reacts']
                mes['is_pinned'] = m['is_pinned']
                messages.append(mes)
            else:
                pass
        else:
            pass
    
    pass
    return sendSuccess(messages)
    
    
    
@APP.route('/admin/userpermission/change', methods=['POST'])
def admin_userpermission_change():
    # input token
    tk = request.form.get('token')
    # input permission_id
    pid = int(request.form.get('permission_id'))
    uid = int(request.form.get('u_id'))
    return admin_userpermission_change_back(tk, pid, uid)


def admin_userpermission_change_back(tk, pid, uid):
    # input token
    tk = request.form.get('token')
    # check token
    userdic = findUser(tk, "token")
    if userdic is not None:
        pass
    else :
        raise ValueError(description="invalid token")
    # check permission
    if userdic['permission_id'] == 3:
        raise AccessError(description="permission denied")
    
    # input u_id
    uid = request.form.get('u_id')
    # check u_id
    targetdic = findUser(uid, "uid")
    
    print(targetdic)
    print("[413]")
    if targetdic is not None:
        print("[414]")
        pass
        print("[417]")
    else:
        print("[419]")
        raise ValueError(description="invalid u_id")
    
    print("[422]")
        
    # input permission_id
    pid = int(request.form.get('permission_id'))
    print(f"pid: {pid}")
    # check permission_id
    print("[428]")
    if int(pid) <= 0 and int(pid) >= 4:
        print("[429]")
        raise ValueError(description="invalid permission_id")
        print("[429]")
    print([432])
    
    targetdic['permission_id'] = pid
    print("[435]")
    print(targetdic)
    print("[437]")
    return sendSuccess({})

#########CHANNEL

@APP.route('/channels/create', methods=['POST'])
def channel_create():
    token =  request.form.get('token')
    is_public = request.form.get('is_public')
    name = request.form.get('name')
    try:
        fn_return = fn_channel_create(token,name,is_public)
        return sendSuccess(fn_return)
    except ValueError as a:
        raise ValueError(description=f"{a}")
    except AccessError as b:
        raise AccessError(description=f"{b}")
    

@APP.route('/channels/list', methods=['GET'])
def channel_list():
    token = request.args.get('token')
    fn_return = fn_channel_list(token)
    return sendSuccess(fn_return)

@APP.route('/channels/listall', methods=['GET'])
def channel_listall():
    token = request.args.get('token')
    fn_return = fn_channel_listall(token)
    return sendSuccess(fn_return)


@APP.route('/channel/join', methods=['POST'])
def channel_join():
    token =  request.form.get('token')
    channel_id = request.form.get('channel_id')
    try:
        fn_return = fn_channel_join(token,channel_id)
        return sendSuccess(fn_return)
    except ValueError as a:
        raise ValueError(description=f"{a}")
    except AccessError as b:
        raise AccessError(description=f"{b}")
    
@APP.route('/channel/details', methods=['GET'])
def channel_details():
    token = request.args.get('token')
    channel_id = request.args.get('channel_id')
    try:
        fn_return = fn_channel_details(token,channel_id)
        return sendSuccess(fn_return)
    except ValueError as a:
        raise ValueError(description=f"{a}")
    except AccessError as b:
        raise AccessError(description=f"{b}")

@APP.route('/channel/messages', methods=['GET'])
def channel_messages():
    token = request.args.get('token')
    channel_id = request.args.get('channel_id')
    start = request.args.get('start')
    try:
        fn_return = fn_channel_messages(token,channel_id,start)
        return sendSuccess(fn_return)
    except ValueError as a:
        raise ValueError(description=f"{a}")
    except AccessError as b:
        raise AccessError(description=f"{b}")

@APP.route("/message/send", methods=['POST'])
def message_send():
    
    token = request.form.get('token')
    channel_id = request.form.get('channel_id')
    channel_id = int(channel_id)
    message = request.form.get('message')
    
    
    try:
        fn_return = fn_message_send(token, channel_id, message)
        return sendSuccess(fn_return)
    except ValueError as e:
        raise ValueError(description=f"{e}")
    except AccessError as er:
        raise AccessError(description=f"{er}")

@APP.route('/channel/leave', methods=['POST'])
def channel_leave():
    token = request.form.get('token')
    channel_id = request.form.get('channel_id')
    try:
        fn_return = fn_channel_leave(token, channel_id)
        return sendSuccess(fn_return)
    except ValueError as a:
        raise ValueError(description=f"{a}")

@APP.route('/channel/invite', methods=['POST'])
def channel_invite():
    token =  request.form.get('token')
    channel_id = request.form.get('channel_id')
    u_id = request.form.get('u_id')
    try:
        fn_return = fn_channel_invite(token, channel_id, u_id)
        return sendSuccess(fn_return)
    except ValueError as a:
        raise ValueError(description=f"{a}")
    except AccessError as b:
        raise AccessError(description=f"{b}")

@APP.route('/channel/addowner', methods=['POST'])
def channel_addowner():
    data = getData()
    token = request.form.get('token')
    channel_id = request.form.get('channel_id')
    u_id = request.form.get('u_id')
    try:
        fn_return = fn_channel_addowner(token, channel_id, u_id)
        return sendSuccess(fn_return)
    except ValueError as a:
        raise ValueError(description=f"{a}")
    except AccessError as b:
        raise AccessError(description=f"{b}")


@APP.route('/channel/removeowner', methods=['POST'])
def channel_removeowner():
    data = getData()
    token = request.form.get('token')
    channel_id = request.form.get('channel_id')
    u_id = request.form.get('u_id')
    try:
        fn_return = fn_channel_removeowner(token, channel_id, u_id)
        return sendSuccess(fn_return)
    except ValueError as a:
        raise ValueError(description=f"{a}")
    except AccessError as b:
        raise AccessError(description=f"{b}")

##MAIN##
if (__name__ == '__main__'):
    
    
    
    
    #print(newRand())
    #print(randomStr)
    #print(newRand())
    #print(randomStr)
    #print(newRand())
    #print(randomStr)
    #print(newRand())
    APP.run(port=(sys.argv[1] if len(sys.argv) > 1 else 5000), debug = True)
    
            
