#coding:utf-8;
#

#creator: tongy
#collaborators: fengx, cuidongd
#
#Script send messages to wecchat rooms automatically

#----------------------------------------------------
#Imports
import re
import itchat
#----------------------------------------------------

itchat.auto_login(enableCmdQR=True,hotReload=True)

room_info=itchat.search_chatrooms(name=u'研究中心')
head_info=room_info[0]['HeadImgUrl']
#Matching to get username
pattern=re.compile('username=(@+\S*)&skey')
username=pattern.findall(head_info)

itchat.send(u'测试成功',username[0])