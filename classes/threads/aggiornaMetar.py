from threading import Event
import sqlite3
from classes.objectmodels.Configurazione import Configurazione
from classes.objectmodels.Aeroporto import Aeroporto
from classes.objectmodels.Metar import Metar
from classes.database.database import Database
from time import sleep
from datetime import datetime
from urllib.request import urlopen

def aggiornaMetar(shutdownEvent: Event, database: str) -> None:
	db: sqlite3.Connection = Database()
	intervallo: int = Configurazione.getConfigurazione('intervallo_metar', 'INTEGER')
	elencoAeroporti: list[Aeroporto] = Aeroporto.getAeroporti()
	elencoAeroporti: list[str] = [aeroporto.codice_icao for aeroporto in elencoAeroporti if len(aeroporto.codice_icao) > 0]
	while True:
		url = 'https://metar.vatsim.net/' + ','.join(elencoAeroporti)
		try:
			with urlopen(url) as risposta:
				metars: list[str] = risposta.read().decode().split('\n')
				for metar in metars:
					aeroporto: Aeroporto = Aeroporto.getAeroportoByIcao(metar[0:4])
					if aeroporto is None:
						continue
					metarObj: Metar = Metar()
					metarObj.id_aeroporto = aeroporto.id
					metarObj.metar = metar
					metarObj.ultimo_aggiornamento = datetime.today()
					metarObj.ultimo_errore = ''
					metarObj.save()
		except BaseException as e:
			for metar in Metar.getMetars():
				metar.ultimo_errore = str(e)
				metar.save()
		for i in range(intervallo):
			if shutdownEvent.is_set():
				break
			sleep(1)
		if shutdownEvent.is_set():
				break
	db.close()