import send.sendmail
import settings
import time
import sys

def debug(strs,level = '普通'):
	f = open(settings.DEBUGNAME,'a')
	f.write(time.ctime()+"["+level+"]: "+str(sys._getframe().f_code.co_name) +" "+strs.strip("\n")+"\n")
	f.close()

def raiseError(strs,level = 0):
	if level==0:
		debug(strs,"严重")
	else:
		debug(strs,"严重且发信")
		send.sendmail.send("剑网三交易行程序严重错误",strs)