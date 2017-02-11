# -*- coding:gbk -*-  
import win32api


DEBUGNAME = "debug.txt" #�����ļ������
INT_GLOBAL_WAITING = 0.5 #ÿ�β�����ȴ�ʱ��


#�����ģʽ����
INT_ANTI_SCAN = 1 #������ܿ��� 1 = ��
FLOAT_WAITING_RANDOM_LOWER = 0.1 #����ȴ�ʱ������
FLOAT_WAITING_RANDOM_UPPER = 0.3 #����ȴ�ʱ������

#��¼ģ�����λ������
TUPLE_LOGIN_USERNAME = (951/1920,484/1080)
TUPLE_LOGIN_PWD = (957/1920,526/1080)
TUPLE_LOGIN_OK = (1051/1920,595/1080)
TUPLE_LOGIN_CONFIRM_LOCATION = (66/1920,1007/1080) #���½���ɽ�Ӱ�ɫ��־�������ʧ(��(255,255,255))��ζ�Ž��롰��ɫѡ��ҳ�桱
TUPLE_LOGIN_CONFRIM_PIXEL = (255,255,255)
TUPLE_LOGIN_SUCCESS_LOCATION = (29/1920,1033/1080) #���½ǵ�½�ɹ�������λ���
TUPLE_LOGIN_SUCCESS_PIXEL = (9,59,57) #���½ǵ�½�ɹ�������λ���

TUPLE_LOGIN_HOTSPAM_LOCATION = (1395/1920,276/1080)
TUPLE_LOGIN_HOTSPAM_PIXEL = (64,90,86)

TUPLE_MAIL_NEW_LOCATION = (1702/1920,148/1080)
TUPLE_MAIL_NEW_PIXEL = (219,212,192)

#������ģ��
TUPLE_TRADER_DIALOG = (272/1920,254/1080) #�����жԻ�����������
TUPLE_TRADER_ITEMINPUT = (88/1920,273/1080) #��������Ʒ�����
TUPLE_TRADER_QUERYBUTTON = (62/1920,215/1080) #"����"��ҳ��ť
TUPLE_TRADER_SELLBUTTON = (285/1920,214/1080) #"����"��ҳ��ť
TUPLE_TRADER_SEARCHBUTTON = (714/1920,274/1080) #������ť
TUPLE_TRADER_ITEMICON_LEFTTOP (25/1920,271/1080) #��Ʒͼ�����Ͻ�
TUPLE_TRADER_ITEMICON_RIGHTDOWN (58/1920,304/1080) #��Ʒͼ�����½�
TUPLE_TRADER_ITEM_ZHUAN (40/1920,429/1080) #��Ʒ����ש������
TUPLE_TRADER_ITEM_JIN (94/1920,427/1080) #��Ʒ���۽�������
TUPLE_TRADER_ITEM_YIN (146/1920,429/1080) #��Ʒ������������

#����
TUPLE_BAG1_START = (1164/1920,236/1080)  ###��һ�����ʼ�����ֶ��޸ġ�
TUPLE_BAG_NEXT = (38/1920,38/1080) #�����ڸ��ӵ�λ��



#�����λ��ת��Ϊ����λ��
class util():
	Screen_X = 0
	Screen_Y = 0
	def __init__(self):
		self.Screen_X =  win32api.GetSystemMetrics(0)
		self.Screen_Y = win32api.GetSystemMetrics(1)
	def GetIntTuple(self,value):
		return tuple((int(value[0]* self.Screen_X),int(value[1] * self.Screen_Y)))
	def CompareTuple(self,x,y,sensitive = 20):
		#�Ƚ��������ص�������ԣ�����ǳ����ƣ���֮��<20������1
		xsum = 0
		ysum = 0
		for i in x:
			xsum += i
		for j in y:
			ysum += j
		if abs(xsum-ysum)<sensitive:
			return True
		else:
			return False

