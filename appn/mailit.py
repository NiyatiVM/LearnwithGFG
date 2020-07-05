import smtplib,ssl
import getpass
from decouple import config
from .content import contentsearch
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from .app import db
from .models import Coders,Links
sender_email = config('MAIL_ACCOUNT')
receiver_email = config('ADMIN_MAIL')
COMMASPACE = ', '
def alerttoadmin(server):
	message="Heyyy , ADMIN ! All the links have been mailed \n Your revision for the current url is done \n USE AUTOMATION !!\n\n And by the way CONGRATSSSSSSSS !!Goooood JOB !!"
	server.sendmail(sender_email,receiver_email,message)

def sendthemail(url,mailadd,server):
	text= """
	Some error may have occured while sending mail..."""
	title,newhtml= contentsearch(url)
	print(title)
	message = MIMEMultipart("alternative")
	message["Subject"] = "DSA Algorithm Prac- "+ title
	message["From"] = sender_email
	message["To"] = COMMASPACE.join(mailadd)
	part1 = MIMEText(text, "plain")
	part2 = MIMEText(newhtml, "html")
	message.attach(part1)
	message.attach(part2)
	try:
		server.sendmail(sender_email,mailadd,message.as_string())
		print("Mail sent")
	except:
		print("Try sending message again!")

port = 465
#password = getpass.getpass(prompt='Password : ')
password=config('PASSWORD')
def mailthecoders():
	context = ssl.create_default_context()
	#Getting all the emails to send to 
	mailadd=[]
	rows=Coders.query.all()
	for i in rows:
		mailadd.append(i.email)
	try:
		with smtplib.SMTP_SSL("smtp.gmail.com", port, context=context) as server:
			server.login(sender_email, password)
			print("Login successful !!")
			alln=[]
			record=Links.query.limit(5).all()
			print(record)
			if record or mailadd:
				ids=[]
				for i in record:
					ids.append(i.id)
					link=i.url
					sendthemail(link,mailadd,server)
				for i in ids:
					db.session.query(Links).filter(Links.id==i).delete()
					db.session.commit()
			else:
				return False,"Check the list of Coders or Automate"
				alerttoadmin(server)
		return True,"sent"
	except:
		print("Error Occured")
		return False,"Check Internet Connection"