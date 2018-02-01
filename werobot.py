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

def sendmess(mess):
    mm=itchat.search_chatrooms(name=u'研究中心')
    nn=mm[0]['HeadImgUrl']
    pattern=re.compile('username=(@+\S*)&skey')
    username=pattern.findall(nn)

    itchat.send(mess,username[0])

