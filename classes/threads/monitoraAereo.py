from threading import Event
from time import sleep
from SimConnect import *

def monitoraAereo(shutdownEvent: Event) -> None:
	connesso: bool = False
	while not connesso:
		try:
			if shutdownEvent.is_set():
				return
			sm: SimConnect = SimConnect()
			connesso = True
		except ConnectionError:
			print('Impossibile connettersi a Flight Simulator')
			sleep(1)
	aq: AircraftRequests = AircraftRequests(sm, 0)
	while True:
		if shutdownEvent.is_set():
			break
		altitudine: float = aq.get('INDICATED_ALTITUDE')
		latitudine: float = aq.get('PLANE_LATITUDE')
		longitudine: float = aq.get('PLANE_LONGITUDE')
		carburante: float = aq.get('FUEL_TOTAL_QUANTITY')
		velocita: float = aq.get('AIRSPEED_INDICATED')
		onGround: bool = aq.get('SIM_ON_GROUND')
		crash: int = aq.get('CRASH_FLAG')
		isRunning: bool = sm.running
		print('Altitudine:', altitudine)
		print('Latitudine:', latitudine)
		print('Longitudine:', longitudine)
		print('Carburante:', carburante)
		print('Velocità:', velocita)
		print('onGround:', onGround)
		print('crash:', crash)
		print('running:', isRunning)
		print('------------------------------------------------------------------------')
		sleep(1)
	sm.exit()