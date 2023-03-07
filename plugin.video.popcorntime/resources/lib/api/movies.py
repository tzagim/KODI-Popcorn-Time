#!/usr/bin/env python

__license__ = "GPLv3"
__version__ = "3.0.0"
__author__ = "theRedMercury"

import re

from resources.lib.api.api import API
from resources.lib.utils import get_setting


class MovieApi:
    types = "movies"

    domains = [
        "https://movies-api.ga",
        "https://movies-api.tk",
        "https://popcorn-time.ga",
        "https://shows.cf",
    ]

    def __init__(self):
        pass

    @staticmethod
    def get_movies(pct_plugin, page, sort_request, genre):
        json_reply = {}
        for dom in MovieApi.domains:
            json_reply = API.get_list(pct_plugin.utils, dom, MovieApi.types, page, genre, sort_request)
            if json_reply != {}:
                continue
        return MovieApi.populate_items(pct_plugin, json_reply)

    @staticmethod
    def search_movies(pct_plugin, keyword):
        json_reply = {}
        for dom in MovieApi.domains:
            json_reply = API.get_search(pct_plugin.utils, dom, MovieApi.types, keyword)
            if json_reply != {}:
                continue
        return MovieApi.populate_items(pct_plugin, json_reply)

    @staticmethod
    def populate_items(pct_plugin, json_reply):

        first_l = get_setting("first_lang_video")
        quality_ask = get_setting("movies_quality") or '4k'
        quality_ask = '2160p' if quality_ask == '4k' else quality_ask

        items = []
        for result in json_reply:

            keys_language = list(result.get('torrents').keys()) or ['en']
            quality = sorted([list(result.get('torrents').get(k).keys()) for k in result.get('torrents').keys()][0],
                             key=lambda x: int(x[:-1] if len(x) > 1 else x), reverse=True) or []
            quality_found = quality_ask if quality_ask in result.get('torrents').get(keys_language[0]).keys() else \
                quality[0]

            stats_torrents = ""
            stats_torrents_full = ""

            for lang in keys_language:
                for q in quality:
                    stats_torrents += f"{str(q).ljust(5, ' ')} : {result.get('torrents').get(lang).get(q).get('filesize')} | S({result.get('torrents').get(lang).get(q).get('seed')}) / P({result.get('torrents').get(lang).get(q).get('peer')})\n"

            stats_torrents += "lang : " + str(keys_language) + "\n"

            for lang in keys_language:
                for q in quality:
                    stats_torrents_full += f"{str(q).ljust(5, ' ')} : {result.get('torrents').get(lang).get(q).get('filesize')} | Seed({result.get('torrents').get(lang).get(q).get('seed')}) / Peer({result.get('torrents').get(lang).get(q).get('peer')})\n"

            magnet_url = result.get('torrents').get(keys_language[0]).get(quality_found).get('url')

            # SUB MENU
            menu = []
            for q in quality:
                menu.append((f"Play {q}",
                             f"RunPlugin(plugin://plugin.video.torrest/play_magnet?magnet={result.get('torrents').get(keys_language[0]).get(q).get('url')})"))
            """
            # Useless 
            menu.append((pct_plugin.tr("add_favorite"),
                         f"RunPlugin(plugin://plugin.video.popcorntime?cmd=add_fav&action=movies&id={result.get('imdb_id')})"))
            """

            """
            # Not supported
            for q in quality:
                menu.append((f"Download {q}",
                             f"RunPlugin(plugin://plugin.video.torrest/insert?magnet={result.get('torrents').get(keys_language[0]).get(q).get('url')})"))
            """

            item = {
                "label": result.get('title'),
                "icon": result.get('images').get('poster'),
                "thumbnail": result.get('images').get('poster'),
                "properties": {
                    "fanart_image": result.get('images').get('fanart').replace('/w500/', '/original/'),
                },

                "info": {
                    'mediatype': 'movie',
                    'title': result.get('title'),
                    'duration': int(result.get('runtime')) * 60 or 0,
                    'tagline': ' / '.join(quality),
                    'year': int(result.get('year')),
                    'genre': ', '.join(genre for genre in result.get('genres', [])) or None,
                    'rating': float(int(result.get('rating').get('percentage')) / 10),
                    'votes': result.get('rating').get('votes'),
                    'imdbnumber': result.get('imdb_id'),
                    'code': result.get('imdb_id'),
                    'mpaa': result.get('certification'),
                    'plot': (result.get('synopsis') or "") + "\n" + stats_torrents_full,
                    'plotoutline': stats_torrents + (result.get('synopsis') or ""),
                    'trailer': MovieApi._get_item_trailer(result.get('trailer')),
                },

                "context_menu": menu,
                "is_playable": True,
                "replace_context_menu": True,

                "path": f"plugin://plugin.video.torrest/play_magnet?magnet={magnet_url}",
            }
            items.append(item)

        return items

    @staticmethod
    def _get_item_trailer(trailer_url):
        trailer = ''
        try:
            trailer_regex = re.match('^[^v]+v=(.{11}).*', trailer_url)
            trailer_id = trailer_regex.group(1)
            trailer = 'plugin://plugin.video.youtube/?action=play_video&videoid=%s' % trailer_id
        except:
            pass
        return trailer
