import sqlite3
import atexit
from secrets import token_hex
from flask import Flask, redirect, render_template, request, flash, url_for
from os.path import exists
from datetime import datetime
from classes.objectmodels.Configurazione import Configurazione
from classes.objectmodels.Aeroporto import Aeroporto
from classes.objectmodels.Aeromobile import Aeromobile
from classes.objectmodels.AeromobilePosseduto import AeromobilePosseduto
from classes.objectmodels.Utente import Utente
from classes.threads.ThreadManager import ThreadManager
from classes.threads.aggiornaMetar import aggiornaMetar
from classes.database.Database import Database

# Inizializzazione sistema

app: Flask = Flask(__name__)
app.secret_key = token_hex()
database: str = app.root_path+'/personal-va.db'

if not exists(database):
	with app.app_context():
		db: sqlite3.Connection = Database()
		with app.open_resource('schema.sql', mode='r') as f:
			db.executescript(f.read())
		db.commit()

threadManager: ThreadManager = ThreadManager()
atexit.register(threadManager.stopThreads)
threadManager.addThread(aggiornaMetar)
threadManager.startThreads()

# Definizione funzioni web

@app.route('/')
def homepage():
	inizializzato: bool = Configurazione.getConfigurazione('inizializzato', 'INTEGER') == 1
	if not inizializzato:
		return redirect(url_for('inizia'))
	return render_template('pages/homepage.html', utente=Utente(), aerei=AeromobilePosseduto.getAeromobiliPosseduti())

@app.route('/inizia', methods=['GET','POST'])
def inizia():
	inizializzato: bool = Configurazione.getConfigurazione('inizializzato', 'INTEGER') == 1
	if inizializzato:
		return redirect(url_for('homepage'))
	elencoAeroporti: list = [(aeroporto.id, f'{aeroporto.nome} ({aeroporto.codiceIcao})') for aeroporto in Aeroporto.getAeroporti()]
	from classes.forms.Inizializzazione import Inizializzazione
	form: Inizializzazione = Inizializzazione(elencoAeroporti, request.form)
	if request.method == 'POST' and form.validate():
		Configurazione.setConfigurazioni({'nome': form.nome.data, 'cognome': form.cognome.data, 'inizializzato': 1, 'intervallo_metar': form.intervalloMetar.data * 60})
		aereo: AeromobilePosseduto = AeromobilePosseduto()
		aereo.aeromobile = Aeromobile(1)
		aereo.aeroporto = Aeroporto(form.base.data)
		aereo.callsign = form.callsign.data
		aereo.carburante = aereo.aeromobile.capacitaSerbatoioL
		aereo.migliaPercorse = 0
		aereo.dataAcquisto = aereo.dataUltimoVolo = datetime.today()
		aereo.save()
		threadManager.restartThreads()
		return redirect(url_for('homepage'))
	return render_template('pages/inizia.html', form=form)

@app.route('/aeroporti', defaults={'idAeroporto': None})
@app.route('/aeroporti/<int:idAeroporto>')
def aeroporti(idAeroporto: int | None = None):
	if idAeroporto is None:
		return render_template('pages/aeroporti.html', aeroporti=Aeroporto.getAeroporti())
	aeroporto: Aeroporto = Aeroporto(idAeroporto)
	if aeroporto.id is None:
		flash('Id aeroporto non trovato', 'error')
		return redirect(url_for('aeroporti'))
	return render_template('pages/aeroporto.html', aeroporto=Aeroporto(idAeroporto))

@app.route('/aeromobili-posseduti', defaults={'idAeromobilePosseduto': None})
@app.route('/aeromobili-posseduti/<int:idAeromobilePosseduto>')
def aeromobiliPosseduti(idAeromobilePosseduto: int | None = None):
	if idAeromobilePosseduto is None:
		return render_template('pages/aeromobili_posseduti.html', aeromobiliPosseduti=AeromobilePosseduto.getAeromobiliPosseduti())
	aeromobilePosseduto: AeromobilePosseduto = AeromobilePosseduto(idAeromobilePosseduto)
	if aeromobilePosseduto.id is None:
		flash('Aeromobile posseduto non trovato', 'error')
		return redirect(url_for('aeromobiliPosseduti'))
	return render_template('pages/aeromobile_posseduto.html', aeromobilePosseduto=aeromobilePosseduto)

app.run('0.0.0.0', 80, debug=True, use_reloader=False)