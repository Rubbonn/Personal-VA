from .prezzi_carburante.AbstractPrezzoCarburanteProvider import AbstractPrezzoCarburanteProvider
from .prezzi_carburante.DefaultPrezzoCarburanteProvider import DefaultPrezzoCarburanteProvider
class PrezziCarburanteProvider:
	__providerList: list[AbstractPrezzoCarburanteProvider] = []

	def __init__(self):
		self.__providerList.append(DefaultPrezzoCarburanteProvider())
	
	def getPrezzoCarburante(self, idAeroporto: int, idCarburante: int) -> float:
		for provider in self.__providerList:
			prezzo = provider.getPrezzoCarburante(idAeroporto, idCarburante)
			if prezzo is not None:
				return prezzo