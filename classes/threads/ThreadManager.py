from threading import Thread, Event
class ThreadManager:
	__shutdownEvent: Event = Event()
	__threadList: list[dict] = []
	
	def addThread(self, f: callable, start: bool = False, *args) -> None:
		args = (self.__shutdownEvent,) + args
		self.__threadList.append({'target': f, 'args': args, 'thread': Thread(target=f, args=args, daemon=True)})
		if start:
			self.__shutdownEvent.clear()
			self.__threadList[:-1]['thread'].start()
	
	def startThreads(self) -> None:
		self.__shutdownEvent.clear()
		for t in self.__threadList:
			if not t['thread'].is_alive():
				t['thread'].start()
	
	def stopThreads(self) -> None:
		self.__shutdownEvent.set()
		for t in self.__threadList:
			if t['thread'].is_alive():
				t['thread'].join()
	
	def restartThreads(self) -> None:
		self.stopThreads()
		newList: list[dict] = []
		for t in self.__threadList:
			newList.append({'target': t['target'], 'args': t['args'], 'thread': Thread(target=t['target'], args=t['args'], daemon=True)})
		self.__threadList = newList
		self.startThreads()