#!/usr/bin/python
import os, re, xbmc, traceback, sys
from kodipopcorntime.threads import Thread
__addon__ = sys.modules['__main__'].__addon__

_id = __addon__.getAddonInfo('id')
_loglevel = [xbmc.LOGDEBUG, xbmc.LOGINFO, xbmc.LOGWARNING, xbmc.LOGERROR, xbmc.LOGFATAL, -1]
if __addon__.getSetting("debug") == 'true':
    _loglevel[-1] = xbmc.LOGDEBUG

class LOGLEVEL:
    NONE     = -1
    DEBUG    = 0
    INFO     = 1
    WARNING  = 2
    ERROR    = 3
    FATAL    = 4

def prefix():
    if hasattr(Thread.LOCAL, 'tName'):
        return "(%s) " %Thread.LOCAL.tName
    return ''

def log(message, level=LOGLEVEL.DEBUG):
    level = _loglevel[level]
    if level > -1:
        xbmc.log(msg='[%s] %s%s' %(_id, prefix(), message), level=level)

def log_error():
    xbmc.log(msg='[%s] %s%s' %(_id, prefix(), traceback.format_exc()), level=_loglevel[LOGLEVEL.FATAL])

class LogPipe(Thread):
    def __init__(self, logger):
        self._logger = logger
        self._read_fd, self._write_fd = os.pipe()
        super(LogPipe, self).__init__(target=self.run)

    def fileno(self):
        return self._write_fd

    def run(self):
        self._logger("Logging started")
        with os.fdopen(self._read_fd) as f:
            for line in iter(f.readline, ""):
                line = re.sub(r'^\d+/\d+/\d+ \d+:\d+:\d+ ', '', line)
                self._logger(line.strip())
                if self.stop.is_set():
                    break
        self._logger("Logging finished")
