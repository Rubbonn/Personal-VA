import sqlite3
from classes.database.Database import Database
class Aeromobile:
	id: int | None = None
	nome: str = ''
	capacitaSerbatoioL: int | None = None
	consumoLH: float | None = None
	numeroPosti: int | None = None
	velocitaMassimaKn: int | None = None
	velocitaCroceraKn: int | None = None
	grandezzaStivaKg: float | None = None
	foto: str = ''

	def __init__(self, id: int = None):
		db: sqlite3.Connection = Database()
		if id is None:
			return
		riga: tuple = db.execute('SELECT * FROM aeromobili WHERE id = ?', (id,)).fetchone()
		if riga is None:
			return
		self.id = id
		self.nome = riga[1]
		self.capacitaSerbatoioL = riga[2]
		self.consumoLH = riga[3]
		self.numeroPosti = riga[4]
		self.velocitaMassimaKn = riga[5]
		self.velocitaCroceraKn = riga[6]
		self.grandezzaStivaKg = riga[7]
		self.foto = riga[8]
	
	def getFormattedConsumoLH(self) -> str:
		return f'{self.consumoLH:,.2f} L/H'
	
	def getFormattedGrandezzaStivaKg(self) -> str:
		return f'{self.grandezzaStivaKg:,.2f} Kg'
	
	@staticmethod
	def getAeromobili() -> list['Aeromobile']:
		db: sqlite3.Connection = Database()
		risultato: list[tuple] = db.execute('SELECT id FROM aeromobili').fetchall()
		if risultato is None:
			return []
		return [Aeromobile(riga[0]) for riga in risultato]