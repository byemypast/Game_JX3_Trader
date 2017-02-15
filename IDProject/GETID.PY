import sqlite3
conn = sqlite3.connect("nameid.db")
for line in open("JX3ITEMS 0215.out"):
	info = line.strip("\n").split("\t")
	if info[3]!='UiID':
		try:
			conn.execute("INSERT INTO ITEM VALUES("+info[3]+",'"+info[1]+"','"+info[2]+"');")
		except:
			pass
	#UID,name,category
conn.commit()