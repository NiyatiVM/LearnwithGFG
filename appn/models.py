from flask import Flask
from .app import db

import psycopg2
from sqlalchemy.dialects.postgresql import JSON

class Users(db.Model):
	__tablename__ = 'users'

	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String())
	email = db.Column(db.String())
	url = db.Column(db.String(),unique=True)

	def __init__(self, name, email, url):
		self.name = name
		self.email = email
		self.url = url

	def __repr__(self):
		return "<Users(id='{}', name='{}', email={}, url={})>".format(self.id, self.name, self.email, self.url)

class Coders(db.Model):
	__tablename__ = 'coders'
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String())
	email = db.Column(db.String(),unique=True)

	def __init__(self, name, email):
		self.name = name
		self.email = email

	def __repr__(self):
		return '<id {}>'.format(self.id)

class Links(db.Model):
	__tablename__ = 'links'
	id = db.Column(db.Integer, primary_key=True)
	url = db.Column(db.String(),unique=True)

	def __init__(self, url):
		self.url = url

	def __repr__(self):
		return '<id {}>'.format(self.id)