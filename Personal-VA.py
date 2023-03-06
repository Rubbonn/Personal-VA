import sqlite3
import atexit
from secrets import token_hex
from flask import Flask, redirect, render_template, request, Response, flash, url_for, jsonify
from os.path import exists
from datetime import datetime
from classes.objectmodels.Configurazione import Configurazione
from classes.objectmodels.Aeroporto import Aeroporto
from classes.objectmodels.Aeromobile import Aeromobile
from classes.objectmodels.AeromobilePosseduto import AeromobilePosseduto
from classes.objectmodels.Utente import Utente
from classes.objectmodels.Transazione import Transazione
from classes.objectmodels.Volo import Volo
from classes.threads.ThreadManager import ThreadManager
from classes.threads.aggiornaMetar import aggiornaMetar
from classes.database.Database import Database
from classes.provider.PrezziCarburanteProvider import PrezziCarburanteProvider

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
		db.close()

threadManager: ThreadManager = ThreadManager()
atexit.register(threadManager.stopThreads)
aggiornaMetarThreadIndice: int = threadManager.addThread(aggiornaMetar)
threadManager.startThreads()

# Definizione funzioni web

@app.before_request
def controlloInizializzazione():
	if request.endpoint == 'inizia' or request.endpoint == 'static':
		return
	inizializzato: bool = Configurazione.getConfigurazione('inizializzato', 'INTEGER') == 1
	if not inizializzato:
		return redirect(url_for('inizia'))

@app.route('/')
def homepage():
	return render_template('pages/homepage.html', utente=Utente(), aerei=AeromobilePosseduto.getAeromobiliPosseduti(), ultimeTransazioni=Transazione.getTransazioni()[:10])

@app.route('/inizia', methods=['GET','POST'])
def inizia():
	inizializzato: bool = Configurazione.getConfigurazione('inizializzato', 'INTEGER') == 1
	if inizializzato:
		return redirect(url_for('homepage'))
	elencoAeroporti: list = [(aeroporto.id, f'{aeroporto.nome} ({aeroporto.codiceIcao})') for aeroporto in Aeroporto.getAeroporti()]
	from classes.forms.Inizializzazione import Inizializzazione
	form: Inizializzazione = Inizializzazione(elencoAeroporti, request.form)
	if request.method == 'POST' and form.validate():
		Configurazione.setConfigurazioni({'nome': form.nome.data, 'cognome': form.cognome.data, 'inizializzato': 1, 'intervallo_metar': form.intervalloMetar.data})
		aereo: AeromobilePosseduto = AeromobilePosseduto()
		aereo.aeromobile = Aeromobile(1)
		aereo.aeroporto = Aeroporto(form.base.data)
		aereo.callsign = form.callsign.data
		aereo.carburante = aereo.aeromobile.capacitaSerbatoioL
		aereo.migliaPercorse = 0
		aereo.dataAcquisto = aereo.dataUltimoVolo = datetime.today()
		aereo.save()
		trans: Transazione = Transazione()
		trans.causale = 'Importo iniziale'
		trans.valore = 100000
		trans.data = datetime.today()
		trans.save()
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

@app.route('/impostazioni', methods=['GET','POST'])
def impostazioni():
	from classes.forms.Impostazioni import Impostazioni
	form: Impostazioni = Impostazioni(request.form)
	if request.method == 'POST' and form.validate():
		Configurazione.setConfigurazioni({'intervallo_metar': form.intervalloMetar.data})
		threadManager.restartThread(aggiornaMetarThreadIndice)
	return render_template('pages/impostazioni.html', form=form, configurazioni=Configurazione.getAllConfigurazioni())

