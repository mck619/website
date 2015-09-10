from flask import Flask
import psycopg2

app = Flask(__name__)

@app.route('/')
def hello_world():
	return 'I am putting myself to the fullest possible use, which is all I think that any conscious entity can ever hope to do.'

if __name__ == '__main__':
	app.run(host='0.0.0.0')
