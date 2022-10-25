from .AbstractProvider import AbstractProvider
class DefaultProvider(AbstractProvider):
	def getPrezzoCarburante(self, idAeroporto: int = None, idCarburante: int = None) -> float | None:
		import sqlite3
		from classes.database.Database import Database
		db: sqlite3.Connection = Database()
		return db.execute('SELECT prezzo_base FROM carburanti WHERE id = ?', (idCarburante,)).fetchone()[0]