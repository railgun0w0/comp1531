
import pytest
from channel import *

class AccessError(Exception):
    pass

    #Test channel_invite function
def test_channel_invite_success():
    # SETUP BEGIN
    registerResponse1 = auth_register("validemail1@gmail.com", "validpassword1", "validname", "validname")
    u_id1 = registerResponse1['u_id']
    token1 = registerResponse1['token']
    channelResponse = channels_create(token1, "My Channel", False)
    channel_id = channelResponse['channel_id']
    registerResponse2 = auth_register("validemail2@gmail.com", "validpassword2", "validname", "validname")
    u_id2 = registerResponse2['u_id']
    token2 = registerResponse2['token']
    registerResponse3 = auth_register("validemail3@gmail.com", "validpassword3", "validname", "validname")
    u_id3 = registerResponse2['u_id']
    token3 = registerResponse2['token']
    # SETUP COMPLETE
    assert channel_invite(token1, channel_id, u_id2) == {} #should work since user1 is a member of channel
    #user1 try to invite user2 to the 'My channel' channel which made by user1.
    assert channel_invite(token2,channel_id,u_id3) == {} # #should work since user2 is a member of channel
    #user2 try to invite user3 to the 'My channel' channel which user2 is a member.


    

def test_channel_invite_Errorcheck1():
    # channel_id does not refer to a valid channel that the authorised user is part of.
    # user1 try to invite user3 to a channel which user2 create and user1 not a member of it

    # SETUP BEGIN
    registerResponse1 = auth_register("validemail1@gmail.com", "validpassword1", "validname", "validname")
    u_id1 = registerResponse1['u_id']
    token1 = registerResponse1['token']
    channelResponse1 = channels_create(token1, "My Channel", False)
    channel_id1 = channelResponse1['channel_id']
    registerResponse2 = auth_register("validemail2@gmail.com", "validpassword2", "validname", "validname")
    u_id2 = registerResponse2['u_id']
    token2 = registerResponse2['token']
    channelResponse2 = channels_create(token2, "My Channel1", False)
    channel_id2 = channelResponse2['channel_id']
    registerResponse3 = auth_register("validemail3@gmail.com", "validpassword3", "validname", "validname")
    u_id3 = registerResponse2['u_id']
    token3 = registerResponse2['token']
    # SETUP COMPLETE
    with pytest.raises(ValueError):
        channel_invite(token1, channel_id2, u_id3)  # Should NOT work since User1 is not a member of channel2
        channel_invite(token1,'invalid_channel_id',u_id1) # Should NOT work since channelid invalid


def test_channel_invite_Errorcheck2():
    # user1 try to invite a person which does not exist
    # u_id does not refer to a valid user
    # SETUP BEGIN
    registerResponse1 = auth_register("validemail1@gmail.com", "validpassword1", "validname", "validname")
    u_id1 = registerResponse1['u_id']
    token1 = registerResponse1['token']
    channelResponse1 = channels_create(token1, "My Channel", False)
    channel_id1 = channelResponse1['channel_id']
    # SETUP COMPLETE
    with pytest.raises(ValueError):
        channel_invite(token1, channel_id1, 'invalid_id')   # Should NOT work since invalid_id
        channel_invite(token1, channel_id1, ' ')    # Should NOT work since invalid_id
        channel_invite(token1, channel_id1, u_id1) # Should NOT work since User 1 is already an owner of channel

# channel_detail
def test_channel_details_success():
    # SETUP BEGIN
    registerResponse1 = auth_register("validemail1@gmail.com", "validpassword1", "validname1", "validname1")
    u_id1 = registerResponse1['u_id']
    token1 = registerResponse1['token']
    channelResponse1 = channels_create(token1, "My Channel", False)
    channel_id1 = channelResponse1['channel_id']
    # SETUP COMPLETE
    assert channel_details(token1, channel_id1) ==  {'name':'My Channel', 'owner_members':{'u_id':u_id1,'name_first':'validname1','name_last':"validname1"}, 'all_members':{'u_id':u_id1,'name_first':'validname1','name_last':"validname1"}}
    #Should work since user1 is the owner of channel and member of channel

