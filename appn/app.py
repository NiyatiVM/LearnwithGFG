from flask import Flask
import os
from config import Config
from decouple import config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from urllib.parse import urlparse
db = SQLAlchemy()
migrate = Migrate()
def create_app():
	app = Flask(__name__)
	app.config.from_object(Config)
	app.static_folder = 'static'
	SECRET_KEY = os.urandom(32)
	app.config['SECRET_KEY'] = SECRET_KEY
	app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
	app.config['SQLALCHEMY_DATABASE_URI'] = config('DATABASE_URI')
	db.init_app(app)
	migrate.init_app(app,db)
	from .routes import index,login,logout,mailall,viewlinks,view,viewcoders,savecoders,savedetails,secret,tologin
	from .routes import deleteuser,automatedurl,automation,subscribe,guideline,add,deleterecord,remuser,remrecord
	app.register_blueprint(index)
	app.register_blueprint(login)
	app.register_blueprint(logout)
	app.register_blueprint(mailall)
	app.register_blueprint(viewlinks)
	app.register_blueprint(view)
	app.register_blueprint(viewcoders)
	app.register_blueprint(savecoders)
	app.register_blueprint(savedetails)
	app.register_blueprint(secret)
	app.register_blueprint(tologin)
	app.register_blueprint(automatedurl)
	app.register_blueprint(automation)
	app.register_blueprint(subscribe)
	app.register_blueprint(guideline)
	app.register_blueprint(add)
	app.register_blueprint(deleteuser)
	app.register_blueprint(deleterecord)
	app.register_blueprint(remuser)
	app.register_blueprint(remrecord)
	from . import models
	return app
