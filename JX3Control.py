# -*- coding:gbk -*-  
#˽�п�
import send.sendapis
import send.sendcore
import settings
import settings_pwd
from debug import *
#���ÿ�
import time
import random
import os
import re
import sqlite3
#��������
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
			debug("ִ�����ݿ�ָ��ʧ�ܣ�SELECT name,category from item where uid = "+strItemID+", ԭ�� "+ str(err))
			return
	def KillFile(self,filename):
		try:
			os.remove(filename)
		except Exception as err:
			debug("ɾ���ļ������ļ��� "+ filename + " ������Ϣ��"+str(err),'����')
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
		self.loginmode = '����'

	def login(self,user = settings_pwd.USERNAME,pwd = settings_pwd.PASSWORD,wait=45):
		#user:�û���
		#pwd:����
		#wait:Ĭ�ϵ�½��ȴ�ʱ�䣬��ʱ����û���жϵ���־����Ϊ��¼ʧ��:45��
		self.control.KillFile(settings.AHRECORD_FILENAME) #����ǰ��ɾ��AH�����¼
		debug("��ʼ��¼ģ�飬�˺� = "+user+" ����=len("+str(len(pwd))+'),��ʱ����Ϊ: '+str(wait)+"s.")
		self.control.ClickMouse(self.util.GetIntTuple(settings.TUPLE_LOGIN_USERNAME))
		self.control.Waiting()
		self.control.PressCtrlA() #��������˺���Ϣ
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
		self.loginmode = '����'
		return 1

	def logout(self,wait=45):
		#���ԣ�ֱ��ʹ�ÿ�ݼ��ǳ���������ΪCtrl + W
		debug("��ʼ�ǳ�ģ�飬��ʱʱ��: "+str(wait)+"s.")
		self.control.PressCtrlW()
		i = 0
		while (self.util.CompareTuple(self.control.GetScreenPixel(self.util.GetIntTuple(settings.TUPLE_LOGIN_CONFIRM_LOCATION)) , settings.TUPLE_LOGIN_CONFRIM_PIXEL)== False) and(i<=wait):
			i += 1
			time.sleep(1)
		if i > wait:
			raiseError("�ǳ�ʧ�ܣ��뾡��鿴����״̬�������ѵ㿨��",1)
			return -1
		debug("�˺ŵǳ��ɹ���")
		self.loginmode = '����'
	def openTrader(self,wait=10):
		if self.TraderPage==True:
			debug("�ظ��򿪽����У�",'����')
			return
		debug("���Դ򿪽�����")
		self.control.PressF()
		self.control.Waiting()
		self.control.ClickMouse(self.util.GetIntTuple(settings.TUPLE_TRADER_DIALOG))
		i = 0
		while(i<=wait)and(self.util.CompareTuple(self.control.GetScreenPixel(self.util.GetIntTuple(settings.TUPLE_TRADER_OPENEDPOS)),settings.TUPLE_TRADER_OPENEDPIX)==False):
			time.sleep(1)
			i += 1
		if i>wait:
			debug("�����д�ʧ�ܣ���������","����")
			self.TraderWindow = False
		else:
			debug("�����д򿪳ɹ���")
			self.TraderPage = '����'
			self.TraderWindow = True

	def TraderSearchWithoutOCR_Online(self,waittime = 40):
		#ʹ�÷�OCR�ķ�ʽ��ѯ��Ϸ��Ʒ�ļ۸�
		#���̣�����������ҳ��������Ʒ����AH�����¼�۸�
		#      ���ߺ��AH�����¼�ж����۸�
		#      ȱ�㣺ֻ�ܼ�¼��ͼۣ����ܼ�¼����
		debug("������ѯ�ۿ�ʼ")
		ItemList = self._TraderMakeList()
		if self.TraderPage == '����':
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
				debug("������ѯ�۳�ʱ����Ʒ = " +ItemName +", ʱ�� = " + str(waittime),'����')
				return
			else:
				debug("������ѯ�۳ɹ�����Ʒ = "+ItemName)
	def TraderSearchWithoutOCR_Offline(self):
		result = []
		#��AH����ļ�¼���ҵ��ϴεĲ�ѯ��¼����ɾ�����ļ����´β�ѯ
		debug("���Դ�AH�����ȡѯ��")
		if self.loginmode =='����':
			debug("��Ϸδ���ߣ�ѯ�۴���",'����')
			return
		if os.path.exists(settings.AHRECORD_FILENAME) == False:
			debug("�Ҳ���AH�����¼��",'����')
			return
		if os.path.exists(settings.ITEMSIDDB_FILENAME) ==False:
			debug("�Ҳ�����ƷID�⣡",'����')
			return
		ahfile = open(settings.AHRECORD_FILENAME,'rb')
		ahheader = ahfile.read(16) #AH��¼ͷ16�ֽ�Ϊͷ�ļ�
		ahrecord = ahfile.read().decode()
		query = re.compile('\[(.*?)\]=\{\[1\]=\{\[\"nGold\"\]=(.*?),\[\"nSilver\"\]=(.*?),\[\"nCopper\"\]=(.*?),},\[2\]=(.*?),},')
		for ID,GPrice,SPrice,CPrice,Timestamp in query.findall(ahrecord):
			try:
				Name,Category = self.control.GetItemInfo(str(ID))
				result.append((Name,Category,GPrice,SPrice,CPrice,time.ctime(int(Timestamp))))
			except Exception as err:
				debug("ѯ�ۺ�����ͼ��ѯ�����ڵ�ID : " +str(ID)+" ������Ϣ��" +str(err),"����")
		ahfile.close()
		#self.control.KillFile(settings.AHRECORD_FILENAME) #ɾ��AH�����ѯ�Ĺ��ڼ�¼
		debug("��ȡѯ�۳ɹ���")
		return result

	def _TraderMakeList(self):
		#ά����ѯ����Ʒ��list
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
		if self.TraderPage == '����':
			debug("�л�����ҳ�棺 ����-->����")
			self.control.ClickMouse(settings.util.GetIntTuple(settings.TUPLE_TRADER_SELLBUTTON))
			self.control.Waiting()
			self.TraderPage == '����'
		else:
			debug("�л�����ҳ�棺 ����-->����")
			self.control.ClickMouse(settings.util.GetIntTuple(settings.TUPLE_TRADER_QUERYBUTTON))
			self.TraderPage == '����'