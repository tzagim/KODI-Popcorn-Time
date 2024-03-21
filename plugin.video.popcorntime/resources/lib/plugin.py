#!/usr/bin/env python

__license__ = "GPLv3"
__version__ = "3.0.1"
__author__ = "Tzagim"

from xbmcswift2 import Plugin

import resources.lib.gui.menu
import resources.lib.gui.movies
import resources.lib.gui.tv_shows
from resources.lib.utils import Utils

STRINGS = {
    "movie": 30162,
    "tv_shows": 30163,

    "most_popular": 30004,
    "rated": 30005,
    "recently": 30006,
    "search": 30160,
    "genres": 30003,

    "show_more": 30000,
    "add_favorite": 30039,
}


class PopCornTimeAddon:
    def __init__(self):
        self.plugin = Plugin("popcorn_time")
        self.utils = Utils(self.plugin)
        self.utils.log_init()

        self.plugin.register_module(resources.lib.gui.menu.MainMenu(self), '')
        self.plugin.register_module(resources.lib.gui.movies.MovieMenu(self), '')
        self.plugin.register_module(resources.lib.gui.movies.MovieList(self), '')
        self.plugin.register_module(resources.lib.gui.tv_shows.TvShowMenu(self), '')
        self.plugin.register_module(resources.lib.gui.tv_shows.TvShowList(self), '')

        # self.utils.dialog_error_msg("Hello")

    def run(self):
        try:
            self.plugin.run()
        except KeyboardInterrupt:
            pass
        except SystemExit:
            pass
        except:
            self.utils.handle_error()

    def tr(self, string_id):
        if string_id in STRINGS:
            return self.plugin.get_string(STRINGS[string_id])
        else:
            self.utils.log.warning(f"String is missing: {string_id}")
            return string_id

    def tr_id(self, s_id):
        try:
            return self.plugin.get_string(s_id)
        except:
            self.utils.log.warning(f"String is missing: {s_id}")
            pass
