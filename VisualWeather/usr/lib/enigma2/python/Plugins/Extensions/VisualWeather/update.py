#!/usr/bin/python
# -*- coding: utf-8 -*-

from .plugin import cfg, pythonVer, weather_json, hdr
from requests.adapters import HTTPAdapter
from collections import OrderedDict

import os
import json
import requests

if pythonVer == 2:
    from urllib import quote
else:
    from urllib.parse import quote


def VisualWeather_Update():
    if os.path.isfile(weather_json):
        os.remove(weather_json)

    elements = [
        "datetime",
        "datetimeEpoch",
        "name",
        "address",
        "resolvedAddress",
        # "latitude",
        # "longitude",
        "tempmax",
        "tempmin",
        "temp",
        # "feelslikemax",
        # "feelslikemin",
        "feelslike",
        # "dew",
        "humidity",
        "precip",
        "precipprob",
        # "precipcover",
        "preciptype",
        "snow",
        # "snowdepth",
        # "windgust",
        "windspeed",
        "winddir",
        "pressure",
        # "cloudcover",
        # "visibility",
        # "solarradiation",
        # "solarenergy",
        "uvindex",
        "severerisk",
        "sunrise",
        "sunset",
        "moonphase",
        "conditions",
        "description",
        "icon",
        "stations",
        "source"

    ]

    include = [
        "fcst",
        "obs",
        "stats",
        "remote",
        "statsfcst",
        "days",
        "hours",
        "alerts",
        "events",
        "current"
    ]

    elementsstring = quote(",".join(elements))
    includestring = quote(",".join(include))

    location = cfg.location.value
    unitGroup = cfg.units.value
    language = cfg.language.value
    key = cfg.apikey.value
    contentType = "json"

    url = "https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/" + str(location) + "?unitGroup=" + str(unitGroup) + "&elements=" + str(elementsstring) \
        + "&include=" + str(includestring) + "&key=" + str(key) + "&contentType=" + str(contentType) + "&iconSet=icons2" + "&lang=" + str(language)

    adapter = HTTPAdapter()
    http = requests.Session()
    http.mount("http://", adapter)
    http.mount("https://", adapter)

    try:
        r = http.get(url, headers=hdr, verify=False, allow_redirects=True)

        r.raise_for_status()
        if r.status_code == requests.codes.ok:
            try:
                content = r.json()

                with open(weather_json, "w") as f:
                    json.dump(OrderedDict(content), f)
            except Exception as e:
                print(e)
                content = ""

    except Exception as e:
        print(e)
