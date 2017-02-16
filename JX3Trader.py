# -*- coding:utf-8 -*-  
import JX3Control
import JX3Save
import JX3Analysis
import time
import settings
from debug import *
def TraderRecord(gameOBJ):
	gameOBJ.login()
	time.sleep(10)
	gameOBJ.openTrader()
	time.sleep(1)
	gameOBJ.TraderSearchWithoutOCR_Online()
	time.sleep(1)
	gameOBJ.logout()
	return gameOBJ.TraderSearchWithoutOCR_Offline()

atool = JX3Analysis.JX3AnalysisTool("saverecord.db")
X = ['Thu Feb 16 17:02:45 2017','Thu Feb 16 18:02:45 2017','Thu Feb 16 19:02:45 2017','Thu Feb 16 20:02:45 2017','Thu Feb 16 21:02:45 2017','Thu Feb 16 22:02:45 2017','Thu Feb 16 23:02:45 2017']
Y = [([0.5,0.5,0.5,0.5,0.5,0.5,0.5],'平均')]
Ymain = [0.8894,0.889,0.8888,0.8884,0.036,0.8863,0.2858]
X_D = []
for t in X:
	X_D.append(time.strptime(t))
atool.PaintXY(X,Ymain,"白术",Y,'测试一下')

exit()
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


