from abc import ABC, abstractmethod
class AbstractPrezzoCarburanteProvider(ABC):
	@abstractmethod
	def getPrezzoCarburante(self, idAeroporto: int = None, idCarburante: int = None) -> float | None:
		pass