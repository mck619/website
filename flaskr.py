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

@app.route('/')
def show_entries():
	cur = g.db.cursor()
	cur.execute('select title, text from entries order by id desc')
	entries = [dict(title=row[0], text=row[1]) for row in cur.fetchall()]
	return render_template('show_entries.html', entries=entries)

@app.route('/add', methods=['POST'])
def add_entry():
	if not session.get('logged_in'):
		abort(401)
	cur = g.db.cursor()
	cur.execute('insert into entries (title, text) values (%s, %s)',
                 [request.form['title'], request.form['text']])
	g.db.commit()
	flash('New entry was successfully posted')
	return redirect(url_for('show_entries'))

@app.route('/login', methods=['GET', 'POST'])
def login():
	error = None
	if request.method == 'POST':
		if request.form['username'] != app.config['USERNAME']:
			error = 'Invalid username'
		elif request.form['password'] != app.config['PASSWORD']:
			error = 'Invalid password'
		else:
			session['logged_in'] = True
			flash('You were logged in')
			return redirect(url_for('show_entries'))
	return render_template('login.html', error=error)

@app.route('/logout')
def logout():
	session.pop('logged_in', None)
	flash('You were logged out')
	return redirect(url_for('show_entries'))

if __name__ == '__main__':
	app.run(host='0.0.0.0')


