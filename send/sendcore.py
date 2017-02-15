# -*- coding:utf-8 -*-  
import pyperclip
import time
from send.sendapis import *

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

