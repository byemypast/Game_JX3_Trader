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
		op.record("本次报告分为以下四部分：")
		op.record("[1].推荐购买物品清单")
		op.record("    **注：本版本推荐算法为： 物品当前交易行价格【低于】历史上该物品的均价")
		op.record("                             建议您充分考虑到成交量、恶意抬价等因素，结合[4].24小时物价监控图，谨慎做出决定")
		op.record("[2].推荐卖出物品清单")
		op.record("    **注：本版本推荐算法为： 物品当前交易行价格【高于】历史上该物品的均价")
		op.record("                             建议您充分考虑到成交量、恶意抬价等因素，结合[4].24小时物价监控图，谨慎做出决定")
		op.record("                             卖出部分的利润【已刨除】交易行手续费")
		op.record("[3].当前最大利润生物技艺物品清单")
		op.record("    **注：原材料、卖出价格按当前交易行价格。利润【未刨除】交易行手续费")
		op.record("[4].24小时物价监控图（附件）")
		op.record("    **注：附件中黄线为程序从2017年2月16日至今的均价走势。蓝线为程序每次上线交易行监控。因网速、意外下线、维护等问题，横轴并非严格等于一小时")
		op.record("---------------------------------------------------------------------------------")
		op.record("[1]. 推荐购买物品清单：","输出")
		for items,value in buy:
			op.record("物品："+items+"，低于历史均价："+str(value)+"，当前价格："+str(price[items]),'输出')
		op.record("------------------",'输出')
		op.record("[2]. 推荐卖出物品清单：",'输出')
		for items,value in sell:
			op.record("物品："+items+"，高于历史均价。现在卖出抛去手续费后剩余利润："+ str(value)+"，当前价格："+str(price[items]),'输出')
	#最好配方
	op.record("------------------",'输出')
	op.record("[3].当前最大利润生物技艺物品清单：",'输出')
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
		if settings.Easy_Mode ==False:
			JX3_RealTime_Analysis(AnalysisControl) #分析
		else:
			try:
				if os.path.exists(settings.TEMPZIP_FILENAME):
					os.remove(settings.TEMPZIP_FILENAME) #删除zip
			except Exception as err:
				debug("尝试删除zip文件失败！原因："+str(err))
			send.sendmail.zipfile(settings.SAVEDB_FILENAME,settings.TEMPZIP_FILENAME)
			send.sendmail.sendwithzip(time.ctime(),time.ctime(),settings.TEMPZIP_FILENAME,settings.TEMPZIP_FILENAME)
		#---------------任务结束----------------
	time.sleep(1)