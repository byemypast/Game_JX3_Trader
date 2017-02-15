# -*- coding:gbk -*-  
import os
import sqlite3
from debug import *

class JX3Save(object):
	def __init__(self):
		if os.path.exists(settings.SAVEDB_FILENAME)==True:
			self.db = JX3Lib(sqlite3.connect(settings.SAVEDB_FILENAME))
		else:
			self._CreateLib(settings.SAVEDB_FILENAME)
	def _CreateLib(self,filename):
		debug("�����½��������ݿ� : "+filename)
		db = JX3Lib(sqlite3.connect(filename))
		db.query("CREATE TABLE itemsinfo(NAME TEXT,PRICE REAL,CATEGORY TEXT,TIME TEXT,N INT)")
		db.query("CREATE TABLE ninfo(NAME TEXT PRIMARY KEY,N INT,LASTUPDATE TEXT)")
		self.db = db
	def updateLib(self,listres):
		debug("��ʼ�����ݿ���д��ѯ�۽��")
		for (name,category,gold,sliver,copper,timeupdate) in listres:
			price = int(gold)+0.01*int(sliver)+0.0001*int(copper)
			result = self.db.query("SELECT N FROM ninfo where NAME = '"+name+"'")
			if result == []:
				query = self.db.query("INSERT INTO ninfo VALUES ('"+name+"',1,'"+str(timeupdate)+"')")
				n = 1
			else:
				query = self.db.query("UPDATE ninfo SET N = N+1,LASTUPDATE = '"+timeupdate+"' WHERE NAME = '"+name+"'")
				n = int(result[0][0]) + 1
			self.db.query("INSERT INTO itemsinfo VALUES ('"+name+"',"+str(price)+",'"+category+"','"+timeupdate+"',"+str(n)+")")
		self.db.commit()
		debug("д�����")


class JX3Lib(object):
	def __init__(self,conn):
		self.conn = conn
		pass
	def query(self,command,conn = None,commit = False):
		if conn == None:
			conn = self.conn
		result = -1
		command = str(command)
		try:
			result = conn.execute(command).fetchall()
			if commit ==True:
				conn.commit()
		except Exception as err:
			debug("���ݿ�ִ������������" + command + ",commit = "+str(commit)+" ,������Ϣ�� "+str(err),'����')
		return result
	def commit(self,conn = None):
		if conn ==None:
			conn = self.conn
		try:
			conn.commit()
		except:
			debug("���ݿⱣ�����",'����')