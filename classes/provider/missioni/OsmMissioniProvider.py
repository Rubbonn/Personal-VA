from .AbstractMissioniProvider import AbstractMissioniProvider
from urllib.request import urlopen
from urllib.parse import urlencode
from ...objectmodels.Missione import Missione
from ...objectmodels.Aeroporto import Aeroporto
from ...objectmodels.AeromobilePosseduto import AeromobilePosseduto
from ...objectmodels.PuntoPassaggio import PuntoPassaggio
from ...cache.Cache import Cache
from random import randrange, choice, uniform, sample
from json import loads
class OsmMissioniProvider(AbstractMissioniProvider):
	def __init__(self):
		self.__puntiInteresse: list[PuntoPassaggio] | None = Cache.get('OsmMissioniProvider_punti_interesse')
		if self.__puntiInteresse is not None:
			return
		self.__puntiInteresse = {}
		try:
			query: str = urlencode({'data': '[timeout:300][out:json];area[name="Italia"][wikipedia="it:Italia"] -> .areaItalia;(nwr[tourism="attraction"][name][historic="monument"](area.areaItalia);nwr[water~"lake|lagoon|oxbow|river"][name](area.areaItalia);) -> .luoghi;.luoghi out geom;.luoghi out center ids;'})
			with urlopen(f'https://overpass-api.de/api/interpreter?{query}') as risposta:
				risposta = risposta.read().decode()
				puntiOsm: object = loads(risposta)
				for elemento in puntiOsm['elements']:
					if elemento['id'] in self.__puntiInteresse:
						if (elemento['type'] == 'way' or elemento['type'] == 'relation') and 'center' in elemento:
							self.__puntiInteresse[elemento['id']].latitudineCentro = elemento['center']['lat']
							self.__puntiInteresse[elemento['id']].longitudineCentro = elemento['center']['lon']
						continue
					punto: PuntoPassaggio = PuntoPassaggio()
					punto.nome = elemento['tags']['name']
					match elemento['type']:
						case 'node':
							punto.latitudineCentro = elemento['lat']
							punto.longitudineCentro = elemento['lon']
						case 'way':
							for angolo in elemento['geometry']:
								punto.perimetro.append((angolo['lat'], angolo['lon']))
						case 'relation':
							for membro in elemento['members']:
								match membro['type']:
									case 'node':
										punto.perimetro.append((membro['lat'], membro['lon']))
									case 'way':
										for angolo in membro['geometry']:
											punto.perimetro.append((angolo['lat'], angolo['lon']))
					self.__puntiInteresse[elemento['id']] = punto
			self.__puntiInteresse = list(self.__puntiInteresse.values())
			Cache.set('OsmMissioniProvider_punti_interesse', self.__puntiInteresse, 300)
		except BaseException as e:
			print('Impossibile scaricare i dati da OpenStreetMap:', e)
			return

	def getMissione(self) -> Missione:
		if self.__puntiInteresse is None:
			return None
		missione: Missione = Missione()
		aeroporti: list[Aeroporto] = Aeroporto.getAeroporti()
		aeromobili: list[AeromobilePosseduto] = AeromobilePosseduto.getAeromobiliPosseduti()
		distanzaMassima: float = 0
		passeggeriMassimi: int = 0
		bagagliMassimi: float = 0
		for aeromobile in aeromobili:
			distanzaMassima = max(distanzaMassima, (aeromobile.aeromobile.capacitaSerbatoioL / aeromobile.aeromobile.consumoLH) * aeromobile.aeromobile.velocitaCroceraKn)
			passeggeriMassimi = max(passeggeriMassimi, aeromobile.aeromobile.numeroPosti - 2)
			bagagliMassimi = max(bagagliMassimi, aeromobile.aeromobile.grandezzaStivaKg)
		while True:
			passeggeri: bool = randrange(0, 2)
			bagagli: bool = randrange(0, 2)
			if passeggeri or bagagli:
				break
		while True:
			aeroportoPartenza: Aeroporto = choice(aeroporti)
			aeroportoArrivo: Aeroporto = choice(aeroporti)
			puntiPassaggio: list[PuntoPassaggio] = []
			if passeggeri:
				puntiPassaggio: list[PuntoPassaggio] = sample(self.__puntiInteresse, randrange(0, 4))
			if len(puntiPassaggio) == 0:
				if aeroportoPartenza.calcolaDistanza(aeroportoArrivo.latitudine, aeroportoArrivo.longitudine) <= distanzaMassima:
					break
			else:
				distanza: float = aeroportoPartenza.calcolaDistanza(puntiPassaggio[0].latitudineCentro, puntiPassaggio[0].longitudineCentro)
				for k, punto in enumerate(puntiPassaggio):
					if k + 1 == len(puntiPassaggio):
						break
					distanza += punto.calcolaDistanza(puntiPassaggio[k + 1].latitudineCentro, puntiPassaggio[k + 1].longitudineCentro)
				distanza += puntiPassaggio[-1].calcolaDistanza(aeroportoArrivo.latitudine, aeroportoArrivo.longitudine)
				if distanza <= distanzaMassima:
					break
		missione.aeroportoPartenza = aeroportoPartenza
		missione.aeroportoArrivo = aeroportoArrivo
		missione.puntiPassaggio = puntiPassaggio
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