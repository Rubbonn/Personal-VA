from .missioni.AbstractMissioniProvider import AbstractMissioniProvider
from .missioni.DefaultMissioniProvider import DefaultMissioniProvider
from ..objectmodels.Missione import Missione
class MissioniProvider:
	__providerList: list[AbstractMissioniProvider] = []

	def __init__(self):
		self.__providerList.append(DefaultMissioniProvider())
	
	def getMissione(self) -> Missione:
		for provider in self.__providerList:
			missione = provider.getMissione()
			if missione is not None:
				return missione