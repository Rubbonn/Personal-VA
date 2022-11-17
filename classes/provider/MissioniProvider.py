from .missioni.AbstractMissioniProvider import AbstractMissioniProvider
from .missioni.DefaultMissioniProvider import DefaultMissioniProvider
from ..objectmodels.Missione import Missione
class MissioniProvider:
	def __init__(self):
		self.__providerList: list[AbstractMissioniProvider] = []
		self.__providerList.append(DefaultMissioniProvider())
	
	def getMissione(self) -> Missione:
		for provider in self.__providerList:
			missione = provider.getMissione()
			if missione is not None:
				return missione