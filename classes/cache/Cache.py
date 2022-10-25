import sqlite3
from typing import Any
from classes.database.Database import Database
from datetime import datetime, timedelta
from pickle import dumps, loads, HIGHEST_PROTOCOL
class Cache:
	@staticmethod
	def get(chiave: str = None):
		if chiave is None:
			return None
		db: sqlite3.Connection = Database()
		risultato: tuple = db.execute('SELECT valore, scadenza FROM cache WHERE chiave LIKE ?', (chiave,)).fetchone()
		if risultato is None:
			return None
		scadenza: datetime = datetime.fromisoformat(risultato[1])
		adesso: datetime = datetime.today()
		if adesso >= scadenza:
			return None
		try:
			return loads(risultato[0])
		except:
			return None
	
	@staticmethod
	def set(chiave: str = None, valore: Any = None, ttl: int = 0) -> None:
		if chiave is None:
			return
		scadenza: datetime = datetime.today() + timedelta(seconds=ttl)
		valore = dumps(valore, HIGHEST_PROTOCOL)
		db: sqlite3.Connection = Database()
		db.execute('INSERT OR REPLACE INTO cache (chiave, valore, scadenza) VALUES (?, ?, ?)', (chiave, valore, scadenza.isoformat(' ', 'seconds')))
		db.commit()