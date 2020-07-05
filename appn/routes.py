import os
import psycopg2
from .app import db
from flask import render_template,Blueprint,request,session,redirect,url_for,flash
import requests,os
from flask_wtf import FlaskForm
from wtforms import StringField,PasswordField,BooleanField
from wtforms.validators import InputRequired,Email,Length
from functools import wraps
from flask_sqlalchemy import SQLAlchemy
from .models import Users,Coders,Links
from .mailit import mailthecoders
from .automate import ps
from config import Config
# index = Blueprint('index',__name__)
# @index.route('/index')
# def indexp():  
#     return render_template("index.html")

class LoginForm(FlaskForm):
	username = StringField('username',validators=[InputRequired()])
	password = PasswordField('password',validators=[InputRequired()])
	remember = BooleanField('remember me')

def is_logged_in(f):
	@wraps(f)
	def wrap(*args, **kwargs):
		if 'logged_in' in session:
			return f(*args, **kwargs)
		else:
			flash('Unauthorized !! Please login','danger')
			return redirect(url_for('login.loginp'))
	return wrap

home = Blueprint('/',__name__)
@home.route('/')
def homep():  
    return render_template("index.html")
    
index = Blueprint('index',__name__)
@index.route('/index')
def indexp():  
    return render_template("index.html")


add = Blueprint('add',__name__)
@add.route("/add",methods=['GET','POST'])  
def addp(): 
    return render_template("add.html")  

remuser = Blueprint('remuser',__name__)
@remuser.route("/remuser",methods=['GET','POST'])  
def remuserp(): 
    return render_template("deleteuser.html")  

remrecord = Blueprint('remrecord',__name__)
@remrecord.route("/remrecord",methods=['GET','POST'])  
def remrecordp(): 
    return render_template("deleterecord.html")  

guideline = Blueprint('guideline',__name__)
@guideline.route("/guideline")  
def guidelinep(): 
    return render_template("guideline.html") 
 

subscribe = Blueprint('subscribe',__name__)
@subscribe.route("/subscribe",methods=['GET','POST'])  
@is_logged_in
def subscribep():  
    return render_template("subscribe.html")


automation = Blueprint('automation',__name__)
@automation.route("/automation",methods=['GET','POST'])  
@is_logged_in
def automationp():  
    return render_template("automate.html")


automatedurl = Blueprint('automatedurl',__name__)
@automatedurl.route("/automatedurl",methods = ["POST","GET"])  
@is_logged_in
def automatedUrlp():
    if request.method == "POST":   
        idnum = request.form["id"]
        user=Users.query.filter_by(id=idnum).first()
        if user:
            turl=user.url
            try:
                try:
                    num=db.session.query(Links).delete()
                    db.session.commit()
                except:
                    db.session.rollback()
                finally:
                    ps(turl)
                    db.session.query(Users).filter(Users.id==idnum).delete()
                    db.session.commit()
                    flash("Automation successfull !")
                    return render_template("secret.html")
            except:
                allentries=Users.query.all()
                if allentries:
                    flash("Some error occured .Couldn't automate.")
                    return render_template("secret.html")
                else:
                    flash("URL list empty .Try requesting url from home page")
                    return render_template("secret.html")
        else:
            flash("No such entry . Check the ID in the table")
            return render_template("secret.html")
    else:
        return render_template("secret.html")

deleterecord = Blueprint('deleterecord',__name__)
@deleterecord.route("/deleterecord",methods = ["POST","GET"])  
@is_logged_in
def deleterecordp():
    if request.method == "POST":   
        idnum = request.form["id"]
        coder=Coders.query.filter_by(id=idnum).first()
        if coder:
            db.session.query(Coders).filter(Coders.id==idnum).delete()
            db.session.commit()
            return render_template("secret.html")
        else:
            flash("No such entry . Check the ID in the table")
            return render_template("secret.html")
    else:
        return render_template("secret.html")


