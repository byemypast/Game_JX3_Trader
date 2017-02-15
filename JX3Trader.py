# -*- coding:gbk -*-  
import JX3Control
import JX3Save
import time
import settings
from debug import *

def TraderRecord(gameOBJ):
	gameOBJ.login()
	time.sleep(1)
	gameOBJ.openTrader()
	time.sleep(1)
	gameOBJ.TraderSearchWithoutOCR_Online()
	time.sleep(1)
	gameOBJ.logout()
	return gameOBJ.TraderSearchWithoutOCR_Offline()


#һ��ִ�г����������������ļ��ȡ���������úÿɲ���ִ�С�
import Onetime
Onetime.RecipeToItem() #���䷽ϵ��ת��Ϊѯ���ļ�

#DEF
GameControl = JX3Control.JX3Action()
SaveControl = JX3Save.JX3Save()

lasttime = 0
time.sleep(10)
while True:
	if (time.time()-lasttime)>settings.INT_RECORDPRICE:
		debug("��ʱ���񴥷���������� = "+str(settings.INT_RECORDPRICE))
		lasttime = time.time()
		#---------------����ʼ----------------
		PriceList = TraderRecord(GameControl) #ִ�е�¼ѭ��
		SaveControl.updateLib(PriceList) #����
		#---------------�������----------------
	time.sleep(1)


