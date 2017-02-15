# -*- coding:gbk -*-  
# 一次性类脚本
import settings

def RecipeToItem():
	#把配方文件中不重复的物品提取出来，做查询用
	items = {}
	for line in open(settings.RECIPE_FILENAME,encoding = 'gbk'):
		if (line[0]!='#')and(line.strip("\n").replace(" ","")!=''):
			#如果有内容且非注释
			info = line.strip("\n").split(" ")
			compounds = info[3:][:-2]
			#物品 说明 来源 ***配方*** 消耗体力 专精
			itemadd = [(info[0].split(",")[0],1)]
			for compound in compounds:
				itemadd.append((compound.split(",")[0],compound.split(",")[1]))
			for item,count in itemadd:
				if item in items:
					items[item] += int(count)
				else:
					items[item] = int(count)
		f = open(settings.QUERYITEM_FILENAME,'w',encoding = 'gbk')
		for item in items:
			f.write(item+"\t"+str(items[item])+"\n")
		f.close()
