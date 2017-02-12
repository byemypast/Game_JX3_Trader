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
		self.PressCtrlV()
		self.Waiting()
		self.PressEnter()
	def GetScreenPixel(self,xy):
		screen = ImageGrab.grab().getpixel(xy)
		return screen
	def PressEnter(self):
		send.sendcore.key_press(0x1C)
	def PressESC(self):
		send.sendcore.key_press(0x01)
	def PressBACK(self):
		send.sendcore.key_press(0x0E)
	def PressF(self):
		send.sendcore.key_press(0x21)
	def PressCtrlXX(self,key):
		#Scancodes references : https://www.win.tue.nl/~aeb/linux/kbd/scancodes-1.html
		send.sendcore.key_down(0x1D) #CTRL
		time.sleep(0.1)
		send.sendcore.key_down(key) #key
		time.sleep(0.1)
		send.sendcore.key_up(0x1D) #CTRL
		time.sleep(0.1)
		send.sendcore.key_up(key) #key
		time.sleep(0.1)
	def PressCtrlA(self):
		self.PressCtrlXX(0x1E)
	def PressCtrlW(self):
		self.PressCtrlXX(0x11)
	def PressCtrlV(self):
		self.PressCtrlXX(0x2F)



class JX3Action(object):
	control = None
	util = None
	TraderWindow = False
	TraderPage = ''
	def __init__(self):
		self.control = JX3Control()
		self.util = settings.util()
		self.TraderWindow = False
		self.TraderPage = ''

	def login(self,user,pwd,wait=45):
		#user:用户名
		#pwd:密码
		#wait:默认登陆后等待时间，超时若仍没有判断到标志则认为登录失败:45秒
		debug("开始登录模块，账号 = "+user+" 密码=len("+str(len(pwd))+'),超时设置为: '+str(wait)+"s.")
		self.control.ClickMouse(self.util.GetIntTuple(settings.TUPLE_LOGIN_USERNAME))
		self.control.Waiting()
		self.control.PressCtrlA() #清除已有账号信息
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
		self.control.PressCtrlW()
		i = 0
		while (self.util.CompareTuple(self.control.GetScreenPixel(self.util.GetIntTuple(settings.TUPLE_LOGIN_CONFIRM_LOCATION)) , settings.TUPLE_LOGIN_CONFRIM_PIXEL)== False) and(i<=wait):
			i += 1
			time.sleep(1)
		if i > wait:
			raiseError("登出失败！请尽快查看程序状态避免消费点卡！",1)
			return -1
		debug("账号登出成功！")
	def openTrader(self,wait=10):
		if self.TraderPage==True:
			debug("重复打开交易行！",'错误')
			return
		debug("尝试打开交易行")
		self.control.PressF()
		self.control.Waiting()
		self.control.ClickMouse(settings.util.GetIntTuple(settings.TUPLE_TRADER_DIALOG))
		i = 0
		while(i<=wait)and(self.util.CompareTuple(self.control.GetScreenPixel(self.util.GetIntTuple(settings.TUPLE_TRADER_OPENEDPOS)),settings.TUPLE_TRADER_OPENEDPIX)==False):
			time.sleep(1)
			i += 1
		if i>wait:
			debug("交易行打开失败！请检查设置","严重")
			self.TraderWindow = False
		else:
			debug("交易行打开成功！")
			self.TraderPage = '买卖'
			self.TraderWindow = True
	def TraderTurnPage(self):
		if self.TraderPage == '买卖':
			debug("切换交易页面： 买卖-->寄售")
			self.control.ClickMouse(settings.util.GetIntTuple(settings.TUPLE_TRADER_SELLBUTTON))
			self.control.Waiting()
			self.TraderPage == '寄售'
		else:
			debug("切换交易页面： 寄售-->买卖")
			self.control.ClickMouse(settings.util.GetIntTuple(settings.TUPLE_TRADER_QUERYBUTTON))
			self.TraderPage == '买卖'
	def TraderSearchWithoutOCR(self,ItemName,BagBase,BagPosition):
		#使用非OCR的方式查询游戏物品的价格
		#流程：首先在买卖页面搜索物品，由交易行插件记录价格
		#      再在寄卖页面拟卖出该物品，在价格一栏中复制当前该物品的价格
		#      这个方法要求背包里必须拥有该物品
		#      考虑到背包界面、不同包裹起始位置在每个客户端位置、不同角色背包数量、大小在不同角色不同，要求设定背包在屏幕中的位置。
		#ItemName: 物品名称 BagBase: 背包基量。为一个二维元组（包裹起始基量，增量） BagPosition: 背包位置，为一个二维元组（行，列）。从0开始
		if self.TraderPage == '寄售':
			self.TraderTurnPage()
			self.control.Waiting()
			self.control.ClickMouse(