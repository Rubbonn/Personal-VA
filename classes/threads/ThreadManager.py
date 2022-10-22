from threading import Thread, Event
class ThreadManager:
	__threadList: list[dict] = []
	
	def addThread(self, f: callable, start: bool = False, *args) -> int:
		for i, t in enumerate(self.__threadList):
			if f is t['target'] and args is t['args']:
				if start:
					self.startThread(i)
				return i
		shutdownEvent: Event = Event()
		self.__threadList.append({'target': f, 'shutdownEvent': shutdownEvent, 'args': args, 'thread': Thread(target=f, args=(shutdownEvent,) + args, daemon=True)})
		indice: int = len(self.__threadList) - 1
		if start:
			self.startThread(indice)
		return indice
	
	def startThread(self, indice: int) -> None:
		if indice < 0 or indice >= len(self.__threadList):
			return
		if self.__threadList[indice]['thread'].is_alive():
			return
		try:
			self.__threadList[indice]['shutdownEvent'].clear()
			self.__threadList[indice]['thread'].start()
		except RuntimeError:
			self.__threadList[indice]['thread'] = Thread(target=self.__threadList[indice]['target'], args=(self.__threadList[indice]['shutdownEvent'],) + self.__threadList[indice]['args'], daemon=True)
			self.__threadList[indice]['shutdownEvent'].clear()
			self.__threadList[indice]['thread'].start()
	
	def startThreads(self) -> None:
		for i, t in enumerate(self.__threadList):
			self.startThread(i)
	
	def stopThread(self, indice: int):
		if indice < 0 or indice >= len(self.__threadList):
			return
		if not self.__threadList[indice]['thread'].is_alive():
			return
		self.__threadList[indice]['shutdownEvent'].set()
		self.__threadList[indice]['thread'].join()
	
	def stopThreads(self) -> None:
		for i, t in enumerate(self.__threadList):
			self.stopThread(i)
	
	def restartThreads(self) -> None:
		self.stopThreads()
		for t in self.__threadList:
			t['thread'] = Thread(target=t['target'], args=(t['shutdownEvent'],) + t['args'], daemon=True)
		self.startThreads()