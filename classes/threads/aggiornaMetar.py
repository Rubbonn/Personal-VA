from threading import Event
import sqlite3
from classes.objectmodels.Configurazione import Configurazione
from classes.objectmodels.Aeroporto import Aeroporto
from classes.objectmodels.Metar import Metar
from time import sleep
from datetime import datetime
from urllib.request import urlopen

def aggiornaMetar(shutdownEvent: Event, database: str) -> None:
	db: sqlite3.Connection = sqlite3.connect(database)
	intervallo: int = Configurazione(db).getConfigurazione('intervallo_metar', 'INTEGER')
	elencoAeroporti: list[Aeroporto] = Aeroporto.getAeroporti(db)
	elencoAeroporti: list[str] = [aeroporto.codice_icao for aeroporto in elencoAeroporti if len(aeroporto.codice_icao) > 0]
	while not shutdownEvent.is_set():
		url = 'https://metar.vatsim.net/' + ','.join(elencoAeroporti)
		try:
			with urlopen(url) as risposta:
				metars: list[str] = risposta.read().decode().split('\n')
				for metar in metars:
					aeroporto: Aeroporto = Aeroporto.getAeroportoByIcao(db, metar[0:4])
					if aeroporto is None:
						continue
					metarObj: Metar = Metar(db)
					metarObj.id_aeroporto = aeroporto.id
					metarObj.metar = metar
					metarObj.ultimo_aggiornamento = datetime.today()
					metarObj.ultimo_errore = ''
					metarObj.save()
		except BaseException as e:
			for metar in Metar.getMetars(db):
				metar.ultimo_errore = str(e)
				metar.save()
		print([(metar.metar, metar.ultimo_aggiornamento.isoformat(' ','seconds'), metar.ultimo_errore) for metar in Metar.getMetars(db)])
		sleep(intervallo)
	db.close()