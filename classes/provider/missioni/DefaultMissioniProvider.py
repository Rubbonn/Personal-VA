from .AbstractMissioniProvider import AbstractMissioniProvider
from ...objectmodels.Missione import Missione
from ...objectmodels.Aeroporto import Aeroporto
from ...objectmodels.AeromobilePosseduto import AeromobilePosseduto
from random import randrange, choice, uniform, sample
class DefaultMissioniProvider(AbstractMissioniProvider):
	def getMissione(self) -> Missione:
		missione: Missione = Missione()
		aeroporti: list[Aeroporto] = Aeroporto.getAeroporti()
		aeromobili: list[AeromobilePosseduto] = AeromobilePosseduto.getAeromobiliPosseduti()
		distanzaMassima: float = 0
		passeggeriMassimi: int = 0
		bagagliMassimi: float = 0
		for aeromobile in aeromobili:
			distanza: float = (aeromobile.aeromobile.capacitaSerbatoioL / aeromobile.aeromobile.consumoLH) * aeromobile.aeromobile.velocitaCroceraKn
			distanzaMassima = max(distanzaMassima, distanza)
			passeggeriMassimi = max(passeggeriMassimi, aeromobile.aeromobile.numeroPosti - 2)
			bagagliMassimi = max(bagagliMassimi, aeromobile.aeromobile.grandezzaStivaKg)
		while True:
			aeroportoPartenza: Aeroporto = choice(aeroporti)
			aeroportoArrivo: Aeroporto = choice(aeroporti)
			if aeroportoPartenza.id == aeroportoArrivo.id:
				continue
			if aeroportoPartenza.calcolaDistanza(aeroportoArrivo.latitudine, aeroportoArrivo.longitudine) <= distanzaMassima:
				break
		while True:
			passeggeri: bool = randrange(0, 2)
			bagagli: bool = randrange(0, 2)
			if passeggeri or bagagli:
				break
		missione.aeroportoPartenza = aeroportoPartenza
		missione.aeroportoArrivo = aeroportoArrivo
		if passeggeri:
			missione.passeggeri = sample(range(4, 121), randrange(1, passeggeriMassimi + 1))
		missione.caricoBagagli = 0
		if bagagli:
			missione.caricoBagagli = round(uniform(0, bagagliMassimi), 2)
		if passeggeri:
			missione.descrizione = f'Trasporto di {len(missione.passeggeri)} passeggeri'
		else:
			missione.descrizione = f'Trasporto di merci'
		return missione