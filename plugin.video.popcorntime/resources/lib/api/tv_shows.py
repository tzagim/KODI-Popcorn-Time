#!/usr/bin/env python

__license__ = "GPLv3"
__version__ = "3.0.0"
__author__ = "theRedMercury"

from resources.lib.api.api import API
from resources.lib.utils import get_setting


class TvShowAPI:
    types = "shows"
    type_season = "show"

    domains = [
        "https://movies-api.ga",
        "https://movies-api.tk",
        "https://popcorn-time.ga",
        "https://shows.cf",
    ]

    def __init__(self):
        pass

    @staticmethod
    def get_tvshows(plugin, page, sort_request, genre):
        json_reply = {}
        for dom in TvShowAPI.domains:
            json_reply = API.get_list(plugin.pct_plugin.utils, dom, TvShowAPI.types, page, genre, sort_request)
            if json_reply != {}:
                continue

        return TvShowAPI.populate_shows(plugin, json_reply)

    @staticmethod
    def search(plugin, keyword):
        json_reply = {}
        for dom in TvShowAPI.domains:
            json_reply = API.get_search(plugin.pct_plugin.utils, dom, TvShowAPI.types, keyword)
            if json_reply != {}:
                continue

        return TvShowAPI.populate_shows(plugin, json_reply)

    @staticmethod
    def get_tvshows_episodes(plugin, id_show, season):
        json_reply = {}
        for dom in TvShowAPI.domains:
            json_reply = API.get_list_show_all(plugin.pct_plugin.utils, dom, TvShowAPI.type_season, id_show)
            if json_reply != {}:
                continue
        return TvShowAPI.populate_episodes(plugin, json_reply, season)

    @staticmethod
    def populate_shows(plugin, json_reply):
        items = []
        for result in json_reply:
            item = {
                "label": result.get('title'),
                "icon": result.get('images').get('poster'),
                "thumbnail": result.get('images').get('poster'),
                "properties": {
                    "fanart_image": result.get('images').get('fanart').replace('/w500/', '/original/'),
                },

                "info": {
                    'mediatype': 'tvshow',
                    'title': result.get('title'),
                    'year': int(result.get('year')),
                    'genre': ', '.join(genre for genre in result.get('genres', [])) or None,
                    'rating': float(int(result.get('rating').get('percentage')) / 10),
                    'votes': result.get('rating').get('votes'),
                    'imdbnumber': result.get('imdb_id'),
                    'code': result.get('imdb_id'),
                    'plot': result.get('synopsis'),
                },

                "path": plugin.url_for("tv_shows.list_items_season",
                                       id_show=result.get('imdb_id'),
                                       num_seasons=result.get('num_seasons'),
                                       fanart=result.get('images').get('fanart').replace('/w500/', '/original/')),
            }

            items.append(item)
        return items

    @staticmethod
    def populate_episodes(plugin, json_reply, season):
        items = []

        quality_ask = get_setting("movies_quality") or '4k'
        quality_ask = '2160p' if quality_ask == '4k' else quality_ask

        for episode in json_reply.get('episodes'):
            if int(episode.get('season')) == int(season):

                stats_torrents = ""
                stats_torrents_full = ""
                quality = sorted(list(episode.get('torrents').keys()), key=lambda x: int(x[:-1] if len(x) > 1 else x),
                                 reverse=True) or []

                quality_found = quality_ask if quality_ask in episode.get('torrents').keys() else quality[0]

                for q in quality:
                    stats_torrents += f"{str(q).ljust(5, ' ')} | S({episode.get('torrents').get(q).get('seeds')}) / P({episode.get('torrents').get(q).get('peers')})\n"
                for q in quality:
                    stats_torrents_full += f"{str(q).ljust(5, ' ')} | Seed({episode.get('torrents').get(q).get('seeds')}) / Peer({episode.get('torrents').get(q).get('peers')})\n"

                magnet_url = episode.get('torrents').get(quality_found).get('url')

                menu = []
                for q in quality:
                    menu.append((f"Play {q}",
                                 f"RunPlugin(plugin://plugin.video.torrest/play_magnet?magnet={episode.get('torrents').get(q).get('url')})"))

                item = {
                    "label": f"{episode.get('episode')} : {episode.get('title')}",
                    "icon": json_reply.get('images').get('poster'),
                    "thumbnail": json_reply.get('images').get('poster'),
                    "properties": {
                        "fanart_image": json_reply.get('images').get('fanart').replace('/w500/', '/original/'),
                    },

                    "info": {
                        'mediatype': 'episode',
                        'season': episode.get('season'),
                        'episode': episode.get('episode'),
                        'plot': stats_torrents_full + (episode.get('overview') or ""),
                        'imdbnumber': json_reply.get('imdb_id'),
                        'code': json_reply.get('imdb_id'),
                        'tagline': ' / '.join(quality),
                        'year': int(json_reply.get('year')),
                        'genre': ', '.join(genre for genre in json_reply.get('genres', [])) or None,
                        'rating': float(int(json_reply.get('rating').get('percentage')) / 10),
                        'votes': json_reply.get('rating').get('votes'),
                    },

                    "context_menu": menu,
                    "is_playable": True,
                    "replace_context_menu": True,
                    "path": f"plugin://plugin.video.torrest/play_magnet?magnet={magnet_url}",
                }

                items.append(item)

        items = sorted(items, key=lambda x: int(x.get('info').get('episode')))
        return items
