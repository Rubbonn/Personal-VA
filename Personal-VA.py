from datetime import datetime
from flask import Flask, g, redirect, render_template, request
import sqlite3
from os.path import exists
from classes.forms.Inizializzazione import Inizializzazione
from classes.objectmodels.Configurazione import Configurazione
from classes.objectmodels.Aeroporto import Aeroporto
from classes.objectmodels.Aeromobile import Aeromobile
from classes.objectmodels.AeromobilePosseduto import AeromobilePosseduto
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
	inizializzato: bool = Configurazione.getConfigurazione('inizializzato', 'INTEGER') == 1
	if inizializzato:
		return redirect('/')
	elencoAeroporti: list = [(aeroporto.id, f'{aeroporto.nome} ({aeroporto.codice_icao})') for aeroporto in Aeroporto.getAeroporti()]
	form: Inizializzazione = Inizializzazione(elencoAeroporti, request.form)
	if request.method == 'POST' and form.validate():
		Configurazione.setConfigurazioni({'nome': form.nome.data, 'cognome': form.cognome.data, 'inizializzato': 1, 'intervallo_metar': form.intervalloMetar.data * 60})
		aereo: AeromobilePosseduto = AeromobilePosseduto()
		aereo.aeromobile = Aeromobile(1)
		aereo.aeroporto_attuale = Aeroporto(form.base.data)
		aereo.carburante = aereo.aeromobile.capacita_serbatoio_l
		aereo.miglia_percorse = 0
		aereo.data_acquisto = aereo.data_ultimo_volo = datetime.today()
		aereo.save()
		threadManager.restartThreads()
		return redirect('/')
	return render_template('pages/inizia.html', form=form)

app.run('0.0.0.0', 80, debug=True, use_reloader=False)