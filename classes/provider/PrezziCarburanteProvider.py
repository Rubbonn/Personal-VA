from .prezzi_carburante.AbstractProvider import AbstractProvider
from .prezzi_carburante.DefaultProvider import DefaultProvider
class PrezziCarburanteProvider:
	__providerList: list[AbstractProvider] = []

	def __init__(self):
		self.__providerList.append(DefaultProvider())
	
	def getPrezzoCarburante(self, idAeroporto: int, idCarburante: int) -> float:
		for provider in self.__providerList:
			prezzo = provider.getPrezzoCarburante(idAeroporto, idCarburante)
			if prezzo is not None:
				return prezzo