def test_channel_details_Errorcheck1():
    # SETUP BEGIN
    registerResponse1 = auth_register("validemail1@gmail.com", "validpassword1", "validname", "validname")
    u_id1 = registerResponse1['u_id']
    token1 = registerResponse1['token']
    # SETUP COMPLETE
    with pytest.raises(ValueError):
        channel_details(token1,'Noexist_channel_id') #Should NOT work since channel_id does not exist

    
def test_channel_details_Errorcheck2():
    # SETUP BEGIN
    registerResponse1 = auth_register("validemail1@gmail.com", "validpassword1", "validname", "validname")
    u_id1 = registerResponse1['u_id']
    token1 = registerResponse1['token']
    channelResponse1 = channels_create(token1, "My Channel", False)
    channel_id1 = channelResponse1['channel_id']
    registerResponse2 = auth_register("validemail2@gmail.com", "validpassword2", "validname", "validname")
    u_id2 = registerResponse2['u_id']
    token2 = registerResponse2['token']
    channelResponse2 = channels_create(token2, "My Channel1", False)
    channel_id2 = channelResponse2['channel_id']
    # SETUP COMPLETE
    with pytest.raises(AccessError):
        channel_details(token2,'channel_id1') #Should NOT work since user 2 is not a member of channel_id1
        channel_details(token1,'channel_id2') #Should NOT work since user 1 is not a member of channel_id2


def test_channel_details_success_case():
    # SETUP BEGIN
    registerResponse1 = auth_register("validemail1@gmail.com", "validpassword1", "validname1", "validname1")
    u_id1 = registerResponse1['u_id']
    token1 = registerResponse1['token']
    channelResponse1 = channels_create(token1, "My Channel", False)
    channel_id1 = channelResponse1['channel_id']
    registerResponse2 = auth_register("validemail2@gmail.com", "validpassword2", "validname2", "validname2")
    u_id2 = registerResponse2['u_id']
    token2 = registerResponse2['token']
    channel_invite(token1,channel_id1,u_id2)
    # SETUP COMPLETE
    assert channel_details(token1, channel_id1) ==  {'name':'My Channel', 'owner_members':[{'u_id':u_id1,'name_first':'validname1','name_last':"validname1"}], 'all_members':[{'u_id':u_id1,'name_first':'validname1','name_last':"validname1"}]}
    #Should work since user1 is the owner of channel and member of channel
    #user1 invite user2 into channel 
    channel_invite(token1,channel_id1,u_id2)
    assert channel_details(token2, channel_id1) ==  {'name':'My Channel', 'owner_members':[{'u_id':u_id1,'name_first':'validname1','name_last':"validname1"}], 'all_members':[{'u_id':u_id1,'name_first':'validname1','name_last':"validname1"},{'u_id':u_id2,'name_first':'validname2','name_last':"validname2"}]}
    #should work since user2 is the member of channel 

def test_channel_message_success():
    # SETUP BEGIN
    registerResponse1 = auth_register("validemail1@gmail.com", "validpassword1", "validname1", "validname1")
    u_id1 = registerResponse1['u_id']
    token1 = registerResponse1['token']
    channelResponse1 = channels_create(token1, "My Channel", False)
    channel_id1 = channelResponse1['channel_id']
    message_send(token1,channel_id1,'message1')
    # SETUP COMPLETE
    assert channel_message(token1,channel_id1,0) == {['messages'], 0, -1} #should work since channel has 1 message and user1 is a member of channel_id1 
                                                    # change meybe
    

def test_channel_message_Errorcheck1():
    # SETUP BEGIN
    registerResponse1 = auth_register("validemail1@gmail.com", "validpassword1", "validname1", "validname1")
    u_id1 = registerResponse1['u_id']
    token1 = registerResponse1['token']
    channelResponse1 = channels_create(token1, "My Channel", False)
    channel_id1 = channelResponse1['channel_id']
    message_send(token1,channel_id1,'message1')
    messages={'message_id':'','u_id':'','message, time_created':'','is_unread':''}
    # SETUP COMPLETE
    with pytest.raises(ValueError):
        channel_message(token1,'noexit_channel_id',0) #should NOT work since channel_id does not exist
        channel_message(token1,channel_id1,2) #should NOT work since start is greater than the total number of messages in the channel
        channel_message(token1,channel_id1,-1) #should NOT work since start is less than 0

        
