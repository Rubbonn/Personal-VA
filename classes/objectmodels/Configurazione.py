import sqlite3
class Configurazione:
	__db: sqlite3.Connection = None
	def __init__(self, db: sqlite3.Connection):
		self.__db = db

	def getConfigurazione(self, nome: str, tipo: str = None) -> str | None:
		sql: str = 'SELECT '
		if tipo is None:
			sql += 'valore '
		else:
			sql += 'CAST(valore AS ' + tipo + ') '
		sql += 'FROM configurazioni WHERE nome LIKE ?'
		risultato = self.__db.cursor().execute(sql, (nome,)).fetchone()
		if risultato is not None:
			return risultato[0]
		return risultato[0] if risultato is not None else risultato

	def getConfigurazioni(self, nomi: list[str], tipi: list[str] = []) -> dict:
		if len(tipi) > 0 and len(tipi) > len(nomi):
			return False
		if len(tipi) < len(nomi):
			tipi = [tipi[i] if i < len(tipi) else None for i in range(len(nomi))]
		cursore: sqlite3.Cursor = self.__db.cursor()
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
	
	def setConfigurazione(self, nome: str, valore: str) -> bool:
		cursore: sqlite3.Cursor = self.__db.cursor()
		cursore.execute('UPDATE configurazioni SET valore = ? WHERE nome LIKE ?', (valore, nome))
		self.__db.commit()
		return cursore.rowcount >= 1
	
	def setConfigurazioni(self, dati: dict) -> None:
		cursore: sqlite3.Cursor = self.__db.cursor()
		for nome, valore in dati.items():
			self.setConfigurazione(nome, valore)
		self.__db.commit()