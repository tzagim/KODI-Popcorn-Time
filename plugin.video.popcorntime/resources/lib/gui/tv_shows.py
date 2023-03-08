#!/usr/bin/env python

__license__ = "GPLv3"
__version__ = "3.0.0"
__author__ = "theRedMercury"

import os.path

import xbmcswift2

from resources.lib.api.api import API
from resources.lib.api.tv_shows import TvShowAPI
from resources.lib.utils import get_media


class TvShowMenu(xbmcswift2.Module):

    def __init__(self, pct_plugin):
        super(TvShowMenu, self).__init__('plugin.video.popcorntime.menu.tv_show_m')

        self.pct_plugin = pct_plugin
        # decorators
        self.menu = self.route('/tv_shows/')(self.menu)
        self.search = self.route('/tv_shows/search')(self.search)

    def menu(self):
        items = [
            {'label': self.pct_plugin.tr('most_popular'),
             'icon': get_media("tvshows", "popular.png"),
             'thumbnail': get_media("tvshows", "popular.png"),
             'path': self.url_for('tv_shows.list_items', sort_request="trending", explicit=True),
             "properties": {
                 "fanart_image": get_media("categories", "fanart.jpg"),
             },
             'offscreen': True},

            {'label': self.pct_plugin.tr('recently'),
             'icon': get_media("tvshows", "recently.png"),
             'thumbnail': get_media("tvshows", "recently.png"),
             'path': self.url_for('tv_shows.list_items', sort_request="last_added", explicit=True),
             "properties": {
                 "fanart_image": get_media("categories", "fanart.jpg"),
             },
             'offscreen': True},

            {'label': self.pct_plugin.tr('rated'),
             'icon': get_media("tvshows", "rated.png"),
             'thumbnail': get_media("tvshows", "rated.png"),
             'path': self.url_for('tv_shows.list_items', sort_request="rating", explicit=True),
             "properties": {
                 "fanart_image": get_media("categories", "fanart.jpg"),
             },
             'offscreen': True},

            {'label': self.pct_plugin.tr('genres'),
             'icon': get_media("tvshows", "genres.png"),
             'thumbnail': get_media("tvshows", "genres.png"),
             'path': self.url_for('tv_shows.genres', explicit=True),
             "properties": {
                 "fanart_image": get_media("categories", "fanart.jpg"),
             },
             'offscreen': True},

            {'label': self.pct_plugin.tr('search'),
             'icon': get_media("tvshows", "search.png"),
             'thumbnail': get_media("tvshows", "search.png"),
             'path': self.url_for('tv_show_m.search', explicit=True),
             "properties": {
                 "fanart_image": get_media("categories", "fanart.jpg"),
             },
             'offscreen': True},
        ]
        return items

    def search(self):
        self.pct_plugin.utils.log.debug("go to search")
        query = self.keyboard(heading=self.pct_plugin.tr('search'))
        if query:
            self.plugin.redirect(self.url_for('tv_shows.search', keyword=query, explicit=True))


class TvShowList(xbmcswift2.Module):

    def __init__(self, pct_plugin):
        super(TvShowList, self).__init__('plugin.video.popcorntime.menu.tv_show_m.tv_shows')

        self.pct_plugin = pct_plugin

        # decorators
        self.list_items = self.route('/tv_shows/list_items/<sort_request>/<genre>/<page>',
                                     options={'genre': 'all', 'page': '1'})(self.list_items)
        self.list_items_season = self.route('/tv_shows/list_items_season/<id_show>/<num_seasons>/<fanart>',
                                            options={'fanart': ''})(self.list_items_season)
        self.list_items_episodes = self.route('/tv_shows/list_items_episodes/<id_show>/<season>')(
            self.list_items_episodes)

        self.genres = self.route('/tv_shows/genres')(self.genres)
        self.search = self.route('/tv_shows/search/<keyword>')(self.search)

    def search(self, keyword):
        self.pct_plugin.utils.log.debug(f"search : {keyword} ")
        return TvShowAPI.search(self, keyword)

    def list_items(self, sort_request, genre, page):
        self.pct_plugin.utils.log.debug(f"list_items page : {page} - {genre} - {sort_request}")

        items = TvShowAPI.get_tvshows(self, page, sort_request, genre)

        next_page = str(int(page) + 1)
        self.pct_plugin.utils.log.debug(f"list_items int_page : {next_page} ")
        items.append(
            {'label': self.pct_plugin.tr('show_more'),
             'icon': get_media("tvshows", "more.png"),
             'thumbnail': get_media("tvshows", "more_thumbnail.png"),
             'path': self.url_for('tv_shows.list_items', sort_request=sort_request, page=next_page, genre=genre,
                                  explicit=True),
             'offscreen': True},
        )
        return items

    def list_items_season(self, id_show, num_seasons, fanart):
        self.pct_plugin.utils.log.debug(f"list_items_season page : {id_show}")

        items = []
        for i in range(0, int(num_seasons)):
            item = {
                "label": f"season {i + 1}",
                "properties": {
                    "fanart_image": fanart,
                },
                "info": {
                    'mediatype': 'season',
                },
                "path": self.url_for("tv_shows.list_items_episodes", id_show=id_show, season=(i + 1)),
            }
            items.append(item)
        return items

    def list_items_episodes(self, id_show, season):
        self.pct_plugin.utils.log.debug(f"list_items_episodes page : {id_show} - {season}")
        return TvShowAPI.get_tvshows_episodes(self, id_show, season)

    def genres(self):
        items = [
            {
                'label': self.pct_plugin.tr_id(key),
                'icon': get_media(os.path.join("tvshows", "genres"), f"{value}.png"),
                'thumbnail': get_media(os.path.join("tvshows", "genres"), f"{value}.png"),
                'path': self.url_for('tv_shows.list_items', sort_request="trending", genre=value, explicit=True),
                "properties": {
                    "fanart_image": get_media("categories", "fanart.jpg"),
                },
                'offscreen': True
            } for key, value in API.genres.items()
        ]
        return items
