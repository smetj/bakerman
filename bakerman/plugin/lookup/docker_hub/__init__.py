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

from bakerman.helper import getLogger
import requests
import sys
import semver  # type: ignore
from functools import cmp_to_key
from typing import Optional, Type

logger = getLogger("plugin:lookup:docker_hub")


def discovery(name: str) -> Optional[Type["DockerHub"]]:
    """
    Function expected by the `bakerman.handler.discoverLookupHandler` factory
    function to determine `bakerman.plugin.lookup.docker_hub.Handler` is
    the required Plugin for `name`.

    Arguments:
        name: The name of the lookup type

    Returns:
        The `DockerHub` class or None
    """

    if name == "docker_hub":
        return DockerHub

    else:
        return None


class DockerHub:
    """
    The Bakerman version lookup plugin for Docker Hub docker images. This
    plugins does make a naive assumption that containers are always versioned
    using semver.  If that's not the case the outcome might be unpredictable.
    A better implementation is welcome.
    """

    def lookup(self, name) -> str:
        """
        Returns the latest available version off the container with name `name`.

        Args:
            name: The name of the package to lookup the latest available version.

        Returns:
            A version number.
        """

        token = self.__getToken(None, None, name)

        headers = {"Authorization": f"Bearer {token}"}
        r = requests.get(
            f"https://index.docker.io/v2/library/{name}/tags/list", headers=headers
        )

        tags = self.__extractValidTags(r.json())
        latest_tag = self.__getLatestTag(tags)
        logger.debug(f"The latest tag for '{name}' is '{latest_tag}'")
        return latest_tag

    def __extractValidTags(self, data):
        valid_tags = []
        for tag in data["tags"]:
            try:
                semver.parse(tag)
            except Exception:
                pass
            else:
                valid_tags.append(tag)
        logger.debug(f"Valid tags are {valid_tags}")
        return valid_tags

    def __getLatestTag(self, tags):
        return sorted(tags, key=cmp_to_key(semver.compare))[-1]

    def __getToken(self, username, token, image, auth_url="https://auth.docker.io"):

        payload = {
            "service": "registry.docker.io",
            "scope": f"repository:library/{image}:pull",
        }

        r = requests.get(auth_url + "/token", params=payload)
        if not r.status_code == 200:
            logger.error(f"Unable to authenticate to {auth_url}. Reason: {r.text}")
            sys.exit(1)
        return r.json()["token"]
