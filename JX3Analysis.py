# -*- coding:utf-8 -*-  
from debug import *
import settings
import sqlite3
import datetime
import os.path
import time
import matplotlib.font_manager as fm
myfont = fm.FontProperties(fname = settings.PAINTING_FONT_FILENAME) #默认华文雅黑
import matplotlib.pyplot as plt
from PIL import Image
from io import BytesIO


class JX3AnalysisTool(object):
	recipe = {}
	util = None
	def __init__(self,dbname):
		self.conn = sqlite3.connect(dbname = settings.SAVEDB_FILENAME)
		self.util = settings.util()
		self.RecipeLoader()
	def dbQuery(self,command):
		try:
			result = self.conn.execute(command).fetchall()
		except Exception as err:
			debug("分析数据库时执行命令出错！命令：" + command + " ,错误信息： "+str(err),'错误')
		return result
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
			plt.annotate(xy[1], xy=xy, xytext=(-5,0), textcoords = 'offset points')
		#保存到PIL对象
		imgdata = BytesIO()
		fig.savefig(imgdata,format = 'png')
		imgdata.seek(0)
		im = Image.open(imgdata)
		plt.close('all')
		return im

	def RecipeLoader(self,source = settings.RECIPE_FILENAME):
		debug("开始读取配方设置!")
		debug("配方文件： "+source+" 配方更新时间：" + time.ctime(os.path.getmtime(source)))
		for line in open(source):
			if line.strip("\n")!='':
				info = line.strip("\n").split(" ")
				name = info[0].split(",")[0]
				intmake = int(info[0].split(",")[1]) #一次制造能做几个
				describe = info[1] #描述
				itemsource = info[2] #来源
				focus = info[-1:] #专精
				intconsume = int(info[-2:-1]) #消耗精力
				self.util.dict2d(self.recipe,name,'intmake',intmake)
				self.util.dict2d(self.recipe,name,'describe',describe)
				self.util.dict2d(self.recipe,name,'source',itemsource)
				self.util.dict2d(self.recipe,name,'focus',focus)
				self.util.dict2d(self.recipe,name,'intconsume',intconsume)
				self.util.dict2d(self.recipe,name,'recipe',info[3:-2])