deleteuser = Blueprint('deleteuser',__name__)
@deleteuser.route("/deleteuser",methods = ["POST","GET"])  
@is_logged_in
def deleteuserp():
    if request.method == "POST":   
        idnum = request.form["id"]
        user=Users.query.filter_by(id=idnum).first()
        if user:
            db.session.query(Users).filter(Users.id==idnum).delete()
            db.session.commit()
            return render_template("secret.html")
        else:
            flash("No such entry . Check the ID in the table")
            return render_template("secret.html")
    else:
        return render_template("secret.html")


login = Blueprint('login',__name__)
@login.route('/login',methods=['GET','POST'])
def loginp():
	formy=LoginForm()
	return render_template('login.html',form=formy)

def validate(username, password):
    completion = False
    if username == os.environ.get('ADMIN_USER') and password== os.environ.get('ADMIN_PASSKEY'):
        completion=True
    return completion



tologin = Blueprint('tologin',__name__)
@tologin.route('/tologin', methods=['GET', 'POST'])
def toLoginp():
    error = None
    form=LoginForm()
    #try:
    if form.validate_on_submit() and request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        completion = validate(username, password)
        if completion ==False:
            error = 'Invalid Credentials. Please try again.'
            flash('Invalid Credentials. Please try again.')
            return render_template('index.html')
        else:
        	session['logged_in'] =True
        	session['username'] = username
        	return redirect(url_for('secret.secretp'))
    else:
        flash("Errrrror")
        return render_template('index.html')
    #except:
        #flash("Invalid credentials")
        #return render_template('index.html')
    #finall


secret = Blueprint('secret',__name__)
@secret.route('/secret')
@is_logged_in
def secretp():
	return render_template('secret.html')



savedetails = Blueprint('savedetails',__name__)
@savedetails.route("/savedetails",methods = ["POST","GET"])
def saveDetailsp():
    msg = "msg"
    if request.method == "POST":
        name = request.form["name"]
        email = request.form["email"]
        url = request.form["url"]
        strofurl='https://www.geeksforgeeks.org/'+url
        newrequest = requests.get(strofurl)
        if newrequest.status_code == 200:
            try:
                purl = Users.query.filter_by(url=url).first()
                if purl:
                    msg = "URL already in request list"
                else:
                    user=Users(name,email,url)
                    db.session.add(user)
                    db.session.commit()
                    msg = "URL successfully Added"
            except:
                msg="Please try adding a unique handle name"
    else:
        msg="URL requested does not belong to GFG"
    flash(msg)
    return render_template("index.html")


savecoders = Blueprint('savecoders', __name__)
@savecoders.route("/savecoders",methods = ["POST","GET"])
@is_logged_in
def savecodersp():
    msg = "msg"
    if request.method == "POST":
        try:
            name = request.form["name"]
            mail = request.form["email"]
            pmail = Coders.query.filter_by(email=mail).first()
            print(pmail)
            print("pmail")
            if pmail:
                msg = "Coder already in request list"
            else:
                print("inside")
                coder=Coders(name,mail)
                print(coder)
                print(coder)
                db.session.add(coder)
                db.session.commit()
                msg = "Coder successfully Added"
        except:
            db.session.rollback()
            msg = "Please try adding a unique handle name"
        finally:
            flash(msg)
            return render_template("secret.html")


viewcoders = Blueprint('viewcoders', __name__)
@viewcoders.route('/viewcoders')
@is_logged_in
def viewCodersp():
    rows=Coders.query.all()
    print(rows)
    return render_template("viewcoders.html",rows=rows)


view = Blueprint('view',__name__)
@view.route("/view")
def viewp():
    rows=Users.query.all()
    return render_template("view.html",rows = rows)


viewlinks = Blueprint('viewlinks',__name__)
@viewlinks.route("/viewlinks")
def viewlinksp():
    rows=Links.query.all()
    return render_template("viewlinks.html",rows = rows)



logout = Blueprint('logout',__name__)
@logout.route('/logout')
@is_logged_in
def logoutp():
    session.clear()
    flash('You are logged out','success')
    return redirect(url_for('login.loginp'))



mailall=Blueprint('mailall',__name__)
@mailall.route('/mailall')
@is_logged_in
def mailAllp():
    flag,msg=mailthecoders()
    if flag:
        msg="Mail sent"
    else:
        msg=msg
    flash(msg)
    return redirect(url_for('secret.secretp'))
