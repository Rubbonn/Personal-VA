from .AbstractProvider import AbstractProvider
from classes.objectmodels.Configurazione import Configurazione
class AvfuelcomProvider(AbstractProvider):
	def getPrezzoCarburante(self, idAeroporto: int = None, idCarburante: int = None) -> float | None:
		apiKey: str = Configurazione.getConfigurazione('avfuel_com_api_key')
		if apiKey is None:
			return None