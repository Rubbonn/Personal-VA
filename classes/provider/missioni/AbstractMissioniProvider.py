from abc import ABC, abstractmethod
from ...objectmodels.Missione import Missione
class AbstractMissioniProvider(ABC):
	@abstractmethod
	def getMissione(self) -> Missione:
		pass