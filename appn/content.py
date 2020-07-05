import requests 
from .cleancontent import clean
from bs4 import BeautifulSoup
from datetime import date

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