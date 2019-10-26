from server import *
import datetime
def fn_channel_create(token,name,is_public):
    data = getData()
    u_id = fromtokentouid(token)
    '''if(isvalidtoken(token) == False):
        return sendError()'''
    
    if (len(name) > 20):
        raise ValueError('Name is more than 20 characters')

    # name
    new_channel = {}
    new_channel['name'] = name
    # id
    global channel_id
    channel_id = channel_id + 1
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
    data['channels'].append(new_channel)
    if(isValidChanelId(channel_id) == False):
        raise ValueError('Channel ID is not a valid channel')
    return {'channel_id':channel_id}
    
def fn_channel_list(token):
    data = getData()
    token = request.args.get('token')
    u_id = fromtokentouid(token)
    channdic = []
    for user in data['channels']:
        for idcheck in user['members']:
            if u_id == idcheck:
                channdic.append({'channel_id': user['channel_id'],'name':user['name']})
    return {'channels':channdic}

def fn_channel_listall(token):
    data = getData()
    token = request.args.get('token')
    channdic = []
    for user in data['channels']:
        channdic.append({'channel_id': user['channel_id'],'name':user['name']})
    return {'channels':channdic}

def fn_channel_join(token,channel_id):
    data = getData()
    u_id = fromtokentouid(token)
    user = findUser(token,'token')
    # user permission
    permission_id = user['permission_id']
    channel_id = int(channel_id)
    # channel_id
    if(isValidChanelId(channel_id) == False):
        raise ValueError('Channel ID is not a valid channel')
    # channel_public
    if(isChannelMember(u_id, channel_id) == True):
        raise ValueError('You are already the member of channel')
    for channel in data['channels']:
        if (channel_id == channel['channel_id']):
            publiccheck = channel['is_public']
    if(publiccheck == True):
        #can join without problem
        data['channels'][channel_id - 1]['members'].append(u_id)
    else:
        if(permission_id == 3):
            raise AccessError('Channel is a private channel')
        else:
            data['channels'][channel_id - 1]['members'].append(u_id)
            return {}

def fn_channel_details(token, channel_id):
    data = getData()
    u_id = fromtokentouid(token)
    channel_id = int(channel_id)
    if(isValidChanelId(channel_id) == False):
        raise ValueError('Channel ID is not a valid channel')
    found = 0
    for user in data['channels'][channel_id - 1]['members']:
        if (user == u_id):
            found = 1
    if (found != 1):
        raise ValueError('you are not a member of channel')
    detail = {}
    ownermember = []
    for every in data['channels']:
        if channel_id == every['channel_id']:
            for per in every['owners']:
                userpro = findUser(token,'token')
                name = {'u_id': per, 'name_first': userpro['name_first'], 'name_last': userpro['name_last']}
                ownermember.append(name)
    member = []
    for every1 in data['channels']:
        if channel_id == every1['channel_id']:
            for per1 in every1['members']:
                user1pro = findUser(token,'token')
                name1 = {'u_id': per1, 'name_first': user1pro['name_first'], 'name_last': user1pro['name_last']}
                member.append(name1)

    for channel in data['channels']:
        if channel_id == channel['channel_id']:
            detail = {'name':channel['name'],
            'owner_members':ownermember,
            'all_members':member,}
    return detail

def fn_channel_messages(token, channel_id, start):
    data = getData()
    channel_id = int(channel_id)
    if(isValidChanelId(channel_id) == False):
        raise ValueError('Channel ID is not a valid channel')
    u_id = fromtokentouid(token)
    user = findUser(token,'token')
    if (user == None):
        raise AccessError('you are not a member of channel')
    #add more
    totalnum = 0
    for word in data['messages']:
        if word['channel_id'] == channel_id:
            totalnum = totalnum + 1
    start = int(start)
    if(start > totalnum):
        raise ValueError('start exceed the maximum number of channel')
    messdic = {}
    messlist = []
    count = 0
    for text in data['messages']:
        if text['channel_id'] == channel_id:
            if text['message_id'] >= start:
                m_id = text['message_id']
                reactsall = text['reacts']
                #reacts_id = text['reacts']['react_id']
                for rea in reactsall:
                    reacts_id = rea['react_id']
                    rea['is_this_user_reacted'] =  hasUserReacted(u_id,m_id,reacts_id)
                messlist.append({'message_id':text['message_id'],'u_id':text['u_id'],'message':text['message'],'time_created':text['time_created'],
                'reacts':text['reacts'] ,'is_pinned':text['is_pinned']})
                count = count + 1
        if count == 50:
            return {'messages':messlist,'start':start,'end':start + 50}
    if count < 50:
        return {'messages':messlist,'start':start,'end':-1}

