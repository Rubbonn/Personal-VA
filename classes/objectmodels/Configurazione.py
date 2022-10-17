import sqlite3
from classes.database.database import Database

class Configurazione:
	
	@staticmethod
	def getConfigurazione(nome: str, tipo: str = None) -> str | None:
		db: sqlite3.Connection = Database()
		sql: str = 'SELECT '
		if tipo is None:
			sql += 'valore '
		else:
			sql += 'CAST(valore AS ' + tipo + ') '
		sql += 'FROM configurazioni WHERE nome LIKE ?'
		risultato = db.execute(sql, (nome,)).fetchone()
		if risultato is not None:
			return risultato[0]
		return risultato[0] if risultato is not None else risultato

	@staticmethod
	def getConfigurazioni(nomi: list[str], tipi: list[str] = []) -> dict:
		if len(tipi) > 0 and len(tipi) > len(nomi):
			return False
		if len(tipi) < len(nomi):
			tipi = [tipi[i] if i < len(tipi) else None for i in range(len(nomi))]
		db: sqlite3.Connection = Database()
		cursore: sqlite3.Cursor = db.cursor()
		risultati: dict = {}
		for configurazione in zip(nomi, tipi):
			sql: str = 'SELECT '
			if configurazione[1] is None:
				sql += 'valore '
			else:
				sql += 'CAST(valore AS ' + configurazione[1] + ') '
			sql += 'FROM configurazioni WHERE nome LIKE ?'
			risultato = cursore.execute(sql, (configurazione[0],)).fetchone()
			risultati[configurazione[0]] = risultato[0] if risultato is not None else risultato
		return risultati
	
	@staticmethod
	def setConfigurazione(nome: str, valore: str) -> bool:
		db: sqlite3.Connection = Database()
		cursore: sqlite3.Cursor = db.cursor()
		cursore.execute('UPDATE configurazioni SET valore = ? WHERE nome LIKE ?', (valore, nome))
		db.commit()
		return cursore.rowcount >= 1
	
	@staticmethod
	def setConfigurazioni(dati: dict) -> None:
		for nome, valore in dati.items():
			Configurazione.setConfigurazione(nome, valore)
		db: sqlite3.Connection = Database()
		db.commit()