# -*- coding:utf-8 -*-  
#公用库
import os
#第三方库
import win32api
#私有库
from debug import *

#发布相关
VERSION = 0.4 #版本号
DEBUG_FLAG = 0 #是否为DEBUG模式。0为关，1为开。请勿修改！

#时间设置相关
INT_GLOBAL_WAITING = 0.2 #每次操作后等待时间
INT_RECORDPRICE = 60 * 60 #每隔多少秒登录游戏记录一次价格。至少半小时(1800),推荐一个小时(3600)
INT_GLOBAL_OVERTIME = 45 #默认超时操作时间

#画图设置
INT_THRESLOAD_MINUSEXP = 10 #如果均值和价格过于接近，不做图
INT_OLDSTYLE_TOPLIMIT = 20000 #老格式的查询文件（query.txt），上限最高多少砖。如果读取的价格超过这个钱数，则认为是无效价格（缺货/恶意抬价），不予考虑。

#程序文件设置
DEBUGNAME = "debug.txt" #调试文件输出名（允许在运行前不存在）
RECIPE_FILENAME = 'recipe.txt' #配方原始文件
ITEMSIDDB_FILENAME = 'nameid.db' #物品名称-UID-分类转化数据库
QUERYITEM_FILENAME = 'query.txt' #欲查询的物品文件
IGNOREITEM_FILENAME = 'ignore.txt' #查询物品中需要忽略的文件
AHRECORD_FILENAME = 'F:\\Game\\JX3\\bin\\zhcn\\interface\\AH\\AH_Base\\data\\ah.jx3dat' #AH插件记录（允许在运行前不存在）
SAVEDB_FILENAME = 'saverecord.db' #询价保存数据库（允许在运行前不存在）
PAINTING_FONT_FILENAME = 'C:\\Windows\\Fonts\\msyh.ttc' #画图默认采用华文雅黑字体
TEMPZIP_FILENAME = "temp.zip" #临时保存的压缩文件名
SAVEPNG_DIRNAME = "savepng" #图像保存的文件夹路径

#反侦测模式设置
INT_ANTI_SCAN = 1 #反侦测总开关 1 = 开
FLOAT_WAITING_RANDOM_LOWER = 0.1 #随机等待时间下限
FLOAT_WAITING_RANDOM_UPPER = 0.3 #随机等待时间上限

#登录模块相对位置设置
TUPLE_LOGIN_USERNAME = (690/1366,346/768)
TUPLE_LOGIN_PWD = (690/1366,370/768)
TUPLE_LOGIN_OK = (716/1366,416/1080)
TUPLE_LOGIN_CONFIRM_LOCATION = (38/1366,698/768) #左下角西山居白色标志。如果消失(非(255,255,255))意味着进入“角色选择页面”
TUPLE_LOGIN_CONFRIM_PIXEL = (255,255,255)
TUPLE_LOGIN_SUCCESS_LOCATION = (1360/1366,43/768) #右上角登陆成功后的修饰花纹
TUPLE_LOGIN_SUCCESS_PIXEL = (71,118,106) #右上角登陆成功后的修饰花纹
TUPLE_LOGIN_BUSYLOGIN_LOCATION = (766/1366,578/768) #服务器繁忙登录按钮
TUPLE_LOGIN_BUSYLOGIN_PIXEL = (109,175,147)

TUPLE_LOGIN_HOTSPAM_LOCATION = (1395/1920,276/1080)
TUPLE_LOGIN_HOTSPAM_PIXEL = (64,90,86)


#交易行模块
TUPLE_TRADER_DIALOG = (166/1366,190/768) #交易行对话——交易行

TUPLE_TRADER_ITEMINPUT = (69/1366,208/768) #交易行物品输入框
TUPLE_TRADER_QUERYBUTTON = (44/1366,169/768) #"买卖"分页按钮
TUPLE_TRADER_SELLBUTTON = (208/1366,164/768) #"寄卖"分页按钮
TUPLE_TRADER_SEARCHBUTTON = (526/1366,206/768) #搜索按钮
TUPLE_TRADER_SEARCHBUTTON_NONGRAY = (146,139,57) #未等待中的按钮颜色
TUPLE_TRADER_SEARCHBUTTON_GRAY = (138,146,146) #等待中的灰色按钮颜色

#发信相关
STR_MAIL_SENDTO = 'wangjunyi2008@sina.com,postnice9606@126.com'


#将相对位置转化为绝对位置
class util():
	Screen_X = 0
	Screen_Y = 0
	def __init__(self):
		self.Screen_X =  win32api.GetSystemMetrics(0)
		self.Screen_Y = win32api.GetSystemMetrics(1)
	def GetIntTuple(self,value):
		return tuple((int(value[0]* self.Screen_X),int(value[1] * self.Screen_Y)))
	def CompareTuple(self,x,y,sensitive = 20):
		#比较两个像素点的相似性，如果非常相似（合之差<20）返回1
		sum = 0
		for i in range(0,min(len(x),len(y))):
			sum += abs(x[i]-y[i])
		if sum<sensitive:
			return True
		else:
			return False
	def dict2d(self,tdict,key_a,key_b,val):
		if key_a in tdict:
			tdict[key_a].update({key_b : val})
		else:
			tdict.update({key_a: {key_b :val}})



	class SystemCheck():
		def __init__(self):
			debug("开始自检。当前版本 "+ str(VERSION))
			checkname = [IGNOREITEM_FILENAME,ITEMSIDDB_FILENAME,QUERYITEM_FILENAME,RECIPE_FILENAME,PAINTING_FONT_FILENAME]
			checked = True
			for filename in checkname:
				if os.path.exists(checkname)==False:
					debug("程序包完整性检查：" + filename +" 文件不存在！",'错误')
					checked = False
			if checked == True:
				debug("程序包完整性检查成功！")
			return checked