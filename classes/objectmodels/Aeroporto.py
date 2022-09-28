import sqlite3
class Aeroporto:
	__db: sqlite3.Connection = None
	id: int = None
	codice_icao: str = ''
	nome: str = ''
	citta: str = ''
	nazione: str = ''
	latitudine: float = None
	longitudine: float = None

	def __init__(self, db: sqlite3.Connection, id: int = None):
		self.__db = db
		if id is None:
			return
		cursore = self.__db.cursor()
		riga: tuple = cursore.execute('SELECT * FROM aeroporti WHERE id = ?', (id,)).fetchone()
		if riga is None:
			return
		self.id = id
		self.codice_icao = riga[1]
		self.nome = riga[2]
		self.citta = riga[3]
		self.nazione = riga[4]
		self.latitudine = riga[5]
		self.longitudine = riga[6]
	
	def getAeroporti(self) -> list['Aeroporto']:
		risultati: list[tuple] = self.__db.execute('SELECT id FROM aeroporti ORDER BY nome ASC').fetchall()
		if risultati is None:
			return []
		return [Aeroporto(self.__db, id[0]) for id in risultati]