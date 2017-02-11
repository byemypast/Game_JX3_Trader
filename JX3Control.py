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
		if settings.INT_ANTI_SCAN ==1:#�����ģʽ
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
		#user:�û���
		#pwd:����
		#wait:Ĭ�ϵ�½��ȴ�ʱ�䣬��ʱ����û���жϵ���־����Ϊ��¼ʧ��:45��
		debug("��ʼ��¼ģ�飬�˺� = "+user+" ����=len("+str(len(pwd))+'),��ʱ����Ϊ: '+str(wait)+"s.")
		self.control.ClickMouse(self.util.GetIntTuple(settings.TUPLE_LOGIN_USERNAME))
		self.control.Waiting()
		send.sendcore.ctrla() #��������˺���Ϣ
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
			#���½���ɽ�Ӱ�ɫһֱ�У���¼ʧ��
			raiseError("��¼ʧ�ܣ��˺ŵ�¼������ʱ���ܷ��سɹ���־���뾡��鿴����״̬�������ѵ㿨��",1)
			self.control.PressESC()
			return -1
		debug("�˺ŵ�¼�ɹ�����ʼ���Ե�һ��ɫ��¼")
		self.control.Waiting()
		self.control.PressEnter() #�س����Ե�һ��ɫ��¼
		i = 0
		while (self.util.CompareTuple(self.control.GetScreenPixel(self.util.GetIntTuple(settings.TUPLE_LOGIN_SUCCESS_LOCATION)) , settings.TUPLE_LOGIN_SUCCESS_PIXEL) == False) and(i<=wait):
			i += 1
			time.sleep(1)
		if i > wait:
			#���½ǻ���һֱû�У���½ʧ��
			raiseError("��¼ʧ�ܣ���ɫ��¼����Ϸ������ʱ���ܷ��سɹ���־���뾡��鿴����״̬�������ѵ㿨��",1)
			self.control.PressESC()
			return -1
		debug("��ɫ��¼�ɹ���")

		#�رճ������ҳ��
		if (self.util.CompareTuple(self.control.GetScreenPixel(self.util.GetIntTuple(settings.TUPLE_LOGIN_HOTSPAM_LOCATION)) , settings.TUPLE_LOGIN_HOTSPAM_PIXEL)) == True:
			debug("��⵽�ȵ��洰�ڣ����Թر�")
			self.control.ClickMouse(self.util.GetIntTuple(settings.TUPLE_LOGIN_CONFIRM_LOCATION))
		else:
			debug("δ��⵽�ȵ��洰��")
		self.control.ClickMouse(self.util.GetIntTuple(settings.TUPLE_LOGIN_SUCCESS_LOCATION)) #���㴰��
		return 1
	def logout(self,wait=45):
		#���ԣ�ֱ��ʹ�ÿ�ݼ��ǳ���������ΪCtrl + W
		debug("��ʼ�ǳ�ģ�飬��ʱʱ��: "+str(wait)+"s.")
		send.sendcore.ctrlw()
		i = 0
		while (self.util.CompareTuple(self.control.GetScreenPixel(self.util.GetIntTuple(settings.TUPLE_LOGIN_CONFIRM_LOCATION)) , settings.TUPLE_LOGIN_CONFRIM_PIXEL)== False) and(i<=wait):
			i += 1
			time.sleep(1)
		if i > wait:
			raiseError("�ǳ�ʧ�ܣ��뾡��鿴����״̬�������ѵ㿨��",1)
			return -1
		debug("�˺ŵǳ��ɹ���")