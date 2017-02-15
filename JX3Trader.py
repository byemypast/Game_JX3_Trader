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


#一次执行程序，用于生成配置文件等。如果已配置好可不被执行。
import Onetime
Onetime.RecipeToItem() #将配方系列转化为询价文件

#DEF
GameControl = JX3Control.JX3Action()
SaveControl = JX3Save.JX3Save()

lasttime = 0
time.sleep(10)
while True:
	if (time.time()-lasttime)>settings.INT_RECORDPRICE:
		debug("定时任务触发，间隔秒数 = "+str(settings.INT_RECORDPRICE))
		lasttime = time.time()
		#---------------任务开始----------------
		PriceList = TraderRecord(GameControl) #执行登录循环
		SaveControl.updateLib(PriceList) #保存
		#---------------任务结束----------------
	time.sleep(1)


