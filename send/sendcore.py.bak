# -*- coding:gb2312 -*-  
import pyperclip
import time
import random
from send.sendapis import *
from core.debug import *

def sendcorekey():
	key_press(0x1C) #ENTER
	time.sleep(0.1)
	key_down(0x1D) #CTRL
	time.sleep(0.1)
	key_down(0x2F) #V
	time.sleep(0.1)
	key_up(0x1D) #CTRL
	time.sleep(0.1)
	key_up(0x2F) #V
	time.sleep(0.1)
	key_press(0x1C) #ENTER
	time.sleep(0.1)
	key_down(0x1D) #CTRL
	time.sleep(0.1)
	key_down(0x2F) #V
	time.sleep(0.1)
	key_up(0x1D) #CTRL
	time.sleep(0.1)
	key_up(0x2F) #V
	time.sleep(0.1)
	key_press(0x1C) #ENTER	

def sendstr(talkto,strs):
	debug("SendStr( "+talkto+" ): " + strs,1)
	sendcache = "/w "+talkto+" "+strs
	pyperclip.copy(sendcache)
	sendcorekey()
	
	
def sendlist(talkto,lists,pauserandom,pausefrom,pauseto):
	#pauserandom : 0 for non-random, use pausefrom
	#              1 for random, from --> to
	pausetime = 0
	if pauserandom ==0:
		pausetime = pausefrom
	else:
		pausetime = random.uniform(0.5,1)
	for i in lists:
		time.sleep(pausetime)
		sendstr(talkto,i)