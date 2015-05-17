
# -*- coding: utf-8 -*-
import smtplib  
from email.mime.text import MIMEText  

mailto_list=["rui91seu@gmail.com","kwkwvenusgod@gmail.com","nick.yinyang@gmail.com","xhgeng131500@gmail.com","dawenliu0909@gmail.com","Chenly.xian@gmail.com","cqbaizuo@gmail.com"]
mail_host="smtp.gmail.com"  #
mail_user="coolcoolruimovie"    #
mail_pass="123456ntu"   #
mail_postfix="gmail.com"  #


def update_maillist(filepath):
	mailto_list = []
	fp = open(filepath,'r')
	for mail in fp:
		mailto_list.append(mail)
	new_list = []
	mailto_list[:] = list(set(new_list+mailto_list))
	fp.close()
	fp = open(filepath,'w')
	for mail in mailto_list:
		fp.write(mail)
	fp.close()


def send_mail(to_list,sub,filepath):  
	
	post = open(filepath,'r')
	content = post.readlines()
	content = ''.join(content)
	post_html = "\"\"\"\\" + content + "\"\"\""

	me="hello"+"<"+mail_user+"@"+mail_postfix+">"  
	msg = MIMEText(content,_subtype='html',_charset='gb2312')  
	msg['Subject'] = sub  
	msg['From'] = me  
	msg['To'] = ";".join(to_list)  
	try:  
		server = smtplib.SMTP()  
		server.connect(mail_host)  
		server.ehlo()
		server.starttls()  
		server.login(mail_user,mail_pass)  
		server.sendmail(me, to_list, msg.as_string())  
		server.close()  
		return True  
	except Exception, e:  
		print str(e)  
		return False  

update_maillist("to_list")

 
"""
filepath = "2015-05-16.html"
if send_mail(mailto_list,"moive report",filepath):
	print "succ"  
else:  
	print "faileds"  
"""
