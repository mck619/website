# all the imports
import psycopg2
from flask import Flask, request, session, g, redirect, url_for, \
     abort, render_template, flash

# configuration
DATABASE = '/tmp/flaskr.db'
DEBUG = True
SECRET_KEY = 'DarrenSproles43'
USERNAME = 'admin'
PASSWORD = 'default'

# create our little application :)
app = Flask(__name__)
app.config.from_object(__name__)






def connect_db():
	f = open(dbpwd.txt)
	pwd = f.readline()
	try:
		conn =  psycopg2.connect(dbname = 'mydb', user = 'postgres', host='localhost', password=pwd)
		f.close
	except:
		f.close
		print('cant connect to database')
	return conn


def init_db():
	with closing(connect_db()) as db:
		with app.open_resource('schema.sql', mode='r') as f:
			db.cursor().execute(f.read())
	db.commit()


if __name__ == '__main__':
	app.run()


