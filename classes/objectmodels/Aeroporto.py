import sqlite3
from math import sqrt, pi, sin, cos, atan2
from classes.objectmodels.Metar import Metar
from classes.database.database import Database

class Aeroporto:
	id: int | None = None
	codice_icao: str = ''
	nome: str = ''
	citta: str = ''
	nazione: str = ''
	latitudine: float | None = None
	longitudine: float | None = None

	def __init__(self, id: int = None):
		db: sqlite3.Connection = Database()
		if id is None:
			return
		riga: tuple = db.execute('SELECT * FROM aeroporti WHERE id = ?', (id,)).fetchone()
		if riga is None:
			return
		self.id = id
		self.codice_icao = riga[1]
		self.nome = riga[2]
		self.citta = riga[3]
		self.nazione = riga[4]
		self.latitudine = riga[5]
		self.longitudine = riga[6]
	
	@staticmethod
	def getAeroporti() -> list['Aeroporto']:
		db: sqlite3.Connection = Database()
		risultati: list[tuple] = db.execute('SELECT id FROM aeroporti ORDER BY nome ASC').fetchall()
		if risultati is None:
			return []
		return [Aeroporto(id[0]) for id in risultati]
	
	@staticmethod
	def getAeroportoByIcao(icao: str) -> 'Aeroporto | None':
		db: sqlite3.Connection = Database()
		risultato: tuple = db.execute('SELECT id FROM aeroporti WHERE codice_icao LIKE ?', (icao,)).fetchone()
		if risultato is None:
			return None
		return Aeroporto(risultato[0])
	
	def calcolaDistanza(self, latitudine: float, longitudine: float) -> float:
		if latitudine < -90 or latitudine > 90 or longitudine < -180 or longitudine > 180:
			raise Exception('Le coordinate non sono valide')
		R: float = 3440.0647948 # Radius of earth in NM
		dLat: float = latitudine * pi / 180 - self.latitudine * pi / 180
		dLon: float = longitudine * pi / 180 - self.longitudine * pi / 180
		a: float = sin(dLat/2) * sin(dLat/2) + cos(self.latitudine * pi / 180) * cos(latitudine * pi / 180) * sin(dLon/2) * sin(dLon/2)
		c: float = 2 * atan2(sqrt(a), sqrt(1-a))
		d: float = R * c
		return d
	
	def getMetar(self) -> Metar:
		return Metar(self.id)