import psycopg2
from urllib.parse import urlparse
import smtplib,ssl
import getpass,requests
from bs4 import BeautifulSoup
from datetime import date
from decouple import config
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
url=urlparse(config('DATABASE_URI'))
db = "dbname=%s user=%s password=%s host=%s " % (url.path[1:], url.username, url.password, url.hostname)
con = psycopg2.connect(db, sslmode='allow')
sender_email = config('MAIL_ACCOUNT')
receiver_email =config('ADMIN_MAIL')
COMMASPACE = ', '
def alerttoadmin(server):
  message="Heyyy , ADMIN ! All the links have been mailed \n Your revision for the current url is done \n USE AUTOMATION !!\n\n And by the CONGRATS !!"
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
  print(f"mailadd={mailadd}")
  try:
    server.sendmail(sender_email,mailadd,message.as_string())
    print("Mail sent")
  except:
    print("Try sending message again!")

port = 465
#password = getpass.getpass(prompt='Password : ')
password=config('PASSWORD')
def mailthecoders():
  # Create a secure SSL context
  context = ssl.create_default_context()
  #Getting all the emails to send to 
  mailadd=[]
  with con as conn:
    cur = conn.cursor()
    cur.execute("select email from coders")
    record = cur.fetchall()
    for i in record:
      mailadd.append(i[0])
  try:
    with smtplib.SMTP_SSL("smtp.gmail.com", port, context=context) as server:
      server.login(sender_email, password)
      print("Login successful !!")
      alln=[]
      with con as conn:
        cur = conn.cursor()
        cur.execute("select * from Links limit 5")
        record = cur.fetchall()
        print(record)
        if record:
          ids=[]
          for i in record:
            ids.append(i[0])
            link=i[1].strip()
            sendthemail(link,mailadd,server)
          query2="""delete from Links where id = %s"""
          for i in ids:
            value=(i,)
            cur.execute(query2,value)
          conn.commit()
        else:
          alerttoadmin(server)
  except:
    print("Error occured")

def contentsearch(contenturl):
    title=None
    use_elems=None
    response=requests.get(contenturl)
    print(response.status_code)
    if response.status_code==200:
        print("Successfully opened the first web page")
        soupone=BeautifulSoup(response.text,'lxml')
        [script.extract() for script in soupone(["script", "ins","footer"])]
        #use_elems = soupone.find('article')
        titlee=soupone.find('h1',{'class':'entry-title'})
        if titlee:
            title=titlee.contents[0]
            #print(title)
            #Getting the required content
            use_elems=soupone.find('div',{'class':'entry-content'})
            use_elems=clean(use_elems)
        else:
            problems=soupone.find('div',{'class':'problemQuestion'})
            if problems:
                #To differentiate between everyday problems
                #So all mails don't stuff up under previous day's mails
                title='Problems  '+ str(date.today())
                use_elems=clean(problems)
        #print(use_elems)
    else:
        print('Some error occured ')
    return title,use_elems

def clean(content):
  listtodelete=['hideInCourse','clear hideIt','personalNoteHeader clear','noteHeaderText','hideNotesDivIcon','collapsableDivPersonalNotes','recommendedPostsDiv',]
  for i in listtodelete:
    elems=content.find('div',class_=i)
    if elems:
      elems.decompose()
  some=content.find_all('i',class_='material-icons')
  for i in some:
    i.decompose()
  banner=content.find_all('a')
  for j in banner:
    p=j.get('href')
    if p!=None and 'utm_medium=banner' in p:
      j.decompose()
  elems=content.find_all('div')
  for i in elems:
    p=i.get('id')
    if p!=None and 'AP_G4GR_' in p:
      i.decompose()
  rem=content.find(id='improvedBy')
  if rem:
    rem.decompose()
  return content

mailthecoders()