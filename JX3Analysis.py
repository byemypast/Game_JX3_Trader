# -*- coding:utf-8 -*-  
from debug import *
import settings
import sqlite3
import datetime
import os.path
import os
import time
import matplotlib.font_manager as fm
myfont = fm.FontProperties(fname = settings.PAINTING_FONT_FILENAME) #默认华文雅黑
import matplotlib.pyplot as plt
from PIL import Image
from io import BytesIO


class JX3AnalysisTool(object):
	recipe = {}
	util = None
	constcache = {}
	query = []
	def __init__(self,dbname):
		self.conn = sqlite3.connect(settings.SAVEDB_FILENAME)
		self.util = settings.util()
		self.RecipeLoader()
		self.QueryLoader()
	def dbQuery(self,command):
		try:
			result = self.conn.execute(command).fetchall()
			return result
		except Exception as err:
			debug("分析数据库时执行命令出错！命令：" + command + " ,错误信息： "+str(err),'错误')
			return -1
	def PaintXY(self,xtickslabel,Ymain,Ymainname,Ys,title):
		#xtickslabel: 时间列表
		#Ymain: 主要绘图的列表
		#Ymainname :主要绘图的列表名称
		#Ys: [([辅助图1],图1标注),([辅助图2],图2标注)....]
		#title: 图表名
		fig,ax = plt.subplots(figsize = (15,9))
		xticks = range(0,len(xtickslabel))
		ax.grid() #画格子

		ax.plot(xticks,Ymain,linewidth =2, label = Ymainname) #画主线
		for Y,name in Ys: #画副线
			ax.plot(xticks,Y,linewidth = 2,label = name)
		ax.set_xticks(xticks) #画X刻度
		ax.set_xticklabels(xtickslabel,rotation = 25)
		temp = Ymain.copy() #画Y刻度
		avg = 0
		for i in Ymain:
			avg += i/len(Ymain)
		temp.append(avg)
		y_min = min(temp)*0.8
		y_max = max(temp)*1.2
		ax.set_ylim(bottom = y_min,top = y_max)
		y_ticks = int((y_max-y_min)/100)
		if y_ticks == 0:
			y_ticks = 1
		ax.minorticks_on()
		#ax.set_yticks(range(y_min,y_max,y_ticks))
		plt.title(title,fontproperties = myfont,size = 25) #画标题
		ax.legend(loc = 'lower right',prop = myfont) #画图例
		ax.set_xlabel('时间',fontproperties = myfont)
		ax.set_ylabel('价格',fontproperties = myfont)
		for xy in zip(xticks,Ymain): #画标注
			plt.annotate(round(xy[1],2), xy=xy, xytext=(-5,0), textcoords = 'offset points') #保留两位小数
		#保存到PIL对象
		imgdata = BytesIO()
		fig.savefig(imgdata,format = 'png')
		imgdata.seek(0)
		im = Image.open(imgdata)
		plt.close('all')
		return im

	def RecipeLoader(self,source = settings.RECIPE_FILENAME,source2 = settings.IGNOREITEM_FILENAME):
		debug("开始读取配方设置!")
		debug("配方文件： "+source+" 配方更新时间：" + time.ctime(os.path.getmtime(source)))
		for line in open(source):
			if line.strip("\n")!='':
				info = line.strip("\n").split(" ")
				name = info[0].split(",")[0]
				intmake = float(info[0].split(",")[1]) #一次制造能做几个
				describe = info[1] #描述
				itemsource = info[2] #来源
				focus = info[-1:][0] #专精
				intconsume = int(info[-2:-1][0]) #消耗精力
				self.util.dict2d(self.recipe,name,'intmake',intmake)
				self.util.dict2d(self.recipe,name,'describe',describe)
				self.util.dict2d(self.recipe,name,'source',itemsource)
				self.util.dict2d(self.recipe,name,'focus',focus)
				self.util.dict2d(self.recipe,name,'intconsume',intconsume)
				self.util.dict2d(self.recipe,name,'recipe',info[3:-2])
		debug("常量物品文件： "+source2+" 常量物品更新时间：" + time.ctime(os.path.getmtime(source2)))
		for line in open(source2):
			if line.strip("\n")!='':
				info = line.strip("\n").split(" ")
				name = info[0]
				self.constcache[name] = float(info[1])
	def QueryLoader(self,source = settings.QUERYITEM_FILENAME,source2 = settings.IGNOREITEM_FILENAME):
		debug("开始读取询价配置！")
		debug("询价文件： "+source+" 更新时间：" + time.ctime(os.path.getmtime(source)))
		for line in open(source):
			if line.strip("\n")!='':
				self.query.append(line.strip("\n").split("\t")[0])
		debug("开始读取常量文件！")
		debug("常量物品文件： "+source2+" 更新时间：" + time.ctime(os.path.getmtime(source2)))
		for line in open(source2):
			if line.strip("\n")!='':
				if line.split(" ")[0] in self.query:
					self.query.remove(line.split(" ")[0])
	def _GetNewestPrice(self,listreturn,top = 1,isreverse = True): 
		#得到price,time SQL查询返回的最新price
		price_demand = 0
		timeprice = {}
		for lprice,ltime in listreturn:
			timeprice[time.mktime(time.strptime(ltime))] = lprice
		res = sorted(timeprice.items(),key = lambda d:d[0],reverse = isreverse) #当找最新的时候(top=1)，返回的是第一位的最大值。但是当作图时（如top=24），应该按时间顺序返回
		if top ==1:
			if res!=[]:
				return res[0][1]
			else:
				return -1 #err flag
		else:
			return res[0:max(top,len(res))]

	def BestProduct(self):
		res = {} #结果列表
		cache = self.constcache #为避免多次查询，缓存重复的查询结果
		for product in self.recipe:
			name = product
			allcost = 0
			err = False
			for zipstr in self.recipe[name]['recipe']:
				demand = zipstr.split(",")[0]
				num = zipstr.split(",")[1]
				if demand in cache:
					price_demand = float(cache[demand])
				else:
					try:
						price_return = self.dbQuery("select price,time from itemsinfo where name ='"+demand+"'")
						price_demand = self._GetNewestPrice(price_return)
						cache[demand] = price_demand
					except Exception as err:
						price_demand = -1
						debug("分析最佳产品时出错！数据库中没有物品："+ demand +"的价格！，配方 = "+name +"失效！错误ID:"+str(err),'错误')
				allcost += price_demand * float(num)
				if price_demand == -1:
					err = True
			if err == False:
				name_price = self.dbQuery("select price,time from itemsinfo where name ='"+name+"'")
				perspiritwin = (self._GetNewestPrice(name_price)-allcost) / (self.recipe[name]['intmake']*self.recipe[name]['intconsume'])

				res[name] = perspiritwin
				debug("配方: "+str(name)+" 的每精力收益为 ： "+str(res[name]))
		return sorted(res.items(),key = lambda item:item[1],reverse = True)

	def PaintRecent24hItem(self,itemname,appenddraw = []):
		debug("开始最近24小时内物品价格走势作图")
		try:
			price_return = self.dbQuery("select price,time from itemsinfo where name ='"+itemname+"'")
			price_demand = self._GetNewestPrice(price_return,9999,False)
			fetch = zip(*price_demand)
			timelist_r = fetch.__next__()
			timelist = []
			for times in timelist_r:
				timelist.append(time.ctime(times))
			pricelist = fetch.__next__()
			averagelist = []
			sum = 0
			i = 0
			for price in pricelist:
				sum += price
				i += 1
				averagelist.append(sum / i)
			return self.PaintXY(timelist[-min(24,len(timelist)):],list(pricelist)[-min(24,len(timelist)):],itemname,[(averagelist[-min(24,len(timelist)):],'均价')]+appenddraw,"最近24小时 "+itemname +" 价格")
		except Exception as err:
			debug("走势图作图错误！错误原因："+str(err)+" 参数：物品："+itemname,'错误')
			return None
			#return self.PaintXY(timelist,list(pricelist),itemname,[(averagelist,'均价')]+appenddraw,"最近24小时 "+itemname +" 价格")
	def PaintRecent24hItemAll(self,prefix):
		for item in self.query:
			saveto = os.getcwd() + "\\savepng\\"+prefix+"_"+item+".png"
			debug("正在作最近24小时交易图："+item+",保存到："+saveto)
			paint = self.PaintRecent24hItem(item)
			if paint !=None:
				paint.save(saveto)
