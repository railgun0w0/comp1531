import jwt
import hashlib
from json import dumps
from flask import Flask, request

APP = Flask(__name__)
        
# GLOBAL VARIABLE BELOW
data = {
    'users' : [],
    'channels' : []
}

SECRET = 'peach'
# GLOBAL VARIABLE ABOVE
'''
@APP.route('/user/create', methods=['POST'])
@APP.route('/user/connect', methods=['PUT'])
@APP.route('/user/secret', methods=['GET'])


'''

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


#post
@APP.route('/channels/create', methods=['POST'])
def channel_create():
    data = getData()
    token =  request.form.get('token')
    is_public = request.form.get('is_public')
    name = request.form.get('name')
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
    new_channel['standup'] = False

    #update
    data['channals'].append(new_channel)
    return sendSuccess({'channel_id':channel_id})


@APP.route('/channels/join', methods=['POST'])
def channel_join():
    data = getData()
    token =  request.form.get('token')
    channel_id = request.form.get('channel_id')
    u_id = fromtokentouid(token)

    # user permission
    permission_id = data['user'][u_id - 1]['permission_id']

    #channel_id
    if(isvalidchannelid(channel_id) == False):
        return sendError('ValueError:Channel ID is not a valid channel')
    

    # channel_public
    for channel in data['channels']:
        if (channel_id == channel['channel_id']):
            publiccheck = channel['is_public']

    if(publiccheck == True):
        #can join without problem
        data['channels'][channel_id - 1]['members'].append(u_id)
    else:
        if(permission_id == 3):
            return sendError('AccessError:Channel is a private channel')
        else:
            data['channels'][channel_id - 1]['members'].append(u_id)
            return sendSuccess({})

@APP.route('/channels/invite', methods=['POST'])
def channel_invite():
    data = getData()
    token =  request.form.get('token')
    channel_id = request.form.get('channel_id')
    u_id = request.form.get('u_id')
    found = 0
    if(isvalidchannelid(channel_id) == False):
        return sendError('ValueError:Channel ID is not a valid channel')
    invite_userid = fromtokentouid(token)
    for user in data['channels'][channel_id - 1]['members']:
        if (user == invite_userid):
            found = 1
    if (found != 1):
        return sendError('ValueError:you are not a members of channel')
    
@APP.route('/channels/list', methods=['GET'])
def channel_list():
    data = getData()
    token = request.args.get('token')
    u_id = fromtokentouid(token)
    channdic = []
    for user in data['channels']:
        for idcheck in user['members']:
            if u_id == idcheck:
                channdic.append({'channel_id': user['channel_id'],'name':user['name']})
    return sendSuccess({channdic})


@APP.route('/channels/listall', methods=['GET'])
def channel_listall():
    data = getData()
    token = request.args.get('token')
    channdic = []
    for user in data['channels']:
        channdic.append({'channel_id': user['channel_id'],'name':user['name']})
    return sendSuccess({channdic})

@APP.route('/channels/addowner', methods=['POST'])
def channel_addowner():
    data = getData()
    token = request.form.get('token')
    channel_id = request.form.get('channel_id')
    u_id = request.form.get('u_id')
    if(isvalidchannelid(channel_id) == False):
        return sendError('ValueError:Channel ID is not a valid channel')
    for user in data['channels'][channel_id - 1]['owners']:
        if (user == u_id):
            found = 1
            break
    if (found == 1):
        return sendError('ValueError:user already is owner of channel')
    for user in data['channels'][channel_id - 1]['members']:
        if (user == u_id):
            foundmem = 1
            break
    if (foundmem != 1):
        return sendError('ValueError:user is not a member of channel')

    userid = fromtokentouid(token)
    for owner in data['channels'][channel_id - 1]['owners']:
        if (owner == userid):
            owner = 1
            break
    permission_id = data['user'][userid - 1]['permission_id']
    if(permission_id == 3 and owner != 1 ):
        return sendError('AccessError:you do not have access to do that')
    data['channel'][channel_id - 1]['owners'].append(u_id)
    return sendSuccess({})
            


