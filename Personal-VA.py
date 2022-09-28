from distutils.command.config import config
from flask import Flask, g, redirect, render_template, request
import sqlite3
from os.path import exists
from classes.forms.Inizializzazione import Inizializzazione
from classes.objectmodels.Configurazione import Configurazione

app: Flask = Flask(__name__)
database: str = app.root_path+'/personal-va.db'

def getDbConnection() -> sqlite3.Connection:
	db: sqlite3.Connection = getattr(g, '_database', None)
	if db is None:
		db = g._database = sqlite3.connect(database)
	return db

def getConfigurationObject() -> Configurazione:
	configurazioni: Configurazione = getattr(g, '_configurazioni', None)
	if configurazioni is None:
		db: sqlite3.Connection = getDbConnection()
		configurazioni = g._configurazioni = Configurazione(db)
	return configurazioni

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
	configurazioni: Configurazione = getConfigurationObject()
	inizializzato: bool = configurazioni.getConfigurazione('inizializzato', 'INTEGER') == 1
	if not inizializzato:
		return redirect('inizia')
	return render_template('pages/homepage.html')

@app.route('/inizia', methods=['GET','POST'])
def inizia():
	db: sqlite3.connection = getDbConnection()
	configurazioni: Configurazione = getConfigurationObject()
	inizializzato: bool = configurazioni.getConfigurazione('inizializzato', 'INTEGER') == 1
	if inizializzato:
		return redirect('/')
	elencoAeroporti: list = db.cursor().execute('SELECT id, nome || " (" || codice_icao || ")" FROM aeroporti ORDER BY nome ASC').fetchall()
	form: Inizializzazione = Inizializzazione(elencoAeroporti, request.form)
	if request.method == 'POST' and form.validate():
		cursore: sqlite3.Cursor = db.cursor()
		configurazioni.setConfigurazioni({'nome': form.nome.data, 'cognome': form.cognome.data, 'inizializzato': 1})
		cursore.execute('INSERT INTO aeromobili_posseduti ("id", "id_aeromobile", "aeroporto_attuale", "carburante", "miglia_percorse", "data_acquisto", "data_ultimo_volo") VALUES (1, 1, ?, 212, 0, date(), "")', (form.base.data,))
		db.commit()
		return redirect('/')
	return render_template('pages/inizia.html', form=form)

app.run('0.0.0.0', 80, debug=True)