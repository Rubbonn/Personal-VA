import sqlite3
from classes.database.Database import Database
class Aeromobile:
	def __init__(self, id: int = None):
		self.id: int | None = None
		self.idCarburante: int | None = None
		self.nome: str = ''
		self.capacitaSerbatoioL: int | None = None
		self.consumoLH: float | None = None
		self.numeroPosti: int | None = None
		self.velocitaMassimaKn: int | None = None
		self.velocitaCroceraKn: int | None = None
		self.grandezzaStivaKg: float | None = None
		self.foto: str = ''
		if id is None:
			return
		db: sqlite3.Connection = Database()
		riga: tuple = db.execute('SELECT * FROM aeromobili WHERE id = ?', (id,)).fetchone()
		if riga is None:
			return
		self.id = id
		self.idCarburante = riga[1]
		self.nome = riga[2]
		self.capacitaSerbatoioL = riga[3]
		self.consumoLH = riga[4]
		self.numeroPosti = riga[5]
		self.velocitaMassimaKn = riga[6]
		self.velocitaCroceraKn = riga[7]
		self.grandezzaStivaKg = riga[8]
		self.foto = riga[9]
	
	def getFormattedConsumoLH(self) -> str:
		return f'{self.consumoLH:,.2f} L/H'
	
	def getFormattedGrandezzaStivaKg(self) -> str:
		return f'{self.grandezzaStivaKg:,.2f} Kg'
	
	def getNomeCarburante(self) -> str:
		db: sqlite3.Connection = Database()
		return db.execute('SELECT nome FROM carburanti WHERE id = ?', (self.idCarburante,)).fetchone()[0]
	
	@staticmethod
	def getAeromobili() -> list['Aeromobile']:
		db: sqlite3.Connection = Database()
		risultato: list[tuple] = db.execute('SELECT id FROM aeromobili').fetchall()
		return [Aeromobile(riga) for riga, in risultato]