def test_channel_message_Errorcheck2():
    # SETUP BEGIN
    registerResponse1 = auth_register("validemail1@gmail.com", "validpassword1", "validname1", "validname1")
    u_id1 = registerResponse1['u_id']
    token1 = registerResponse1['token']
    channelResponse1 = channels_create(token1, "My Channel", False)
    channel_id1 = channelResponse1['channel_id']
    registerResponse2 = auth_register("validemail2@gmail.com", "validpassword2", "validname2", "validname2")
    u_id2 = registerResponse2['u_id']
    token2 = registerResponse2['token']
    # SETUP COMPLETE
    with pytest.raises(AccessError):
        channel_message(token2,channel_id1,0) #should NOT work since user2 is not a member of channel_id1


def test_channel_leave_success():
    # SETUP BEGIN
    registerResponse1 = auth_register("validemail1@gmail.com", "validpassword1", "validname1", "validname1")
    u_id1 = registerResponse1['u_id']
    token1 = registerResponse1['token']
    channelResponse1 = channels_create(token1, "My Channel", False)
    channel_id1 = channelResponse1['channel_id']
    # SETUP COMPLETE
    assert channel_leave(token1,channel_id1) == {}  #should work since user1 is a member of channel_id1

def test_channel_leave_Errorcheck():
    # SETUP BEGIN
    registerResponse1 = auth_register("validemail1@gmail.com", "validpassword1", "validname1", "validname1")
    u_id1 = registerResponse1['u_id']
    token1 = registerResponse1['token']
    channelResponse1 = channels_create(token1, "My Channel", False)
    channel_id1 = channelResponse1['channel_id']
    # SETUP COMPLETE
    with pytest.raises(ValueError):
        channel_leave(token1,'invaild_channel_id') #should NOT work since channal_id doese not exist 
        # assumption more case later

def test_channel_leave_assumption():
    # SETUP BEGIN
    registerResponse1 = auth_register("validemail1@gmail.com", "validpassword1", "validname1", "validname1")
    u_id1 = registerResponse1['u_id']
    token1 = registerResponse1['token']
    channelResponse1 = channels_create(token1, "My Channel", False)
    channel_id1 = channelResponse1['channel_id']
    registerResponse2 = auth_register("validemail2@gmail.com", "validpassword2", "validname2", "validname2")
    u_id2 = registerResponse2['u_id']
    token2 = registerResponse2['token']
    # SETUP COMPLETE
    with pytest.raises(AccessError):
        channel_leave(token2,channel_id1) #should NOT work since user2 is not a member of channel_id1 


def test_channel_join_success():
    # SETUP BEGIN
    registerResponse1 = auth_register("validemail1@gmail.com", "validpassword1", "validname1", "validname1")
    u_id1 = registerResponse1['u_id']
    token1 = registerResponse1['token']
    channelResponse1 = channels_create(token1, "My Channel", True)
    channel_id1 = channelResponse1['channel_id']
    registerResponse2 = auth_register("validemail2@gmail.com", "validpassword2", "validname2", "validname2")
    u_id2 = registerResponse2['u_id']
    token2 = registerResponse2['token']
    # SETUP COMPLETE
    assert channel_join(token2,channel_id1) == {} # should work since channel is pudlic

def test_channel_join_Errorcheck1():
    # SETUP BEGIN
    registerResponse1 = auth_register("validemail1@gmail.com", "validpassword1", "validname1", "validname1")
    u_id1 = registerResponse1['u_id']
    token1 = registerResponse1['token']
    channelResponse1 = channels_create(token1, "My Channel", True)
    channel_id1 = channelResponse1['channel_id']
    registerResponse2 = auth_register("validemail2@gmail.com", "validpassword2", "validname2", "validname2")
    u_id2 = registerResponse2['u_id']
    token2 = registerResponse2['token']
    # SETUP COMPLETE
    with pytest.raises(ValueError):
        channel_join(token1,'fake_channel_id') #should NOT work since channel id does not exist
        channel_join(token2,'fake_channel_id') #should NOT work since channel id does not exist

