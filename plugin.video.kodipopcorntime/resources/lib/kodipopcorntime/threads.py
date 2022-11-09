#!/usr/bin/python
import sys, threading, time

class Thread(threading.Thread):
    LOCAL = threading.local()

    def __init__(self, target=None):
        # _target is set by Thread()
        self.__target = target or self.run
        self._exc_info = []

        super(Thread, self).__init__(target=self.___run)
        self.daemon = False
        self.stop = threading.Event()
        self.start()

    def __enter__(self):
        return self

    def ___run(self):
        try:
            Thread.LOCAL.tName = self.getName()
            self.__target()
        except:
            self._exc_info = sys.exc_info()
            self.stop.set()

    def checkError(self):
        return len(self._exc_info) > 0

    def raiseAnyError(self):
        if self._exc_info:
            raise self._exc_info[1].with_traceback(self._exc_info[2])

    def cleanError(self):
        self._exc_info = []

    def getError(self):
        return self._exc_info

    def __exit__(self, *exc_info):
        self.close()
        return not exc_info[0] and not len(self._exc_info) > 0

    def __del__(self):
        self.close()

    def close(self):
        if hasattr(self, 'stop') and not self.stop.is_set():
            self.stop.set()
        self.raiseAnyError()

class FLock:
    _locks = {}
    def __init__(self, file):
        if not FLock._locks.get(file):
            FLock._locks[file] = False
        while FLock._locks[file]:
            time.sleep(0.100)
        if FLock._locks[file]:
            raise RuntimeError("cannot acquired lock")
        FLock._locks[file] = True

    def unLock(self, file):
        if not FLock._locks[file]:
            raise RuntimeError("cannot release un-acquired lock")
        FLock._locks[file] = False
