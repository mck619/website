# all the imports
import psycopg2
from flask import Flask, request, session, g, redirect, url_for, \
     abort, render_template, flash
from contextlib import closing

# configuration
f = open('config.txt')
secrets = f.readlines()
f.close
DATABASE = '/tmp/flaskr.db'
DEBUG = True
SECRET_KEY = secrets[0].replace('\n','')
USERNAME = secrets[1].replace('\n','')
PASSWORD = secrets[2].replace('\n','')

# create our little application :)
app = Flask(__name__)
app.config.from_object(__name__)


@app.route('/HAL')
def HAL():
	return "I'm sorry, Dave. I'm afraid I can't do that."


def connect_db():
	f = open('dbpwd.txt')
	pwd = f.readline().replace('\n','')
	try:
		conn =  psycopg2.connect(dbname = 'mydb', user = 'postgres', password = pwd, host='localhost')
		f.close
	except Exception as e:
		print(e)
		f.close
		print('cant connect to database')
	return conn


def init_db():
	with closing(connect_db()) as db:
		with app.open_resource('dbtester.sql', mode='r') as f:
			db.cursor().execute(f.read())
		db.commit()

@app.before_request
def before_request():
	g.db = connect_db()

@app.teardown_request
def teardown_request(exception):
	db = getattr(g, 'db', None)
	if db is not None:
		db.close()








if __name__ == '__main__':
	app.run(host='0.0.0.0')