def fn_message_send(token, channel_id, message):
    data = getData()
    u_id = fromtokentouid(token)
    
    # Error handling:
    if (len(message) > 1000):
        raise ValueError("Message is more than 1000 characters")
    
    if (isValidChanelId(channel_id) == False):
        raise ValueError('Channel ID is not a valid channel')
        
    if isChannelMember(u_id, channel_id) == False:
        raise AccessError('User has not joined channel')
        
    # Adding message to data structure:  
    new_message = {}  
    global m_id 
    m_id = m_id + 1
    new_message['message_id'] = m_id

    new_message['u_id'] = u_id
    new_message['message'] = message 
    
    time_created = datetime.datetime.utcnow()
    #TODO
    test = datetime.datetime.now
    print(f"!!!!!!!TYPE OF time_created is {type(time_created)}")
    print(f"!!!!!!!TYPE OF test is {type(test)}")
    created_timestamp = time_created.timestamp()
    
    #created_timestamp = time_created.replace(tzinfo=timezone.utc).timestamp()
    new_message['time_created'] = created_timestamp
    
    time_sent = datetime.datetime.utcnow()
    #TODO
    sent_timestamp = time_sent.timestamp()
    #sent_timestamp = time_sent.replace(tzinfo=timezone.utc).timestamp()
    new_message['time_sent'] = sent_timestamp
    
    new_message['reacts'] = []
    new_message['is_pinned'] = False
    new_message['channel_id'] = channel_id
    
    data['messages'].append(new_message)
    
    return ({'message_id' : m_id})

def fn_channel_leave(token, channel_id):
    data = getData()
    channel_id = int(channel_id)
    if(isValidChanelId(channel_id) == False):
        raise ValueError('Channel ID is not a valid channel')
    u_id = fromtokentouid(token)
    user = findUser(token,'token')
    if (user == None):
        raise AccessError('you are not a member of channel')
    found = 0
    for user1 in data['channels'][channel_id - 1]['owners']:
        if (user1 == u_id):
            found = 1
            break
    if (found == 1):
        data['channels'][channel_id - 1]['owners'].remove(u_id)
    data['channels'][channel_id - 1]['members'].remove(u_id)
    return {}


def fn_channel_invite(token, channel_id, u_id):
    data = getData()
    found = 0
    channel_id = int(channel_id)
    if(isValidChanelId(channel_id) == False):
        raise ValueError('Channel ID is not a valid channel')
    invite_userid = fromtokentouid(token)
    for user in data['channels'][channel_id - 1]['members']:
        if (user == invite_userid):
            found = 1
    if (found != 1):
        raise AccessError('you are not a members of channel')
    inviteduser = findUser(u_id,'uid')
    if(inviteduser == None):
        raise ValueError('u_id does not refer to a valid user')
    data['channels'][channel_id - 1]['members'].append(u_id)
    return {}

def fn_channel_addowner(token, channel_id, u_id):
    data = getData()
    channel_id = int(channel_id)
    u_id = int(u_id)
    if(isValidChanelId(channel_id) == False):
        raise ValueError('Channel ID is not a valid channel')
    for user in data['channels'][channel_id - 1]['owners']:
        if (user == u_id):
            found = 1
            break
    if (found == 1):
        raise ValueError('user already is owner of channel')
    for user in data['channels'][channel_id - 1]['members']:
        if (user == u_id):
            foundmem = 1
            break
    if (foundmem != 1):
        raise ValueError('user is not a member of channel')
    userid = fromtokentouid(token)
    for owner in data['channels'][channel_id - 1]['owners']:
        if (owner == userid):
            owner = 1
            break
    permission_id = data['user'][userid - 1]['permission_id']
    if(permission_id == 3 and owner != 1 ):
        raise AccessError('you do not have access to do that')
    data['channels'][channel_id - 1]['owners'].append(u_id)
    return {}

def fn_channel_removeowner(token, channel_id, u_id):
    data = getData()
    channel_id = int(channel_id)
    u_id = int(u_id)
    found = 0
    if(isValidChanelId(channel_id) == False):
        raise ValueError('Channel ID is not a valid channel')
    for user in data['channels'][channel_id - 1]['owners']:
        if (user == u_id):
            found = 1
            break
    print(data['channels'][channel_id - 1]['owners'])
    print(u_id)
    print(found)
    if (found != 1):
        raise ValueError('user is not a owner of channel')
    userid = fromtokentouid(token)
    for owner in data['channels'][channel_id - 1]['owners']:
        if (owner == userid):
            owner = 1
            break
    remove = findUser(token,'token')
    permission_id = remove['permission_id']
    if(permission_id == 3 and owner != 1 ):
        raise AccessError('you do not have access to do that')
    data['channels'][channel_id - 1]['owners'].remove(u_id)
    return {}