from flask import Flask, g, redirect, render_template, request
import sqlite3
from os.path import exists
from classes.forms import Inizializzazione

app: Flask = Flask(__name__)
database: str = app.root_path+'/personal-va.db'

def getDbConnection() -> sqlite3.Connection:
	db: sqlite3.Connection = getattr(g, '_database', None)
	if db is None:
		db = g._database = sqlite3.connect(database)
	return db

@app.teardown_appcontext
def closeDbConnection(exception) -> None:
	db: sqlite3.Connection = getattr(g, '_database', None)
	if db is not None:
		db.close()

if not exists(database):
	with app.app_context():
		db: sqlite3.Connection = getDbConnection()
		with app.open_resource('schema.sql', mode='r') as f:
			db.cursor().executescript(f.read())
		db.commit()

@app.route('/')
def homepage():
	db: sqlite3.Connection = getDbConnection()
	inizializzato: bool = int(db.cursor().execute('SELECT valore FROM configurazioni WHERE nome LIKE "inizializzato"').fetchone()[0]) == 1
	if not inizializzato:
		return redirect('inizia')
	return 'Benvenuto'

@app.route('/inizia')
def inizia():
	form: Inizializzazione = Inizializzazione(request.form)
	if request.method == 'POST' and form.validate():
		return 'Bravo!'
	return render_template('pages/inizia.html')

app.run('0.0.0.0', 80, True)