from threading import Event
import sqlite3
from classes.objectmodels.Configurazione import Configurazione
from classes.objectmodels.Aeroporto import Aeroporto
from classes.objectmodels.Metar import Metar
from classes.database.Database import Database
from time import sleep
from datetime import datetime
from urllib.request import urlopen

def aggiornaMetar(shutdownEvent: Event) -> None:
	db: sqlite3.Connection = Database()
	intervallo: int = Configurazione.getConfigurazione('intervallo_metar', 'INTEGER') * 60
	elencoAeroporti: list[Aeroporto] = Aeroporto.getAeroporti()
	elencoAeroporti: list[str] = [aeroporto.codiceIcao for aeroporto in elencoAeroporti if len(aeroporto.codiceIcao) > 0]
	url: str = 'https://metar.vatsim.net/' + ','.join(elencoAeroporti)
	while True:
		for i in range(intervallo):
			if shutdownEvent.is_set():
				break
			sleep(1)
		if shutdownEvent.is_set():
			break
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
					metarObj.ultimoAggiornamento = datetime.today()
					metarObj.ultimoErrore = ''
					metarObj.save()
		except BaseException as e:
			for metar in Metar.getMetars():
				metar.ultimoErrore = str(e)
				metar.save()
	db.close()