from datetime import datetime
from flask import Flask, redirect, render_template, request
import sqlite3
from os.path import exists
from classes.forms.Inizializzazione import Inizializzazione
from classes.objectmodels.Configurazione import Configurazione
from classes.objectmodels.Aeroporto import Aeroporto
from classes.objectmodels.Aeromobile import Aeromobile
from classes.objectmodels.AeromobilePosseduto import AeromobilePosseduto
from classes.objectmodels.Utente import Utente
import atexit
from classes.threads.ThreadManager import ThreadManager
from classes.threads.aggiornaMetar import aggiornaMetar
from classes.database.Database import Database

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
	return render_template('pages/homepage.html', utente=Utente(), aerei=AeromobilePosseduto.getAeromobiliPosseduti())

@app.route('/inizia', methods=['GET','POST'])
def inizia():
	inizializzato: bool = Configurazione.getConfigurazione('inizializzato', 'INTEGER') == 1
	if inizializzato:
		return redirect('/')
	elencoAeroporti: list = [(aeroporto.id, f'{aeroporto.nome} ({aeroporto.codiceIcao})') for aeroporto in Aeroporto.getAeroporti()]
	form: Inizializzazione = Inizializzazione(elencoAeroporti, request.form)
	if request.method == 'POST' and form.validate():
		Configurazione.setConfigurazioni({'nome': form.nome.data, 'cognome': form.cognome.data, 'inizializzato': 1, 'intervallo_metar': form.intervalloMetar.data * 60})
		aereo: AeromobilePosseduto = AeromobilePosseduto()
		aereo.aeromobile = Aeromobile(1)
		aereo.aeroporto = Aeroporto(form.base.data)
		aereo.callsign = form.callsign.data
		aereo.carburante = aereo.aeromobile.capacita_serbatoio_l
		aereo.miglia_percorse = 0
		aereo.data_acquisto = aereo.data_ultimo_volo = datetime.today()
		aereo.save()
		threadManager.restartThreads()
		return redirect('/')
	return render_template('pages/inizia.html', form=form)

@app.route('/aeroporti', defaults={'idAeroporto': None})
@app.route('/aeroporti/<int:idAeroporto>')
def aeroporti(idAeroporto: int | None = None):
	if idAeroporto is None:
		return render_template('pages/aeroporti.html', aeroporti=Aeroporto.getAeroporti())
	else:
		# Fare prima dei controlli che l'id sia valido ed esista
		return render_template('pages/aeroporto.html', aeroporto=Aeroporto(idAeroporto))

app.run('0.0.0.0', 80, debug=True, use_reloader=False)