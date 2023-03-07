#!/usr/bin/env python

__license__ = "GPLv3"
__version__ = "3.0.0"
__author__ = "theRedMercury"

import os
import sys
import traceback
import xbmcaddon
from xbmcswift2 import xbmcgui

__addon__ = xbmcaddon.Addon(id="plugin.video.popcorntime")

__resources_path__ = os.path.join(__addon__.getAddonInfo('path'), 'resources')
__media_path__ = os.path.join(__resources_path__, 'media')


def get_setting(id_set):
    return __addon__.getSetting(id_set)


def get_media(subdir, file_name):
    return os.path.join(__media_path__, subdir, file_name)


class Utils:

    def __init__(self, plugin):
        self.plugin = plugin
        self.log = plugin.log
        self.name = plugin.name
        self.id = plugin.addon.getAddonInfo('id')
        self.version = plugin.addon.getAddonInfo('version')

    def log_init(self):
        self.log.debug('Initialising %s addon, v%s' % (self.name, self.version))

    def handle_error(self, err=""):
        traceback_str = traceback.format_exc()
        self.log.error(traceback_str)

    def dialog_error_msg(self, msg=""):
        content = []
        exc_type, exc_value, exc_traceback = sys.exc_info()
        content.append(f"{self.name} {self.version} : Error")
        if exc_value:
            content.append(f"{msg} : {exc_value}")
        else:
            content.append(f"{msg}")

        xbmcgui.Dialog().ok(*content)
        return
