#!/usr/bin/env python

__license__ = "GPLv3"
__version__ = "3.0.0"
__author__ = "theRedMercury"

import os.path

import xbmcswift2

from resources.lib.api.api import API
from resources.lib.api.movies import MovieApi
from resources.lib.utils import get_media


class MovieMenu(xbmcswift2.Module):

    def __init__(self, pct_plugin):
        super(MovieMenu, self).__init__('plugin.video.popcorntime.menu.movie_m')

        self.pct_plugin = pct_plugin
        # decorators
        self.menu = self.route('/movies/')(self.menu)
        self.search = self.route('/movies/search')(self.search)

    def menu(self):
        items = [
            {'label': self.pct_plugin.tr('most_popular'),
             'icon': get_media("movies", "popular.png"),
             'thumbnail': get_media("movies", "popular.png"),
             'path': self.url_for('movies.list_items', sort_request="trending", explicit=True),
             "properties": {
                 "fanart_image": get_media("categories", "fanart.jpg"),
             },
             'offscreen': True},

            {'label': self.pct_plugin.tr('recently'),
             'icon': get_media("movies", "recently.png"),
             'thumbnail': get_media("movies", "recently.png"),
             'path': self.url_for('movies.list_items', sort_request="last_added", explicit=True),
             "properties": {
                 "fanart_image": get_media("categories", "fanart.jpg"),
             },
             'offscreen': True},

            {'label': self.pct_plugin.tr('rated'),
             'icon': get_media("movies", "rated.png"),
             'thumbnail': get_media("movies", "rated.png"),
             'path': self.url_for('movies.list_items', sort_request="rating", explicit=True),
             "properties": {
                 "fanart_image": get_media("categories", "fanart.jpg"),
             },
             'offscreen': True},

            {'label': self.pct_plugin.tr('genres'),
             'icon': get_media("movies", "genres.png"),
             'thumbnail': get_media("movies", "genres.png"),
             'path': self.url_for('movies.genres', explicit=True),
             "properties": {
                 "fanart_image": get_media("categories", "fanart.jpg"),
             },
             'offscreen': True},

            {'label': self.pct_plugin.tr('search'),
             'icon': get_media("movies", "search.png"),
             'thumbnail': get_media("movies", "search.png"),
             'path': self.url_for('movie_m.search', explicit=True),
             "properties": {
                 "fanart_image": get_media("categories", "fanart.jpg"),
             },
             'offscreen': True},
        ]
        return items

    def search(self):
        query = self.keyboard(heading=self.pct_plugin.tr('search'))
        if query:
            self.plugin.redirect(self.url_for('movies.search', keyword=query, explicit=True))


class MovieList(xbmcswift2.Module):

    def __init__(self, pct_plugin):
        super(MovieList, self).__init__('plugin.video.popcorntime.menu.movie_m.movies')

        self.pct_plugin = pct_plugin

        # decorators
        self.list_items = self.route('/movies/list_items/<sort_request>/<genre>/<page>',
                                     options={'genre': 'all', 'page': '1'})(self.list_items)
        self.search = self.route('/movies/search/<keyword>')(self.search)
        self.genres = self.route('/movies/genres')(self.genres)

    def list_items(self, sort_request, genre, page):
        self.pct_plugin.utils.log.debug(f"movies page : {page} - {genre}")
        items = MovieApi.get_movies(self.pct_plugin, page, sort_request, genre)

        items.append(
            {'label': self.pct_plugin.tr('show_more'),
             'icon': get_media("movies", "more.png"),
             'thumbnail': get_media("movies", "more_thumbnail.png"),
             'path': self.url_for('movies.list_items', sort_request=sort_request, page=str(int(page) + 1), genre=genre,
                                  explicit=True),
             'offscreen': True
             },
        )
        return items

    def search(self, keyword):
        self.pct_plugin.utils.log.debug(f"search : {keyword} ")
        return MovieApi.search_movies(self.pct_plugin, keyword)

    def genres(self):
        items = [
            {
                'label': self.pct_plugin.tr_id(key),
                'icon': get_media(os.path.join("movies", "genres"), f"{value}.png"),
                'thumbnail': get_media(os.path.join("movies", "genres"), f"{value}.png"),
                'path': self.url_for('movies.list_items', sort_request="trending", genre=value, explicit=True),
                "properties": {
                    "fanart_image": get_media("categories", "fanart.jpg"),
                },
                'offscreen': True
            } for key, value in API.genres.items()
        ]
        return items
