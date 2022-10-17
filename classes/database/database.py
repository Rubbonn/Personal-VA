from sqlite3 import connect, Connection

class Database:
	__database: str = 'personal-va.db'

	def __new__(cls) -> Connection:
		return connect(cls.__database)