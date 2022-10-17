from flask import Flask, g, redirect, render_template, request
import sqlite3
from os.path import exists
from classes.forms.Inizializzazione import Inizializzazione
from classes.objectmodels.Configurazione import Configurazione
from classes.objectmodels.Aeroporto import Aeroporto
import atexit
from classes.threads.ThreadManager import ThreadManager
from classes.threads.aggiornaMetar import aggiornaMetar
from classes.database.database import Database

# Inizializzazione sistema

app: Flask = Flask(__name__)
database: str = app.root_path+'/personal-va.db'

if not exists(database):
	with app.app_context():
		db: sqlite3.Connection = Database()
		with app.open_resource('schema.sql', mode='r') as f:
			db.executescript(f.read())
		db.commit()

threadManager: ThreadManager = ThreadManager(database)
atexit.register(threadManager.stopThreads)
threadManager.addThread(aggiornaMetar)
threadManager.startThreads()

# Definizione funzioni web

@app.route('/')
def homepage():
	inizializzato: bool = Configurazione.getConfigurazione('inizializzato', 'INTEGER') == 1
	if not inizializzato:
		return redirect('inizia')
	return render_template('pages/homepage.html')

@app.route('/inizia', methods=['GET','POST'])
def inizia():
	db: sqlite3.Connection = Database()
	inizializzato: bool = Configurazione.getConfigurazione('inizializzato', 'INTEGER') == 1
	if inizializzato:
		return redirect('/')
	elencoAeroporti: list = [(aeroporto.id, f'{aeroporto.nome} ({aeroporto.codice_icao})') for aeroporto in Aeroporto.getAeroporti()]
	form: Inizializzazione = Inizializzazione(elencoAeroporti, request.form)
	if request.method == 'POST' and form.validate():
		Configurazione.setConfigurazioni({'nome': form.nome.data, 'cognome': form.cognome.data, 'inizializzato': 1, 'intervallo_metar': form.intervalloMetar.data * 60})
		db.execute('INSERT INTO aeromobili_posseduti ("id", "id_aeromobile", "aeroporto_attuale", "carburante", "miglia_percorse", "data_acquisto", "data_ultimo_volo") VALUES (1, 1, ?, 212, 0, date(), "")', (form.base.data,))
		db.commit()
		threadManager.restartThreads()
		return redirect('/')
	return render_template('pages/inizia.html', form=form)

app.run('0.0.0.0', 80, debug=True, use_reloader=False)