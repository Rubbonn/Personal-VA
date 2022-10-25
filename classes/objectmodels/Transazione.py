import sqlite3
from datetime import datetime
from classes.database.Database import Database

class Transazione:
	id: int | None = None
	causale: str = ''
	valore: float | None = None
	data: datetime | None = None

	def __init__(self, id: int = None):
		db: sqlite3.Connection = Database()
		if id is None:
			return
		riga: tuple = db.execute('SELECT * FROM transazioni WHERE id = ?', (id,)).fetchone()
		if riga is None:
			return
		self.id = id
		self.causale = riga[1]
		self.valore = riga[2]
		self.data = datetime.fromisoformat(riga[3])
	
	def save(self):
		db: sqlite3.Connection = Database()
		db.execute('INSERT OR REPLACE INTO transazioni VALUES (?, ?, ?, ?)', (self.id, self.causale, self.valore, self.data.isoformat(' ', 'seconds')))
		db.commit()
	
	def getFormattedValore(self):
		return f'{self.valore:+,.2f} €'
	
	@staticmethod
	def getTransazioni(dateFrom: datetime | None = None, dateTo: datetime | None = None) -> list['Transazione']:
		db: sqlite3.Connection = Database()
		sql: str = 'SELECT id FROM transazioni'
		if dateFrom is not None and dateTo is not None and dateFrom <= dateTo:
			sql += f' WHERE data >= {dateFrom.isoformat(" ", "seconds")} AND data <= {dateTo.isoformat(" ", "seconds")}'
		sql += ' ORDER BY data DESC'
		risultato: list[tuple] | None = db.execute(sql).fetchall()
		if risultato is None:
			return []
		return [Transazione(id[0]) for id in risultato]