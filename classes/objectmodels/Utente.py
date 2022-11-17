from classes.objectmodels.Configurazione import Configurazione
class Utente:
	def __init__(self):
		dati: dict = Configurazione.getConfigurazioni(['nome', 'cognome', 'saldo'], ['TEXT', 'TEXT', 'REAL'])
		self.nome: str = dati['nome']
		self.cognome: str = dati['cognome']
		self.saldo: float | None = dati['saldo']
	
	def getSaldoFormattato(self) -> str:
		return f'{self.saldo:,.2f} €'
	
	@staticmethod
	def aggiornaSaldo(delta: float = 0):
		saldo: float = Configurazione.getConfigurazione('saldo', 'REAL')
		saldo += delta
		Configurazione.setConfigurazione('saldo', saldo)