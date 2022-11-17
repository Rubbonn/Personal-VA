import sqlite3
from datetime import datetime
from classes.database.Database import Database
from classes.objectmodels.Aeroporto import Aeroporto
from classes.objectmodels.PuntoPassaggio import PuntoPassaggio

class Missione:
	def __init__(self, id: int = None):
		self.id: int | None = None
		self.descrizione: str = ''
		self.aeroportoPartenza: Aeroporto | None = None
		self.aeroportoArrivo: Aeroporto | None = None
		self.dataCompletamento: datetime | None = None
		self.caricoBagagli: float | None = None
		self.passeggeri: list[float] = []
		self.puntiPassaggio: list[PuntoPassaggio] = []
		if id is None:
			return
		db: sqlite3.Connection = Database()
		riga: tuple = db.execute('SELECT * FROM missioni WHERE id = ?', (id,)).fetchone()
		if riga is None:
			return
		self.id = id
		self.descrizione = riga[1]
		self.aeroportoPartenza = Aeroporto(riga[2])
		self.aeroportoArrivo = Aeroporto(riga[3])
		self.dataCompletamento = datetime.fromisoformat(riga[4]) if riga[4] is not None else None
		self.caricoBagagli = riga[5]
		for passeggero, in db.execute('SELECT peso FROM passeggeri WHERE id_missione = ?', (self.id,)).fetchall():
			self.passeggeri.append(passeggero)
		for puntoPassaggio, in db.execute('SELECT id FROM punti_passaggio WHERE id_missione = ?', (self.id,)).fetchall():
			self.puntiPassaggio.append(PuntoPassaggio(puntoPassaggio))
	
	def add(self) -> bool:
		db: sqlite3.Connection = Database()
		c: sqlite3.Cursor = db.execute('INSERT INTO missioni (descrizione, aeroporto_partenza, aeroporto_arrivo, data_completamento, carico_bagagli) VALUES (?, ?, ?, ?, ?)', (self.descrizione, self.aeroportoPartenza.id, self.aeroportoArrivo.id, self.dataCompletamento.isoformat(' ', 'seconds') if self.dataCompletamento is not None else None, self.caricoBagagli))
		if c.rowcount < 1:
			return False
		self.id = c.lastrowid
		for passeggero in self.passeggeri:
			db.execute('INSERT INTO passeggeri (id_missione, peso) VALUES (?, ?)', (self.id, passeggero))
		db.commit()
		for puntoPassaggio in self.puntiPassaggio:
			puntoPassaggio.idMissione = self.id
			puntoPassaggio.add()
		return True
	
	def update(self) -> bool:
		db: sqlite3.Connection = Database()
		c: sqlite3.Cursor = db.execute('UPDATE missioni SET descrizione = ?, aeroporto_partenza = ?, aeroporto_arrivo = ?, data_completamento = ?, carico_bagagli = ? WHERE id = ?', (self.descrizione, self.aeroportoPartenza.id, self.aeroportoArrivo.id, self.dataCompletamento.isoformat(' ', 'seconds') if self.dataCompletamento is not None else None, self.caricoBagagli, self.id))
		if c.rowcount < 1:
			return False
		db.execute('DELETE FROM passeggeri WHERE id_missione = ?', (self.id,))
		for passeggero in self.passeggeri:
			db.execute('INSERT INTO passeggeri (id_missione, peso) VALUES (?, ?)', (self.id, passeggero))
		db.commit()
		for puntoPassaggio in self.puntiPassaggio:
			puntoPassaggio.idMissione = self.id
			puntoPassaggio.save()
		return True
	
	def save(self) -> bool:
		if self.id is None:
			return self.add()
		return self.update()
	
	@staticmethod
	def getMissioniDisponibili():
		db: sqlite3.Connection = Database()
		return [Missione(id) for id, in db.execute('SELECT id FROM missioni WHERE data_completamento IS NULL')]
	
	@staticmethod
	def getMissioniCompletate(dateFrom: datetime = None, dateTo: datetime = None):
		db: sqlite3.Connection = Database()
		query: str = 'SELECT id FROM missioni WHERE data_completamento IS NOT NULL'
		params: tuple = ()
		if dateFrom is not None and dateTo is not None and dateFrom < dateTo:
			query += ' AND data_completamento > ? AND data_completamento < ?'
			params = (dateFrom.isoformat(' ', 'seconds'), dateTo.isoformat(' ', 'seconds'))
		return [Missione(id) for id, in db.execute(query, params)]