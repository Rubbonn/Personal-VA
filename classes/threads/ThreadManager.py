from threading import Thread, Event
class ThreadManager:
	__database: str = None
	__shutdownEvent: Event = Event()
	__threadList: list[Thread] = []

	def __init__(self, database: str):
		self.__database = database
	
	def addThread(self, f: callable, start: bool = False, *args, **kwargs) -> None:
		args = (self.__shutdownEvent, self.__database) + args
		self.__threadList.append(Thread(target=f, args=args, daemon=True))
		if start:
			self.__shutdownEvent.clear()
			self.__threadList[:-1].start()
	
	def startThreads(self) -> None:
		self.__shutdownEvent.clear()
		for thread in self.__threadList:
			if not thread.is_alive():
				thread.start()
	
	def stopThreads(self) -> None:
		self.__shutdownEvent.set()
		for thread in self.__threadList:
			if thread.is_alive():
				thread.join()