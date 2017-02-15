# -*- coding:utf-8 -*-  
#私有库
import send.sendapis
import send.sendcore
import settings
import settings_pwd
from debug import *
#公用库
import time
import random
import os
import re
import sqlite3
#第三方库
from PIL import ImageGrab
import pyperclip
import win32api
import win32con


class JX3Control(object):
	conn = None
	def __init__(self):
		self.conn = sqlite3.connect(settings.ITEMSIDDB_FILENAME)
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
	def GetItemInfo(self,strItemID):
		try:
			res = self.conn.execute("SELECT name,category from item where uid = "+strItemID).fetchall()
			return res[0]
		except Exception as err:
			debug("执行数据库指令失败：SELECT name,category from item where uid = "+strItemID+", 原因： "+ str(err))
			return
	def KillFile(self,filename):
		try:
			os.remove(filename)
		except Exception as err:
			debug("删除文件错误！文件： "+ filename + " 错误信息："+str(err),'警告')
	def ClearData(self):
		self.PressCtrlA()
		self.Waiting()
		self.PressBACK()




class JX3Action(object):
	control = None
	util = None
	TraderWindow = False
	TraderPage = ''
	loginmode = ''
	def __init__(self):
		self.control = JX3Control()
		self.util = settings.util()
		self.TraderWindow = False
		self.TraderPage = ''
		self.loginmode = '下线'

	def login(self,user = settings_pwd.USERNAME,pwd = settings_pwd.PASSWORD,wait=45):
		#user:用户名
		#pwd:密码
		#wait:默认登陆后等待时间，超时若仍没有判断到标志则认为登录失败:45秒
		self.control.KillFile(settings.AHRECORD_FILENAME) #上线前先删除AH插件记录
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
		self.loginmode = '上线'
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
		self.loginmode = '下线'
	def openTrader(self,wait=10):
		if self.TraderPage==True:
			debug("重复打开交易行！",'错误')
			return
		debug("尝试打开交易行")
		self.control.PressF()
		self.control.Waiting()
		self.control.ClickMouse(self.util.GetIntTuple(settings.TUPLE_TRADER_DIALOG))
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

	def TraderSearchWithoutOCR_Online(self,waittime = 40):
		#使用非OCR的方式查询游戏物品的价格
		#流程：首先在买卖页面搜索物品，由AH插件记录价格
		#      下线后从AH插件记录中读到价格
		#      缺点：只能记录最低价，不能记录存量
		debug("交易行询价开始")
		ItemList = self._TraderMakeList()
		if self.TraderPage == '寄售':
			self._TraderTurnPage()
			self.control.Waiting()
		for ItemName in ItemList:
			self.control.ClickMouse(self.util.GetIntTuple(settings.TUPLE_TRADER_ITEMINPUT))
			self.control.ClearData()
			self.control.ClickMouse(self.util.GetIntTuple(settings.TUPLE_TRADER_ITEMINPUT))
			self.control.ClickMouse(self.util.GetIntTuple(settings.TUPLE_TRADER_ITEMINPUT))
			self.control.InputData(ItemName)
			i = 0
			while (i<=waittime)and(self.util.CompareTuple(self.control.GetScreenPixel(self.util.GetIntTuple(settings.TUPLE_TRADER_SEARCHBUTTON)), settings.TUPLE_TRADER_SEARCHBUTTON_GRAY)==True):
				i+=0.5
				#print(self.control.GetScreenPixel(self.util.GetIntTuple(settings.TUPLE_TRADER_SEARCHBUTTON)), settings.TUPLE_TRADER_SEARCHBUTTON_GRAY,self.util.CompareTuple(self.control.GetScreenPixel(self.util.GetIntTuple(settings.TUPLE_TRADER_SEARCHBUTTON)), settings.TUPLE_TRADER_SEARCHBUTTON_GRAY))
				self.control.Waiting(0.5)
			if i>waittime:
				debug("交易行询价超时！物品 = " +ItemName +", 时间 = " + str(waittime),'错误')
				return
			else:
				debug("交易行询价成功！物品 = "+ItemName)
	def TraderSearchWithoutOCR_Offline(self):
		result = []
		#从AH插件的记录中找到上次的查询记录，并删除该文件待下次查询
		debug("尝试从AH插件读取询价")
		if self.loginmode =='上线':
			debug("游戏未下线，询价错误",'错误')
			return
		if os.path.exists(settings.AHRECORD_FILENAME) == False:
			debug("找不到AH插件记录！",'错误')
			return
		if os.path.exists(settings.ITEMSIDDB_FILENAME) ==False:
			debug("找不到物品ID库！",'错误')
			return
		ahfile = open(settings.AHRECORD_FILENAME,'rb')
		ahheader = ahfile.read(16) #AH记录头16字节为头文件
		ahrecord = ahfile.read().decode()
		query = re.compile('\[(.*?)\]=\{\[1\]=\{\[\"nGold\"\]=(.*?),\[\"nSilver\"\]=(.*?),\[\"nCopper\"\]=(.*?),},\[2\]=(.*?),},')
		for ID,GPrice,SPrice,CPrice,Timestamp in query.findall(ahrecord):
			try:
				Name,Category = self.control.GetItemInfo(str(ID))
				result.append((Name,Category,GPrice,SPrice,CPrice,time.ctime(int(Timestamp))))
			except Exception as err:
				debug("询价函数试图查询不存在的ID : " +str(ID)+" 错误信息：" +str(err),"警告")
		ahfile.close()
		#self.control.KillFile(settings.AHRECORD_FILENAME) #删除AH插件查询的过期记录
		debug("读取询价成功！")
		return result

	def _TraderMakeList(self):
		#维护欲询价物品的list
		makelist = []
		for line in open(settings.QUERYITEM_FILENAME):
			info = line.strip().split("\t")[0]
			if info!='':
				makelist.append(info)
		for line in open(settings.IGNOREITEM_FILENAME):
			info = line.strip().split(" ")[0]
			if (info!='')and (info in makelist):
				makelist.remove(info)
		return makelist
	def _TraderTurnPage(self):
		if self.TraderPage == '买卖':
			debug("切换交易页面： 买卖-->寄售")
			self.control.ClickMouse(settings.util.GetIntTuple(settings.TUPLE_TRADER_SELLBUTTON))
			self.control.Waiting()
			self.TraderPage == '寄售'
		else:
			debug("切换交易页面： 寄售-->买卖")
			self.control.ClickMouse(settings.util.GetIntTuple(settings.TUPLE_TRADER_QUERYBUTTON))
			self.TraderPage == '买卖'

