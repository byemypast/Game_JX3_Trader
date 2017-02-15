# -*- coding:gbk -*-  
# һ������ű�
import settings

def RecipeToItem():
	#���䷽�ļ��в��ظ�����Ʒ��ȡ����������ѯ��
	items = {}
	for line in open(settings.RECIPE_FILENAME,encoding = 'gbk'):
		if (line[0]!='#')and(line.strip("\n").replace(" ","")!=''):
			#����������ҷ�ע��
			info = line.strip("\n").split(" ")
			compounds = info[3:][:-2]
			#��Ʒ ˵�� ��Դ ***�䷽*** �������� ר��
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
