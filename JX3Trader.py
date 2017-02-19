# -*- coding:utf-8 -*-  
import JX3Control
import JX3Save
import JX3Analysis
import time
import settings
import send.sendmail
from debug import *
import os
import shutil
def TraderRecord(gameOBJ):
	gameOBJ.login()
	time.sleep(10)
	gameOBJ.openTrader()
	time.sleep(1)
	gameOBJ.TraderSearchWithoutOCR_Online()
	time.sleep(1)
	gameOBJ.logout()
	return gameOBJ.TraderSearchWithoutOCR_Offline()

def JX3_RealTime_Analysis(atool,ifsend = True):
	#建文件夹
	try:
		if os.path.exists(settings.SAVEPNG_DIRNAME)==True:
			shutil.rmtree(settings.SAVEPNG_DIRNAME)   #删除文件夹后建立
			os.mkdir(settings.SAVEPNG_DIRNAME)
		else:
			os.mkdir(settings.SAVEPNG_DIRNAME)
		op.clear()
	except Exception as err:
		debug("建立文件夹错误！错误内容："+str(err),'错误')
		return 
	buy,sell,price = atool.PaintRecent24hItemAll("24小时")
	#推荐买卖
	if buy!=None:
		op.record("推荐购买物品清单：","输出")
		for items,value in buy:
			op.record("物品："+items+"，低于历史均价："+str(value)+"，当前价格："+str(price[items]),'输出')
		op.record("------------------",'输出')
		op.record("推荐卖出物品清单：",'输出')
		for items,value in sell:
			op.record("物品："+items+"，高于历史均价。现在卖出抛去手续费后剩余利润："+ str(value)+"，当前价格："+str(price[items]),'输出')
	#最好配方
	for name,profit in atool.BestProduct():
		op.record("物品： "+ name+" 每精力净赚： "+ str(profit)+"金，物品描述："+atool.recipe[name]['describe']+"，配方来源："+atool.recipe[name]['source']+"，专精："+atool.recipe[name]['focus'],'输出')
	if ifsend:
		#发送走
		try:
			if os.path.exists(settings.TEMPZIP_FILENAME):
				os.remove(settings.TEMPZIP_FILENAME) #删除zip
		except Exception as err:
			debug("尝试删除zip文件失败！原因："+str(err))
		send.sendmail.zipfolder(settings.SAVEPNG_DIRNAME,settings.TEMPZIP_FILENAME)
		send.sendmail.sendwithzip("剑网三交易监控 - "+str(time.ctime()),op.getstr(),settings.TEMPZIP_FILENAME,settings.TEMPZIP_FILENAME)

#一次执行程序，用于生成配置文件等。如果已配置好可不被执行。
import Onetime
Onetime.RecipeToItem() #将配方系列转化为询价文件

#DEF
GameControl = JX3Control.JX3Action()
SaveControl = JX3Save.JX3Save()
AnalysisControl = JX3Analysis.JX3AnalysisTool("saverecord.db")
op = output()
lasttime = 0

time.sleep(10)
while True:
	if (time.time()-lasttime)>settings.INT_RECORDPRICE:
		debug("定时任务触发，间隔秒数 = "+str(settings.INT_RECORDPRICE))
		lasttime = time.time()
		#---------------任务开始----------------
		PriceList = TraderRecord(GameControl) #执行登录循环
		SaveControl.updateLib(PriceList) #保存
		JX3_RealTime_Analysis(AnalysisControl) #分析
		#---------------任务结束----------------
	time.sleep(1)