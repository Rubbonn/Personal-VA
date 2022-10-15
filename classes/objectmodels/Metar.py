import sqlite3
from datetime import datetime

class Metar:
	__db: sqlite3.Connection = None
	id_aeroporto: int | None = None
	metar: str = ''
	ultimo_aggiornamento: datetime | None = None
	ultimo_errore: str = ''

	def __init__(self, db: sqlite3.Connection, id_aeroporto: int = None):
		self.__db = db
		if id_aeroporto is None:
			return
		riga: tuple = self.__db.execute('SELECT * FROM metar WHERE id_aeroporto = ?', (id_aeroporto,)).fetchone()
		if riga is None:
			return
		self.id_aeroporto = id_aeroporto
		self.metar = riga[1]
		self.ultimo_aggiornamento = datetime.fromisoformat(riga[2])
		self.ultimo_errore = riga[3]
	
	def save(self):
		self.__db.execute('INSERT OR REPLACE INTO metar VALUES (?, ?, ?, ?)', (self.id_aeroporto, self.metar, self.ultimo_aggiornamento.isoformat(' ', 'seconds'), self.ultimo_errore))
		self.__db.commit()
	
	@staticmethod
	def getMetars(db: sqlite3.Connection):
		metar: list[Metar] = []
		for id_aeroporto in db.execute('SELECT id_aeroporto FROM metar').fetchall():
			metar.append(Metar(db, id_aeroporto[0]))
		return metar