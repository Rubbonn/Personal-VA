import sqlite3
from datetime import datetime
from classes.database.Database import Database

class Metar:
	def __init__(self, id_aeroporto: int = None):
		self.id_aeroporto: int | None = None
		self.metar: str = ''
		self.ultimoAggiornamento: datetime | None = None
		self.ultimoErrore: str = ''
		if id_aeroporto is None:
			return
		db: sqlite3.Connection = Database()
		riga: tuple = db.execute('SELECT * FROM metar WHERE id_aeroporto = ?', (id_aeroporto,)).fetchone()
		if riga is None:
			return
		self.id_aeroporto = id_aeroporto
		self.metar = riga[1]
		self.ultimoAggiornamento = datetime.fromisoformat(riga[2])
		self.ultimoErrore = riga[3]
	
	def save(self):
		db: sqlite3.Connection = Database()
		db.execute('INSERT OR REPLACE INTO metar VALUES (?, ?, ?, ?)', (self.id_aeroporto, self.metar, self.ultimoAggiornamento.isoformat(' ', 'seconds'), self.ultimoErrore))
		db.commit()
	
	@staticmethod
	def getMetars():
		db: sqlite3.Connection = Database()
		metar: list[Metar] = []
		for id_aeroporto, in db.execute('SELECT id_aeroporto FROM metar').fetchall():
			metar.append(Metar(id_aeroporto))
		return metar