from classes.objectmodels.Configurazione import Configurazione
class Utente:
	nome: str = ''
	cognome: str = ''
	saldo: float | None = None

	def __init__(self):
		dati: dict = Configurazione.getConfigurazioni(['nome', 'cognome', 'saldo'], ['TEXT', 'TEXT', 'REAL'])
		self.nome = dati['nome']
		self.cognome = dati['cognome']
		self.saldo = dati['saldo']
	
	def getSaldoFormattato(self) -> str:
		return f'{self.saldo:,.2f} €'