def test_channel_join_Errorcheck2():
    # SETUP BEGIN
    registerResponse1 = auth_register("validemail1@gmail.com", "validpassword1", "validname1", "validname1")
    u_id1 = registerResponse1['u_id']
    token1 = registerResponse1['token']
    channelResponse1 = channels_create(token1, "My Channel", False)
    channel_id1 = channelResponse1['channel_id']
    registerResponse2 = auth_register("validemail2@gmail.com", "validpassword2", "validname2", "validname2")
    u_id2 = registerResponse2['u_id']
    token2 = registerResponse2['token']
    # SETUP COMPLETE
    with pytest.raises(AccessError):
        channel_join(token2,channel_id1) #should NOT work since channel is private and user2 is not a admin
        
def test_channel_join_assumption():
    # SETUP BEGIN
    registerResponse1 = auth_register("validemail1@gmail.com", "validpassword1", "validname1", "validname1")
    u_id1 = registerResponse1['u_id']
    token1 = registerResponse1['token']
    channelResponse1 = channels_create(token1, "My Channel", False)
    channel_id1 = channelResponse1['channel_id']
    registerResponse2 = auth_register("validemail2@gmail.com", "validpassword2", "validname2", "validname2")
    u_id2 = registerResponse2['u_id']
    token2 = registerResponse2['token']
    # SETUP COMPLETE
    with pytest.raises(ValueError):
        channel_join(token1,channel_id1) #should NOT work since user already a member of channel

def test_channel_join_success_case():
    # SETUP BEGIN
    registerResponse1 = auth_register("validemail1@gmail.com", "validpassword1", "validname1", "validname1")
    u_id1 = registerResponse1['u_id']
    token1 = registerResponse1['token']
    channelResponse1 = channels_create(token1, "My Channel", False)
    channel_id1 = channelResponse1['channel_id']
    registerResponse2 = auth_register("validemail2@gmail.com", "validpassword2", "validname2", "validname2")
    u_id2 = registerResponse2['u_id']
    token2 = registerResponse2['token']
    # SETUP COMPLETE
    admin_userpermission_change(token2,u_id2,'permission_id')
    channel_join(token2,channel_id1) #should work since user2 is a admin
    

def test_channel_addowner_success():
    # SETUP BEGIN
    registerResponse1 = auth_register("validemail1@gmail.com", "validpassword1", "validname1", "validname1")
    u_id1 = registerResponse1['u_id']
    token1 = registerResponse1['token']
    channelResponse1 = channels_create(token1, "My Channel", False)
    channel_id1 = channelResponse1['channel_id']
    registerResponse2 = auth_register("validemail2@gmail.com", "validpassword2", "validname2", "validname2")
    u_id2 = registerResponse2['u_id']
    token2 = registerResponse2['token']
    # SETUP COMPLETE
    assert channel_addowner(token1,channel_id1,u_id2) == {}# Should work since User 2 is not an owner

def test_channel_addowner_Errorcheck1():
    # SETUP BEGIN
    registerResponse1 = auth_register("validemail1@gmail.com", "validpassword1", "validname1", "validname1")
    u_id1 = registerResponse1['u_id']
    token1 = registerResponse1['token']
    channelResponse1 = channels_create(token1, "My Channel", False)
    channel_id1 = channelResponse1['channel_id']
    registerResponse2 = auth_register("validemail2@gmail.com", "validpassword2", "validname2", "validname2")
    u_id2 = registerResponse2['u_id']
    token2 = registerResponse2['token']
    channel_addowner(token1,channel_id1,u_id2)
    # SETUP COMPLETE
    with pytest.raises(ValueError):
        channel_addowner(token1,'noexist_channal_id',u_id2) #should NOT work since channel_id not exist
        channel_addowner(token1,channel_id1,u_id1)  #should NOT work since user1 already an owner of it
        channel_addowner(token1,channel_id1,u_id2)  #should NOT work since user2 already an owner of it

