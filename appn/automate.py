import requests 
from .app import db
from .models import Users,Coders,Links
from bs4 import BeautifulSoup
def ps(urlink):
  firsturl='https://www.geeksforgeeks.org/'+urlink
  response=requests.get(firsturl)
  if response.status_code==200:
    print("Successfully opened the first web page")
    #print("The algorithm category is :-\n")
    soupone=BeautifulSoup(response.content,'lxml')
    #results = soupone.find(id=postid)
    results = soupone.find_all('article')
    ols=[]
    spans=[]
    if len(results)>1:
      for result in results:
        spans.append(result.find_all("span",{'class':'read-more'}))
    else:
      ols=results[0].find_all("ol")
    #print(ols)
    lis=[]
    for ol in ols:
      lis.append(ol.findAll('li'))
    links=[]
    for l in lis:
      for i in l:
        if i.find('a'):
          links.append(i.find('a')['href'])
    for span in spans:
      for i in span:
        if i.find('a'):
          links.append(i.find('a')['href'])
    for i in links:
      try:
        link=Links(i)
        db.session.add(link)
        db.session.commit()
      except:
        db.session.rollback()