@app.route('/nuovo-volo', methods=['GET', 'POST'])
def nuovoVolo():
	from classes.forms.NuovoVolo import NuovoVolo
	nuovoVoloForm: NuovoVolo = NuovoVolo(request.form)
	if request.method == 'POST' and nuovoVoloForm.validate():
		vecchioVolo: Volo = Volo.getUltimoVoloDaFare()
		if vecchioVolo.id is not None:
			vecchioVolo.delete()
		nuovoVolo: Volo = Volo()
		nuovoVolo.aeromobilePosseduto = AeromobilePosseduto(nuovoVoloForm.aeromobile.data)
		nuovoVolo.aeroportoPartenza = Aeroporto(nuovoVoloForm.aeroportoPartenza.data)
		nuovoVolo.aeroportoArrivo = Aeroporto(nuovoVoloForm.aeroportoArrivo.data)
		nuovoVolo.dataCreazione = datetime.now()
		nuovoVolo.save()
		if 'save' in request.form:
			flash('Volo salvato e pronto', 'success')
			return redirect(url_for('homepage'))
		elif 'saveAndStart' in request.form:
			return redirect(url_for('eseguiVolo'))
	return render_template('pages/nuovo_volo.html', nuovoVoloForm=nuovoVoloForm, voloEsistente=True if Volo.getUltimoVoloDaFare().id is not None else False)

@app.route('/esegui-volo')
def eseguiVolo():
	pass

@app.route('/ajax/getPrezzoCarburante/<int:idAeroporto>/<int:idCarburante>')
def getPrezzoCarburante(idAeroporto:int, idCarburante:int):
	return jsonify(PrezziCarburanteProvider().getPrezzoCarburante(idAeroporto, idCarburante))

@app.route('/ajax/rifornisciAereo', methods=['POST'])
def rifornisciAereo():
	try:
		idAeromobilePosseduto: int = request.form.get('idAeromobilePosseduto', None, int)
		aeromobilePosseduto: AeromobilePosseduto = AeromobilePosseduto(idAeromobilePosseduto)
		if idAeromobilePosseduto is None or aeromobilePosseduto.id is None:
			raise Exception()
	except:
		return jsonify({'stato': False, 'errore': 'Id aeromobile posseduto sbagliato'})
	try:
		volume: float = request.form.get('volume', None, float)
		if volume is None or volume <= 0:
			raise Exception()
	except:
		return jsonify({'stato': False, 'errore': 'Volume carburante sbagliato'})
	if volume > aeromobilePosseduto.aeromobile.capacitaSerbatoioL - aeromobilePosseduto.carburante:
		return jsonify({'stato': False, 'errore': 'Volume carburante oltre il massimo rifornibile'})
	costoCarburante: float = PrezziCarburanteProvider().getPrezzoCarburante(aeromobilePosseduto.aeroporto.id, aeromobilePosseduto.aeromobile.idCarburante)
	if costoCarburante * volume > Utente().saldo:
		return jsonify({'stato': False, 'errore': 'Non hai abbastanza soldi'})
	aeromobilePosseduto.carburante += volume
	aeromobilePosseduto.save()
	transazione: Transazione = Transazione()
	transazione.causale = f'Rifornimento carburante aeromobile {aeromobilePosseduto.callsign} di {volume}L'
	transazione.valore = round(costoCarburante * volume, 2)
	transazione.data = datetime.today()
	transazione.save()
	Utente.aggiornaSaldo(-transazione.valore)
	return jsonify({'stato': True})

@app.route('/ajax/getInfoAeromobilePosseduto/<int:idAeromobilePosseduto>')
def getInfoAeromobilePosseduto(idAeromobilePosseduto:int):
	aeromobile: AeromobilePosseduto = AeromobilePosseduto(idAeromobilePosseduto)
	if aeromobile.id is None:
		return jsonify(False)
	from jsonpickle import encode
	return Response(encode(aeromobile, False), mimetype='application/json')

@app.route('/ajax/getInfoAeroporto/<int:idAeroporto>')
def getInfoAeroporto(idAeroporto:int):
	aeroporto: Aeroporto = Aeroporto(idAeroporto)
	if aeroporto.id is None:
		return jsonify(False)
	from jsonpickle import encode
	return Response(encode(aeroporto, False), mimetype='application/json')

app.run('0.0.0.0', 80, debug=True, use_reloader=False)