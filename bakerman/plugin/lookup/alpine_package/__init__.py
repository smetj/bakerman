#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  __init__.py
#
#  Copyright 2018 Jelle Smet <development@smetj.net>
#
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 3 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.
#
#

import requests
from bs4 import BeautifulSoup
from bakerman.helper import getLogger

logger = getLogger("plugin:lookup:alpine_package")


def discovery(name):

    if name == "alpine_package":
        return Handler

    else:
        return False


class Handler:
    def __init__(self):
        pass

    def lookup(self, name):

        logger.debug("Doing a lookup for %s" % (name))
        response = requests.get(
            f"https://pkgs.alpinelinux.org/packages?name={name}&branch=v3.10&repo=main&arch=x86_64"
        )

        page_content = BeautifulSoup(response.content, "html.parser")

        for item in page_content.find_all("td", class_="version"):
            return item.text
