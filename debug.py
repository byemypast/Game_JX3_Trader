import send.sendmail
import settings
import time
import inspect

def debug(strs,level = '普通'):
	try:
		strs = str(strs)
		f = open(settings.DEBUGNAME,'a')
		f.write(time.ctime()+"["+level+"]: "+str(inspect.stack()[1][3]) +" "+strs.strip("\n")+"\n")
		f.close()
	except Exception as err:
		print("debug输出错误！原因："+str(err))

def raiseError(strs,level = 0):
	if level==0:
		debug(strs,"严重")
	else:
		debug(strs,"严重且发信")
		send.sendmail.send("剑网三交易行程序严重错误",strs)