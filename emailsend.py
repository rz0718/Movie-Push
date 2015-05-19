
# -*- coding: utf-8 -*-
import smtplib  
from email.mime.text import MIMEText  
import time

mailto_list=[]   #add the email accounts of receivers

mail_host="smtp.gmail.com"  #
mail_user=""    #      Setting up the senders' account
mail_pass=""   #  Password
mail_postfix="gmail.com"  #  The domain of emails



## updating maillists from local files and possible new files
def update_maillist(filepath):
	mailto_list = []
	fp = open(filepath,'r')
	for mail in fp:
		mailto_list.append(mail.split()[0])
	new_list = []
	mailto_list[:] = list(set(new_list+mailto_list))
	fp = open(filepath,'w')
	for mail in mailto_list:
		fp.write(mail)
		fp.write('\n')
	fp.close()
	return mailto_list



## Sending the email with the local html file as its content
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

mailto_list = update_maillist("to_list")

 
#Obtain the filepath for html file, since the file is named by the current time
time_now = time.strftime('%Y-%m-%d',time.localtime(time.time()))
filepath = time_now+'.html'



if send_mail(mailto_list,"moive report",filepath):
	print "succ"  
else:  
	print "faileds"  