@APP.route('/channels/removeowner', methods=['POST'])
def channel_removeowner():
    data = getData()
    token = request.form.get('token')
    channel_id = request.form.get('channel_id')
    u_id = request.form.get('u_id')
    if(isvalidchannelid(channel_id) == False):
        return sendError('ValueError:Channel ID is not a valid channel')
    for user in data['channels'][channel_id - 1]['owners']:
        if (user == u_id):
            found = 1
            break
    if (found != 1):
        return sendError('ValueError:user is not a owner of channel')
    userid = fromtokentouid(token)
    for owner in data['channels'][channel_id - 1]['owners']:
        if (owner == userid):
            owner = 1
            break
    permission_id = data['user'][userid - 1]['permission_id']
    if(permission_id == 3 and owner != 1 ):
        return sendError('AccessError:you do not have access to do that')
    data['channel'][channel_id - 1]['owners'].remove(u_id)
    return sendSuccess({})

@APP.route('/channels/leave', methods=['POST'])
def channel_leave():
    data = getData()
    token = request.form.get('token')
    channel_id = request.form.get('channel_id')
    if(isvalidchannelid(channel_id) == False):
        return sendError('ValueError:Channel ID is not a valid channel')
    u_id = fromtokentouid(token)
    for user in data['channels'][channel_id - 1]['members']:
        if (user == u_id):
            found = 1
    if (found != 1):
        return sendError('ValueError:you are not a member of channel')
    for user1 in data['channels'][channel_id - 1]['owners']:
        if (user1 == u_id):
            found = 1
            break
    if (found == 1):
        data['channels'][channel_id - 1]['owners'].remove(u_id)
    data['channels'][channel_id - 1]['members'].remove(u_id)
    return sendSuccess({})

@APP.route('/channels/messages', methods=['GET'])
def channel_messages():
    data = getData()
    token = request.args.get('token')
    channel_id = request.args.get('channel_id')
    start = request.args.get('start')
    if(isvalidchannelid(channel_id) == False):
        return sendError('ValueError:Channel ID is not a valid channel')
    u_id = fromtokentouid(token)
    for user in data['channels'][channel_id - 1]['members']:
        if (user == u_id):
            found = 1
    if (found != 1):
        return sendError('AccessError:you are not a member of channel')
    #add more
    totalnum = 0
    for word in data['message']:
        if word['channel_id'] == channel_id:
            totalnum = totalnum + 1
    if(start >= totalnum):
        return sendError('start exceed the maximum number of channel')
    messdic = {}
    messlist = []
    count = 0
    for text in data['message']:
        if text['channel_id'] == channel_id:
            if text['message_id'] >= start:
                text['reacts']['is_this_user_reacted'] = hasUserReacted(text['u_id'],text['message_id'],text['reacts']['react_id'])
                messlist.append({'message_id':text['message_id'],'u_id':text['u_id'],'message':text['message'],'time_created':text['time_created'],
                'reacts':text['reacts'] ,'is_pinned':text['is_pinned'],})
                count = count + 1
        if count == 50:
            return sendSuccess({'messages':messlist,'start':start,'end':start + 50})
    if count < 50:
        return sendSuccess({'messages':messlist,'start':start,'end':-1})
        

@APP.route('/channels/details', methods=['GET'])
def channel_details():
    data = getData()
    token = request.args.get('token')
    u_id = fromtokentouid(token)
    channel_id = request.form.get('channel_id')
    if(isvalidchannelid(channel_id) == False):
        return sendError('ValueError:Channel ID is not a valid channel')
    for user in data['channels'][channel_id - 1]['members']:
        if (user == u_id):
            found = 1
    if (found != 1):
        return sendError('ValueError:you are not a member of channel')
    for channel in data['channels']:
        if channel_id == channel['channel_id']:
            detail = {'name': channel['name'], 'owner_member':channel['owner'], 'all_member':channel['members']}
    return sendSuccess(detail)