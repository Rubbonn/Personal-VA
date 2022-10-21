import sqlite3
from classes.database.Database import Database
from classes.objectmodels.Aeromobile import Aeromobile
from classes.objectmodels.Aeroporto import Aeroporto
from datetime import datetime
class AeromobilePosseduto:
	id: int | None = None
	aeromobile: Aeromobile | None = None
	aeroporto: Aeroporto | None = None
	callsign: str = ''
	carburante: float | None = None
	migliaPercorse: float | None = None
	dataAcquisto: datetime | None = None
	dataUltimoVolo: datetime | None = None

	def __init__(self, id: int = None):
		db: sqlite3.Connection = Database()
		if id is None:
			return
		riga: tuple = db.execute('SELECT * FROM aeromobili_posseduti WHERE id = ?', (id,)).fetchone()
		if riga is None:
			return
		self.id = id
		self.aeromobile = Aeromobile(riga[1])
		self.aeroporto = Aeroporto(riga[2])
		self.callsign = riga[3]
		self.carburante = riga[4]
		self.migliaPercorse = riga[5]
		self.dataAcquisto = datetime.fromisoformat(riga[6])
		self.dataUltimoVolo = datetime.fromisoformat(riga[7])
	
	def add(self) -> bool:
		db: sqlite3.Connection = Database()
		c: sqlite3.Cursor = db.execute('INSERT INTO aeromobili_posseduti (id_aeromobile, aeroporto, callsign, carburante, miglia_percorse, data_acquisto, data_ultimo_volo) VALUES (?, ?, ?, ?, ?, ?, ?)', (self.aeromobile.id, self.aeroporto.id, self.callsign, self.carburante, self.migliaPercorse, self.dataAcquisto.isoformat(' ', 'seconds'), self.dataUltimoVolo.isoformat(' ', 'seconds')))
		db.commit()
		if c.rowcount >= 1:
			self.id = c.lastrowid
			return True
		return False
	
	def update(self) -> bool:
		db: sqlite3.Connection = Database()
		c: sqlite3.Cursor = db.execute('UPDATE aeromobili_posseduti SET id_aeromobile = ?, aeroporto = ?, callsign = ?, carburante = ?, miglia_percorse = ?, data_acquisto = ?, data_ultimo_volo = ? WHERE id = ?', (self.aeromobile.id, self.aeroporto.id, self.callsign, self.carburante, self.migliaPercorse, self.dataAcquisto.isoformat(' ', 'seconds'), self.dataUltimoVolo.isoformat(' ', 'seconds'), self.id))
		db.commit()
		return c.rowcount >= 1
	
	def save(self) -> bool:
		if self.id is None:
			return self.add()
		return self.update()
	
	def getFormattedCarburante(self) -> str:
		return f'{self.carburante:,.2f} L'
	
	def getFormattedMigliaPercorse(self) -> str:
		return f'{self.migliaPercorse:,.2f} NM'
	
	@staticmethod
	def getAeromobiliPosseduti() -> list['AeromobilePosseduto']:
		db: sqlite3.Connection = Database()
		risultato: list[tuple] = db.execute('SELECT id FROM aeromobili_posseduti').fetchall()
		if risultato is None:
			return []
		return [AeromobilePosseduto(riga[0]) for riga in risultato]