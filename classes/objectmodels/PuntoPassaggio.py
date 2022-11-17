import sqlite3
from classes.database.Database import Database
from json import dumps, loads

class PuntoPassaggio:
	def __init__(self, id: int = None):
		self.id: int | None = None
		self.idMissione: int | None = None
		self.latitudineCentro: float | None = None
		self.longitudineCentro: float | None = None
		self.perimetro: list[tuple[float,float]] = []
		if id is None:
			return
		db: sqlite3.Connection = Database()
		riga: tuple = db.execute('SELECT * FROM punti_passaggio WHERE id = ?', (id,)).fetchone()
		if riga is None:
			return
		self.id = id
		self.idMissione = riga[1]
		self.latitudineCentro = riga[2]
		self.longitudineCentro = riga[3]
		self.perimetro = loads(riga[4])
	
	def add(self) -> bool:
		db: sqlite3.Connection = Database()
		c: sqlite3.Cursor = db.execute('INSERT INTO punti_passaggio (id_missione, latitudine_centro, longitudine_centro, perimetro) VALUES (?, ?, ?, ?)', (self.idMissione, self.latitudineCentro, self.longitudineCentro, dumps(self.perimetro)))
		db.commit()
		if c.rowcount >= 1:
			self.id = c.lastrowid
			return True
		return False
	
	def update(self) -> bool:
		db: sqlite3.Connection = Database()
		c: sqlite3.Cursor = db.execute('UPDATE punti_passaggio SET id_missione = ?, latitudine_centro = ?, longitudine_centro = ?, perimetro = ? WHERE id = ?', (self.idMissione, self.latitudineCentro, self.longitudineCentro, dumps(self.perimetro), self.id))
		db.commit()
		return c.rowcount >= 1
	
	def save(self) -> bool:
		if self.id is None:
			return self.add()
		return self.update()
	
	def calcolaDistanza(self, latitudine: float, longitudine: float) -> float:
		if latitudine < -90 or latitudine > 90 or longitudine < -180 or longitudine > 180:
			raise Exception('Le coordinate non sono valide')
		from math import sqrt, pi, sin, cos, atan2
		R: float = 3440.0647948 # Radius of earth in NM
		dLat: float = latitudine * pi / 180 - self.latitudineCentro * pi / 180
		dLon: float = longitudine * pi / 180 - self.longitudineCentro * pi / 180
		a: float = sin(dLat/2) * sin(dLat/2) + cos(self.latitudineCentro * pi / 180) * cos(latitudine * pi / 180) * sin(dLon/2) * sin(dLon/2)
		c: float = 2 * atan2(sqrt(a), sqrt(1-a))
		d: float = R * c
		return d