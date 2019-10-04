import sys
def auth_register(email, password, name_first, name_last):
    return{ 'u_id':'', 'token':'' }

def channel_invite(token, channel_id, u_id):
    return{}
    
def channel_details(token, channel_id):
    return{'name':'', 'owner_members':'', 'all_members':{}}

def channel_message(token, channel_id, start):
    return{'messages':'', 'start':'', 'end':''}

def channel_leave(token, channel_id):
    return{}

def channel_join(token, channel_id):
    return{}

def channel_addowner(token, channel_id, u_id):
    return{}

def channel_removeowner(token, channel_id, u_id):
    return{}

def channels_list(token):
    return{'id':'asdasd','name':'asdasd'}

def channels_listall(token):
    return{'id':'asdasd','name':'asdasd'}


def channels_create(token, name, is_public):
    return{'channel_id':'12312412431'}