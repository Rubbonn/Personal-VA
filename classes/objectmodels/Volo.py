import sqlite3
from datetime import datetime
from classes.database.Database import Database
from classes.objectmodels.AeromobilePosseduto import AeromobilePosseduto
from classes.objectmodels.Aeroporto import Aeroporto

class Volo:
	def __init__(self, id: int = None):
		self.id: int | None = None
		self.aeromobilePosseduto: AeromobilePosseduto | None = None
		self.aeroportoPartenza: Aeroporto | None = None
		self.aeroportoArrivo: Aeroporto | None = None
		self.dataCreazione: datetime | None = None
		self.dataFine: datetime | None = None
		self.tempoImpiegato: str | None = None
		self.distanzaPercorsa: float | None = None
		if id is None:
			return
		db: sqlite3.Connection = Database()
		riga: tuple = db.execute('SELECT * FROM voli WHERE id = ?', (id,)).fetchone()
		if riga is None:
			return
		self.id = id
		self.aeromobilePosseduto = AeromobilePosseduto(riga[1])
		self.aeroportoPartenza = Aeroporto(riga[2])
		self.aeroportoArrivo = Aeroporto(riga[3])
		self.dataCreazione = datetime.fromisoformat(riga[4])
		self.dataFine = datetime.fromisoformat(riga[5]) if riga[5] is not None else None
		self.tempoImpiegato = riga[6]
		self.distanzaPercorsa = riga[7]
	
	def add(self) -> bool:
		db: sqlite3.Connection = Database()
		c: sqlite3.Cursor = db.execute('INSERT INTO voli (aeromobile_posseduto, aeroporto_partenza, aeroporto_arrivo, data_creazione, data_fine, tempo_impiegato, distanza_percorsa) VALUES (?, ?, ?, ?, ?, ?, ?)', (self.aeromobilePosseduto.id, self.aeroportoPartenza.id, self.aeroportoArrivo.id, self.dataCreazione.isoformat(' ', 'seconds'), self.dataFine.isoformat(' ', 'seconds') if self.dataFine is not None else None, self.tempoImpiegato, self.distanzaPercorsa))
		db.commit()
		if c.rowcount >= 1:
			self.id = c.lastrowid
			return True
		return False
	
	def update(self) -> bool:
		db: sqlite3.Connection = Database()
		c: sqlite3.Cursor = db.execute('UPDATE voli SET aeromobile_posseduto = ?, aeroporto_partenza = ?, aeroporto_arrivo = ?, data_creazione = ?, data_fine = ?, tempo_impiegato = ?, distanza_percorsa = ? WHERE id = ?', (self.aeromobilePosseduto.id, self.aeroportoPartenza.id, self.aeroportoArrivo.id, self.dataCreazione.isoformat(' ', 'seconds'), self.dataFine.isoformat(' ', 'seconds') if self.dataFine is not None else None, self.tempoImpiegato, self.distanzaPercorsa, self.id))
		db.commit()
		return c.rowcount >= 1
	
	def save(self) -> bool:
		if self.id is None:
			return self.add()
		return self.update()
	
	def delete(self) -> bool:
		if self.id is None:
			return True
		db: sqlite3.Connection = Database()
		c: sqlite3.Cursor = db.execute('DELETE FROM voli WHERE id = ?', (self.id,))
		db.commit()
		if c.rowcount > 0:
			return True
		return False
	
	@staticmethod
	def getVoli() -> list['Volo']:
		db: sqlite3.Connection = Database()
		risultati: list[tuple] = db.execute('SELECT id FROM voli ORDER BY data_creazione ASC').fetchall()
		return [Volo(id) for id, in risultati]
	
	@staticmethod
	def getUltimoVoloDaFare() -> 'Volo':
		db: sqlite3.Connection = Database()
		volo: tuple | None = db.execute('SELECT id FROM voli WHERE data_fine IS NULL ORDER BY data_creazione ASC').fetchone()
		if volo is None:
			return Volo()
		id, = volo
		return Volo(id)