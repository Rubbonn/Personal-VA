import sqlite3
from datetime import datetime
from classes.database.Database import Database
from classes.objectmodels.Aeroporto import Aeroporto
from classes.objectmodels.PuntoPassaggio import PuntoPassaggio

class Missione:
	id: int | None = None
	aeroportoPartenza: int | None = None
	aeroportoArrivo: int | None = None
	dataCompletamento: datetime | None = None
	caricoBagagli: float | None = None
	passeggeri: list[float] = []
	puntiPassaggio: list[PuntoPassaggio] = []

	def __init__(self, id: int = None):
		db: sqlite3.Connection = Database()
		if id is None:
			return
		riga: tuple = db.execute('SELECT * FROM missioni WHERE id = ?', (id,)).fetchone()
		if riga is None:
			return
		self.id = id
		self.aeroportoPartenza = Aeroporto(riga[1])
		self.aeroportoArrivo = Aeroporto(riga[2])
		self.dataCompletamento = datetime.fromisoformat(riga[3]) if riga[3] is not None else None
		self.caricoBagagli = riga[4]
		for passeggero, in db.execute('SELECT peso FROM passeggeri WHERE id_missione = ?', (self.id,)).fetchall():
			self.passeggeri.append(passeggero)
		for puntoPassaggio, in db.execute('SELECT id FROM punti_passaggio WHERE id_missione = ?', (self.id,)).fetchall():
			self.puntiPassaggio.append(PuntoPassaggio(puntoPassaggio))
	
	def add(self) -> bool:
		db: sqlite3.Connection = Database()
		c: sqlite3.Cursor = db.execute('INSERT INTO missioni (aeroporto_partenza, aeroporto_arrivo, data_completamento, carico_bagagli) VALUES (?, ?, ?, ?)', (self.aeroportoPartenza.id, self.aeroportoArrivo.id, self.dataCompletamento.isoformat(' ', 'seconds') if self.dataCompletamento is not None else None, self.caricoBagagli))
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
		c: sqlite3.Cursor = db.execute('UPDATE missioni SET aeroporto_partenza = ?, aeroporto_arrivo = ?, data_completamento = ?, carico_bagagli = ? WHERE id = ?', (self.aeroportoPartenza.id, self.aeroportoArrivo.id, self.dataCompletamento.isoformat(' ', 'seconds') if self.dataCompletamento is not None else None, self.caricoBagagli, self.id))
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