def test_channel_addowner_Errorcheck2():
    # SETUP BEGIN
    registerResponse1 = auth_register("validemail1@gmail.com", "validpassword1", "validname1", "validname1")
    u_id1 = registerResponse1['u_id']
    token1 = registerResponse1['token']
    channelResponse1 = channels_create(token1, "My Channel", False)
    channel_id1 = channelResponse1['channel_id']
    registerResponse2 = auth_register("validemail2@gmail.com", "validpassword2", "validname2", "validname2")
    u_id2 = registerResponse2['u_id']
    token2 = registerResponse2['token']
    channel_addowner(token1,channel_id1,u_id2)
    # SETUP COMPLETE
    with pytest.raises(AccessError):
        channel_addowner(token2,channel_id1,u_id2)  #should not work since user2 is not the owner of channel
        channel_addowner(token2,channel_id1,u_id1)  #should not work since user2 is not the owner of channel

def test_channel_addowner_assumption():
    # SETUP BEGIN
    registerResponse1 = auth_register("validemail1@gmail.com", "validpassword1", "validname1", "validname1")
    u_id1 = registerResponse1['u_id']
    token1 = registerResponse1['token']
    channelResponse1 = channels_create(token1, "My Channel", False)
    channel_id1 = channelResponse1['channel_id']
    registerResponse2 = auth_register("validemail2@gmail.com", "validpassword2", "validname2", "validname2")
    u_id2 = registerResponse2['u_id']
    token2 = registerResponse2['token']
    channel_addowner(token1,channel_id1,u_id2)
    # SETUP COMPLETE
    with pytest.raises(ValueError):
        channel_addowner(token1,channel_id1,'invaild_u_id') #should NOT work since u_id invaild


def test_channel_removeowner_success():
    # SETUP BEGIN
    registerResponse1 = auth_register("validemail1@gmail.com", "validpassword1", "validname1", "validname1")
    u_id1 = registerResponse1['u_id']
    token1 = registerResponse1['token']
    channelResponse1 = channels_create(token1, "My Channel", False)
    channel_id1 = channelResponse1['channel_id']
    registerResponse2 = auth_register("validemail2@gmail.com", "validpassword2", "validname2", "validname2")
    u_id2 = registerResponse2['u_id']
    token2 = registerResponse2['token']
    channel_addowner(token1,channel_id1,u_id2)
    # SETUP COMPLETE
    assert channel_removeowner(token1,channel_id1,u_id2) == {}  #should work since user2 is a owner of channel
    assert channel_removeowner(token1,channel_id1,u_id1) == {} #should work since user2 is a owner of channel

def test_channel_removeowner_Errorcheck1():
    # SETUP BEGIN
    registerResponse1 = auth_register("validemail1@gmail.com", "validpassword1", "validname1", "validname1")
    u_id1 = registerResponse1['u_id']
    token1 = registerResponse1['token']
    channelResponse1 = channels_create(token1, "My Channel", False)
    channel_id1 = channelResponse1['channel_id']
    registerResponse2 = auth_register("validemail2@gmail.com", "validpassword2", "validname2", "validname2")
    u_id2 = registerResponse2['u_id']
    token2 = registerResponse2['token']
    channel_addowner(token1,channel_id1,u_id2)
    registerResponse3 = auth_register("validemail3@gmail.com", "validpassword3", "validname3", "validname3")
    u_id3 = registerResponse3['u_id']
    token3 = registerResponse3['token']
    # SETUP COMPLETE
    with pytest.raises(ValueError):
        channel_removeowner(token1,'noexist_channel_id',u_id1)  #should NOT work since channel_id not exist
        channel_removeowner(token1,channel_id1,u_id3)   #should NOT work since user3 is not a owner of channel
        
def test_channel_removeowner_Errorcheck2():
    # SETUP BEGIN
    registerResponse1 = auth_register("validemail1@gmail.com", "validpassword1", "validname1", "validname1")
    u_id1 = registerResponse1['u_id']
    token1 = registerResponse1['token']
    channelResponse1 = channels_create(token1, "My Channel", False)
    channel_id1 = channelResponse1['channel_id']
    registerResponse2 = auth_register("validemail2@gmail.com", "validpassword2", "validname2", "validname2")
    u_id2 = registerResponse2['u_id']
    token2 = registerResponse2['token']
    channel_addowner(token1,channel_id1,u_id2)
    registerResponse3 = auth_register("validemail3@gmail.com", "validpassword3", "validname3", "validname3")
    u_id3 = registerResponse3['u_id']
    token3 = registerResponse3['token']
    # SETUP COMPLETE
    with pytest.raises(AccessError):
        channel_removeowner(token3,channel_id1,u_id1)  #should not work since user3 is not the owner of channel
        channel_removeowner(token3,channel_id1,u_id2)    #should not work since user3 is not the owner of channel


