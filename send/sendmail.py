# -*- coding: utf-8 -*-

import settings
import settings_pwd
import smtplib
from email.mime.text import MIMEText
from email.header import Header
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
import os
import os.path
import zipfile
import debug
# 第三方 SMTP 服务
def send(subject,maintext):
	debug.debug("send.sendmail.send : subject "+subject+" maintext: "+maintext)
	try:
		mail_host=settings_pwd.mail_host
		mail_user=settings_pwd.mail_user
		mail_pass=settings_pwd.mail_pass
		sender = mail_user #自己发给自己
		receivers = mail_user 
		message = MIMEText(maintext, 'plain', 'utf-8')
		message['From'] = Header("自己", 'utf-8')
		message['To'] =  Header("自己", 'utf-8')
		message['Subject'] = Header(subject, 'utf-8')
		smtpObj = smtplib.SMTP() 
		smtpObj.connect(mail_host, 25)    # 25 为 SMTP 端口号
		smtpObj.login(mail_user,mail_pass)  
		smtpObj.sendmail(sender, receivers, message.as_string())
		debug.debug ("邮件发送成功")
	except Exception as err:
		debug.debug("邮件发送失败！原因："+str(err))

def sendwithzip(subject,maintext,zipfilepathname,zipfilename):
	debug.debug("send.sendmail.send : subject "+subject+" maintext: "+maintext)
	try:
		mail_host=settings_pwd.mail_host
		mail_user=settings_pwd.mail_user
		mail_pass=settings_pwd.mail_pass
		sender = mail_user #自己发给自己
		receivers = settings.STR_MAIL_SENDTO

		msg = MIMEMultipart()
		msg['From'] = Header("自己", 'utf-8')
		msg['To'] =  Header("自己", 'utf-8')
		msg['Subject'] = Header(subject, 'utf-8')
		msg.attach(MIMEText(maintext,'plain','utf-8'))

		zippart = MIMEApplication(open(zipfilepathname,'rb').read())
		zippart.add_header('Content-Disposition', 'attachment',filename = zipfilename)
		msg.attach(zippart)


		smtpObj = smtplib.SMTP() 
		smtpObj.connect(mail_host, 25)    # 25 为 SMTP 端口号
		smtpObj.login(mail_user,mail_pass)  
		smtpObj.sendmail(sender, receivers, msg.as_string())
		smtpObj.quit()
		debug.debug ("邮件发送成功")
	except Exception as err:
		debug.debug("邮件发送失败！原因："+str(err))

def zipfolder(path ,filename):
	debug.debug("开始压缩路径" + path+"--->"+filename)
	try:
		zipf = zipfile.ZipFile(filename,'w',zipfile.ZIP_DEFLATED)
		for root,dirs,files in os.walk(path):
			for f in files:
				zipf.write(os.path.join(root,f),os.path.join(root,f).replace(os.sep,"_"))
		zipf.close()
	except Exception as err:
		debug.debug("压缩失败！错误信息："+str(err))

def zipsinglefile(filenamefrom,filenameto):
	f = zipfile.ZipFile(filenameto,'w',zipfile.ZIP_DEFLATED)
	f.write(filenamefrom)
	f.close()