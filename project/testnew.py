# GLOBAL VARIABLE BELOW
from json import dumps
import jwt
import hashlib
data = {
    'users' : [],
    'channels' : []
}
SECRET = 'peach'
def getData():
    global data
    return data
    

def sendSuccess(data):
    return dumps(data)
    
    
def sendError(message):
    return dumps({
        'error_exists' : message,
    })
    
def generateToken(email):
    global SECRET
    return str(jwt.encode({'email' : email}, SECRET, algorithm='HS256'))

def getUserFromToken(token):
    global SECRET
    decode = jwt.decode(token, SECRET, algorithm=['HS256'])
    return decode['email']

def hashpassword(password):
    return hashlib.sha256(password.encode()).hexdigest()

def fromtokentouid(token) :
    data = getData()
    email = getUserFromToken(token)
    for user in data['users']:
        if email == user["email"]:
            return (user[uid])
    return sendError("[fromtokentouid()] cannot find email")

    
def isvalidchannelid(channelid):
    data = getData()
    for id in data['channels']:
        if channelid == id['channel_id']:
            return True
    return False

def fn_channel_create(token, is_public, name):
    data = getData()
    u_id = fromtokentouid(token)

    '''if(isvalidtoken(token) == False):
        return sendError()'''
    
    if len(name) > 20:
        return sendError('Valueerror:Name is more than 20 characters')

    # name
    new_channel = {}
    new_channel['name'] = name
    # id
    channellist = data['channels']
    channel_id = len(channellist) + 1
    new_channel['channel_id'] = channel_id
    # member list
    new_channel['members'] = []
    new_channel['members'].append(u_id)
    # owner list 
    new_channel['owners'] = []
    new_channel['owners'].append(u_id)
    # public
    new_channel['is_public'] = is_public

    #update
    data['channals'].append(new_channel)
    return {'channel_id':channel_id}


    