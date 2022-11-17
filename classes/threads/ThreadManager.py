from threading import Thread, Event
class ThreadManager:
	__threadList: list[dict] = []
	
	def addThread(self, f: callable, start: bool = False, *args) -> int:
		for i, t in enumerate(ThreadManager.__threadList):
			if f is t['target'] and args is t['args']:
				if start:
					self.startThread(i)
				return i
		shutdownEvent: Event = Event()
		ThreadManager.__threadList.append({'target': f, 'shutdownEvent': shutdownEvent, 'args': args, 'thread': Thread(target=f, args=(shutdownEvent,) + args, daemon=True)})
		indice: int = len(ThreadManager.__threadList) - 1
		if start:
			self.startThread(indice)
		return indice
	
	def startThread(self, indice: int) -> None:
		if indice < 0 or indice >= len(ThreadManager.__threadList):
			return
		if ThreadManager.__threadList[indice]['thread'].is_alive():
			return
		try:
			ThreadManager.__threadList[indice]['shutdownEvent'].clear()
			ThreadManager.__threadList[indice]['thread'].start()
		except RuntimeError:
			ThreadManager.__threadList[indice]['thread'] = Thread(target=ThreadManager.__threadList[indice]['target'], args=(ThreadManager.__threadList[indice]['shutdownEvent'],) + ThreadManager.__threadList[indice]['args'], daemon=True)
			ThreadManager.__threadList[indice]['shutdownEvent'].clear()
			ThreadManager.__threadList[indice]['thread'].start()
	
	def startThreads(self) -> None:
		for i, t in enumerate(ThreadManager.__threadList):
			self.startThread(i)
	
	def stopThread(self, indice: int):
		if indice < 0 or indice >= len(ThreadManager.__threadList):
			return
		if not ThreadManager.__threadList[indice]['thread'].is_alive():
			return
		ThreadManager.__threadList[indice]['shutdownEvent'].set()
		ThreadManager.__threadList[indice]['thread'].join()
	
	def stopThreads(self) -> None:
		for i, t in enumerate(ThreadManager.__threadList):
			self.stopThread(i)
	
	def restartThread(self, indice: int):
		if indice < 0 or indice >= len(ThreadManager.__threadList):
			return
		if ThreadManager.__threadList[indice]['thread'].is_alive():
			self.stopThread(indice)
		self.startThread(indice)
	
	def restartThreads(self) -> None:
		self.stopThreads()
		for t in ThreadManager.__threadList:
			t['thread'] = Thread(target=t['target'], args=(t['shutdownEvent'],) + t['args'], daemon=True)
		self.startThreads()