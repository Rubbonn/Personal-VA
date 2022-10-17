from operator import truediv
import sqlite3
from classes.database.database import Database
from classes.objectmodels.Aeromobile import Aeromobile
from classes.objectmodels.Aeroporto import Aeroporto
from datetime import datetime
class AeromobilePosseduto:
	id: int | None = None
	aeromobile: Aeromobile | None = None
	aeroporto_attuale: Aeroporto | None = None
	carburante: float | None = None
	miglia_percorse: float | None = None
	data_acquisto: datetime | None = None
	data_ultimo_volo: datetime | None = None

	def __init__(self, id: int = None):
		db: sqlite3.Connection = Database()
		if id is None:
			return
		riga: tuple = db.execute('SELECT * FROM aeromobili_posseduti WHERE id = ?', (id,)).fetchone()
		if riga is None:
			return
		self.id = id
		self.aeromobile = Aeromobile(riga[1])
		self.aeroporto_attuale = Aeroporto(riga[2])
		self.carburante = riga[3]
		self.miglia_percorse = riga[4]
		self.data_acquisto = datetime.fromisoformat(riga[5])
		self.data_ultimo_volo = datetime.fromisoformat(riga[6])
	
	def add(self) -> bool:
		db: sqlite3.Connection = Database()
		c: sqlite3.Cursor = db.execute('INSERT INTO aeromobili_posseduti (id_aeromobile, aeroporto_attuale, carburante, miglia_percorse, data_acquisto, data_ultimo_volo) VALUES (?, ?, ?, ?, ?, ?)', (self.aeromobile.id, self.aeroporto_attuale.id, self.carburante, self.miglia_percorse, self.data_acquisto.isoformat(' ', 'seconds'), self.data_ultimo_volo.isoformat(' ', 'seconds')))
		db.commit()
		if c.rowcount >= 1:
			self.id = c.lastrowid
			return True
		return False
	
	def update(self) -> bool:
		db: sqlite3.Connection = Database()
		c: sqlite3.Cursor = db.execute('UPDATE aeromobili_posseduti SET id_aeromobile = ?, aeroporto_attuale = ?, carburante = ?, miglia_percorse = ?, data_acquisto = ?, data_ultimo_volo = ? WHERE id = ?', (self.aeromobile.id, self.aeroporto_attuale.id, self.carburante, self.miglia_percorse, self.data_acquisto.isoformat(' ', 'seconds'), self.data_ultimo_volo.isoformat(' ', 'seconds'), self.id))
		db.commit()
		return c.rowcount >= 1
	
	def save(self) -> bool:
		if self.id is None:
			return self.add()
		return self.update()
	
	@staticmethod
	def getAeromobiliPosseduti() -> list['AeromobilePosseduto']:
		db: sqlite3.Connection = Database()
		risultato: list[tuple] = db.execute('SELECT id FROM aeromobili_posseduti').fetchall()
		if risultato is None:
			return []
		return [AeromobilePosseduto(riga[0]) for riga in risultato]