def test_channels_list_success():
    # SETUP BEGIN
    registerResponse1 = auth_register("validemail1@gmail.com", "validpassword1", "validname1", "validname1")
    u_id1 = registerResponse1['u_id']
    token1 = registerResponse1['token']
    channelResponse1 = channels_create(token1, "My Channel", False)
    channel_id1 = channelResponse1['channel_id']
    registerResponse2 = auth_register("validemail2@gmail.com", "validpassword2", "validname2", "validname2")
    u_id2 = registerResponse2['u_id']
    token2 = registerResponse2['token']
    channel_addowner(token1,channel_id1,u_id2)
    registerResponse3 = auth_register("validemail3@gmail.com", "validpassword3", "validname3", "validname3")
    u_id3 = registerResponse3['u_id']
    token3 = registerResponse3['token']
    # SETUP COMPLETE
    channels_list(token2) == {'channel1,2'}
    channels_list(token1) == {'channel1'}
    channels_list(token3) == {}

####ADDMORE MAYBE

def test_channels_listall_success():
    # SETUP BEGIN
    registerResponse1 = auth_register("validemail1@gmail.com", "validpassword1", "validname1", "validname1")
    u_id1 = registerResponse1['u_id']
    token1 = registerResponse1['token']
    channelResponse1 = channels_create(token1, "My Channel", False)
    channel_id1 = channelResponse1['channel_id']
    registerResponse2 = auth_register("validemail2@gmail.com", "validpassword2", "validname2", "validname2")
    u_id2 = registerResponse2['u_id']
    token2 = registerResponse2['token']
    channel_addowner(token1,channel_id1,u_id2)
    registerResponse3 = auth_register("validemail3@gmail.com", "validpassword3", "validname3", "validname3")
    u_id3 = registerResponse3['u_id']
    token3 = registerResponse3['token']
    # SETUP COMPLETE
    assert channels_list(token2) == channels_listall(token1)
    assert channels_list(token2) == channels_listall(token3)

#ADD MORE MAYBE
def test_channels_create_success():
    # SETUP BEGIN
    registerResponse1 = auth_register("validemail1@gmail.com", "validpassword1", "validname1", "validname1")
    u_id1 = registerResponse1['u_id']
    token1 = registerResponse1['token']
    # SETUP COMPLETE
    channels_create(token1,'channel_name', True)#should work since everything is fine
    channels_create(token1,'channel_name1', False)#should work since everything is fine

def test_channels_create_Errorcheck():
    # SETUP BEGIN
    registerResponse1 = auth_register("validemail1@gmail.com", "validpassword1", "validname1", "validname1")
    u_id1 = registerResponse1['u_id']
    token1 = registerResponse1['token']
    # SETUP COMPLETE
    with pytest.raises(ValueError):
        channels_create(token1,'channel_name'*11, True) #should not work since channel name biger than 20
        channels_create(token1,'c'*20, True) #should not work since channel name biger than 20

def test_channels_create_assumption():
    # SETUP BEGIN
    registerResponse1 = auth_register("validemail1@gmail.com", "validpassword1", "validname1", "validname1")
    u_id1 = registerResponse1['u_id']
    token1 = registerResponse1['token']
    channelResponse1 = channels_create(token1, "My Channel", False)
    channel_id1 = channelResponse1['channel_id']
    # SETUP COMPLETE
    with pytest.raises(ValueError):
        channels_create(token1,' ', True)   #should not work since channel name is empty
        channels_create(token1,'!@#$%^', True)  #should not work since channel name contain !@#$%^
        channels_create(token1, "My Channel", False) #should not work since  another same channel name 
