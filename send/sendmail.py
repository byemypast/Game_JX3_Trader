# -*- coding: gbk -*-

import settings_pwd
import smtplib
from email.mime.text import MIMEText
from email.header import Header
from debug import *
# ������ SMTP ����
def send(subject,maintext):
	debug("send.sendmail.send : subject "+subject+" maintext: "+maintext)
	try:
		mail_host=settings_pwd.mail_host
		mail_user=settings_pwd.mail_user
		mail_pass=settings_pwd.mail_pass
		sender = mail_user #�Լ������Լ�
		receivers = mail_user 
		message = MIMEText(maintext, 'plain', 'utf-8')
		message['From'] = Header("�Լ�", 'utf-8')
		message['To'] =  Header("�Լ�", 'utf-8')
		message['Subject'] = Header(subject, 'utf-8')
		smtpObj = smtplib.SMTP() 
		smtpObj.connect(mail_host, 25)    # 25 Ϊ SMTP �˿ں�
		smtpObj.login(mail_user,mail_pass)  
		smtpObj.sendmail(sender, receivers, message.as_string())
		debug ("�ʼ����ͳɹ�")
	except Exception as err:
		debug("�ʼ�����ʧ�ܣ�ԭ��"+str(err))
