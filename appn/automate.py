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
    resultsforsome=soupone.find_all('div',{'class':'popularArticle'})
    ols=[]
    spans=[]
    uls=[]
    if len(results)>1:
      print("Found spans")
      for result in results:
        spans.append(result.find_all("span",{'class':'read-more'}))
    elif len(resultsforsome)>1:
      print("Found uls")
      for result in resultsforsome:
        exist=result.find("ul")
        if exist:
          uls.append(exist)
    else:
      print("Searching ols")
      ols=results[0].find_all("ol")
    print(*uls,sep="\n")
    lis=[]
    liss=[]
    for ol in ols:
      lis.append(ol.findAll('li'))
    for ul in uls:
      print("\nfind_all")
      new=ul.find_all('li')
      if new:
        for n in new:
          liss.append(n)
      else:
        pass
    #print(liss)
    links=[]
    for i in liss:
      if i.find('a'):
        links.append(i.find('a')['href'])
    for l in lis:
      print(l)
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