# LearnwithGFG

Scrapes GFG tutorials and creates a list of links from tutorials with automate.py

Then this links can be mailed everyday with automation everyday for learning new algorithms or solving questions.

Can be deployed on heroku (see automatedmails repo) with scheduling to fix a time when you want to receive mails.

Can be run locally by using Windows Task scheduler 

and a local postgres database

```
.env file shall hold

ADMIN_USER = for login 

ADMIN_PASSKEY = for login

ADMIN_MAIL = default admin mail

SECRET = for form validation 

DATABASE_URL = "your postgres db link"

MAIL_ACCOUNT = mail_address from which mails will be sent

PASSWORD = mail_add password
```
Create an additional email account for this to send mails as it will have to be configured to allow mails to be automated .

To do:
format this readme
