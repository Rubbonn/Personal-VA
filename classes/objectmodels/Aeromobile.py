import sqlite3
from classes.database.database import Database
class Aeromobile:
	id: int | None = None
	nome: str = ''
	capacita_serbatoio_l: int | None = None
	consumo_l_h: float | None = None
	numero_posti: int | None = None
	velocita_massima_kn: int | None = None
	velocita_crocera_kn: int | None = None
	grandezza_stiva_kg: float | None = None
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
		self.capacita_serbatoio_l = riga[2]
		self.consumo_l_h = riga[3]
		self.numero_posti = riga[4]
		self.velocita_massima_kn = riga[5]
		self.velocita_crocera_kn = riga[6]
		self.grandezza_stiva_kg = riga[7]
		self.foto = riga[8]
	
	@staticmethod
	def getAeromobili() -> list['Aeromobile']:
		db: sqlite3.Connection = Database()
		risultato: list[tuple] = db.execute('SELECT id FROM aeromobili').fetchall()
		if risultato is None:
			return []
		return [Aeromobile(riga[0]) for riga in risultato]