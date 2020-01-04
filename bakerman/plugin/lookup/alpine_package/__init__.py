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
from bs4 import BeautifulSoup  # type: ignore
from bakerman.helper import getLogger
from bakerman.plugin.lookup import Skeleton
from typing import Optional, Type

logger = getLogger("plugin:lookup:alpine_package")


def discovery(name: str) -> Optional[Type["AlpinePackage"]]:
    """
    Function expected by the `bakerman.handler.discoverLookupHandler` factory
    function to determine `bakerman.plugin.lookup.alpine_package.Handler` is
    the required Plugin for `name`.

    Arguments:
        name: The name of type of lookup

    Returns:
        The the `AlpinePackage` class or None.
    """

    if name == "alpine_package":
        return AlpinePackage
    else:
        return None


class AlpinePackage(Skeleton):
    """
    The Bakerman version lookup plugin for Alpine Packages.
    """

    def lookup(
        self, name: str, branch: str, repo: str = "main", arch: str = "x86_64"
    ) -> Optional[str]:
        """
        Returns the latest package version off the package with name `name`.

        Args:
            name: The name of the package to lookup the latest available version.
            branch: The Alpine branch name
            repo: The Alpine repo name
            arch: The platform architecture

        Returns:
            A version number.
        """

        logger.debug("Doing a lookup for %s" % (name))
        response = requests.get(
            f"https://pkgs.alpinelinux.org/packages?name={name}&branch={branch}&repo={repo}&arch={arch}"
        )

        page_content = BeautifulSoup(response.content, "html.parser")

        for item in page_content.find_all("td", class_="version"):
            return item.text

        return None
