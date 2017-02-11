# -*- coding:gbk -*-  
import send.sendapis
import send.sendcore
from debug import *
import pyperclip
import time
import random
import win32api
import win32con
import settings
import settings_pwd
from PIL import ImageGrab

class JX3Control(object):
	def __init__(self):
		pass
	def SetClipData(self,strs):
		pyperclip.copy(strs)
	def GetClipData(self):
		return pyperclip.paste()
	def MoveMouse(self,xy):
		win32api.SetCursorPos(xy)
	def GetMouse(self,xy):
		return win32api.GetCursorPos(xy)
	def Waiting(self,waittime = settings.INT_GLOBAL_WAITING):
		if settings.INT_ANTI_SCAN ==1:#反侦查模式
			waittime += random.uniform(settings.FLOAT_WAITING_RANDOM_LOWER,settings.FLOAT_WAITING_RANDOM_UPPER)
		time.sleep(waittime)
	def ClickMouse(self,xy):
		self.MoveMouse(xy)
		x,y = xy[0],xy[1]
		win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN,x,y,0,0)
		self.Waiting(settings.INT_GLOBAL_WAITING)
		win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP,x,y,0,0)
	def InputData(self,strs):
		self.SetClipData(strs)
		self.Waiting()
		send.sendcore.ctrlventer()
	def GetScreenPixel(self,xy):
		screen = ImageGrab.grab().getpixel(xy)
		return screen
	def PressEnter(self):
		send.sendcore.key_press(0x1C)
	def PressESC(self):
		send.sendcore.key_press(0x01)
	def PressBACK(self):
		send.sendcore.key_press(0x0E)


class JX3Action(object):
	control = None
	util = None
	def __init__(self):
		self.control = JX3Control()
		self.util = settings.util()

	def login(self,user,pwd,wait=45):
		#user:用户名
		#pwd:密码
		#wait:默认登陆后等待时间，超时若仍没有判断到标志则认为登录失败:45秒
		debug("开始登录模块，账号 = "+user+" 密码=len("+str(len(pwd))+'),超时设置为: '+str(wait)+"s.")
		self.control.ClickMouse(self.util.GetIntTuple(settings.TUPLE_LOGIN_USERNAME))
		self.control.Waiting()
		send.sendcore.ctrla() #清除已有账号信息
		self.control.Waiting()
		self.control.PressBACK()

		self.control.InputData(user)
		self.control.Waiting()
		self.control.ClickMouse(self.util.GetIntTuple(settings.TUPLE_LOGIN_PWD))
		self.control.Waiting()
		self.control.InputData(pwd)
		self.control.Waiting()
		self.control.ClickMouse(self.util.GetIntTuple(settings.TUPLE_LOGIN_OK))
		i = 0
		while (self.util.CompareTuple(self.control.GetScreenPixel(self.util.GetIntTuple(settings.TUPLE_LOGIN_CONFIRM_LOCATION)) , settings.TUPLE_LOGIN_CONFRIM_PIXEL) == True)and(i<=wait):
			time.sleep(1)
			i += 1
		if i > wait:
			#左下角西山居白色一直有，登录失败
			raiseError("登录失败，账号登录至界面时不能返回成功标志。请尽快查看程序状态避免消费点卡！",1)
			self.control.PressESC()
			return -1
		debug("账号登录成功！开始尝试第一角色登录")
		self.control.Waiting()
		self.control.PressEnter() #回车，以第一角色登录
		i = 0
		while (self.util.CompareTuple(self.control.GetScreenPixel(self.util.GetIntTuple(settings.TUPLE_LOGIN_SUCCESS_LOCATION)) , settings.TUPLE_LOGIN_SUCCESS_PIXEL) == False) and(i<=wait):
			i += 1
			time.sleep(1)
		if i > wait:
			#左下角花纹一直没有，登陆失败
			raiseError("登录失败，角色登录至游戏主界面时不能返回成功标志。请尽快查看程序状态避免消费点卡！",1)
			self.control.PressESC()
			return -1
		debug("角色登录成功！")

		#关闭冲销活动等页面
		if (self.util.CompareTuple(self.control.GetScreenPixel(self.util.GetIntTuple(settings.TUPLE_LOGIN_HOTSPAM_LOCATION)) , settings.TUPLE_LOGIN_HOTSPAM_PIXEL)) == True:
			debug("检测到热点广告窗口，尝试关闭")
			self.control.ClickMouse(self.util.GetIntTuple(settings.TUPLE_LOGIN_CONFIRM_LOCATION))
		else:
			debug("未检测到热点广告窗口")
		self.control.ClickMouse(self.util.GetIntTuple(settings.TUPLE_LOGIN_SUCCESS_LOCATION)) #焦点窗口
		return 1
	def logout(self,wait=45):
		#策略：直接使用快捷键登出。请设置为Ctrl + W
		debug("开始登出模块，超时时间: "+str(wait)+"s.")
		send.sendcore.ctrlw()
		i = 0
		while (self.util.CompareTuple(self.control.GetScreenPixel(self.util.GetIntTuple(settings.TUPLE_LOGIN_CONFIRM_LOCATION)) , settings.TUPLE_LOGIN_CONFRIM_PIXEL)== False) and(i<=wait):
			i += 1
			time.sleep(1)
		if i > wait:
			raiseError("登出失败！请尽快查看程序状态避免消费点卡！",1)
			return -1
		debug("账号登出成功！")