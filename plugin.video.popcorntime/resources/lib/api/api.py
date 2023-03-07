#!/usr/bin/env python

__license__ = "GPLv3"
__version__ = "3.0.0"
__author__ = "theRedMercury"

import json
from urllib.request import Request, urlopen


class API:
    header = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/30.0.1599.66 Safari/537.36",
        "Accept-Encoding": "none",
    }

    genres = {
        30400: "action",
        30401: "adventure",
        30402: "animation",
        30403: "comedy",
        30404: "crime",
        30405: "disaster",
        30406: "documentary",
        30407: "drama",
        30408: "eastern",
        30409: "family",
        30410: "fan-film",
        30411: "fantasy",
        30412: "film-noir",
        30413: "history",
        30414: "horror",
        30415: "indie",
        30416: "music",
        30417: "mystery",
        30418: "road",
        30419: "romance",
        30420: "science-fiction",
        30421: "short",
        30422: "sports",
        30423: "sporting-event",
        30424: "suspense",
        30425: "thriller",
        30427: "war",
        30428: "western"
    }

    """
    Search :    {domain}/{types}/1?keywords={keywords}
    List :      {domain}/{types}/{page}?genre={genre}&sort={sort}
    Season :    {domain}/{types}/{imdb_id}
    """

    @staticmethod
    def get_list(utils, dom_link, types, page, genre, sort_request):
        req = Request(
            f"{dom_link}/{types}/{page}?genre={genre}&sort={sort_request}",
            headers=API.header,
        )
        return API._get_request(utils, req)

    @staticmethod
    def get_list_show_all(utils, dom_link, types, id_show):
        req = Request(
            f"{dom_link}/{types}/{id_show}",
            headers=API.header,
        )
        return API._get_request(utils, req)

    @staticmethod
    def get_search(utils, dom_link, types, keywords):
        req = Request(
            f"{dom_link}/{types}/1?keywords={keywords}",
            headers=API.header,
        )
        return API._get_request(utils, req)

    @staticmethod
    def _get_request(utils, request):
        try:
            response = urlopen(request)
            results = json.loads(response.read())
            utils.log.debug(f"API : {request.get_full_url()} > {results}")
            return results

        except Exception as e:
            utils.log.warning(f"API request fail : {request.get_full_url()}")
            utils.log.warning(e)
            return {}
