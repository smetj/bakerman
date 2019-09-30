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
import semver
from functools import cmp_to_key


logger = getLogger("plugin:lookup:docker_hub")


def discovery(name):

    if name == "docker_hub":
        return Handler

    else:
        return False


class Handler:
    def __init__(self):
        pass
        # if "BAKERMAN_PLUGIN_DOCKER_HUB_TOKEN" in os.environ:
        #     logger.debug(
        #         "Found BAKERMAN_PLUGIN_DOCKER_HUB_TOKEN using that for authentication"
        #     )
        # else:
        #     logger.error(
        #         "Could not find BAKERMAN_PLUGIN_DOCKER_HUB_TOKEN environment variable."
        #     )
        #     sys.exit(1)

        # if "BAKERMAN_PLUGIN_DOCKER_HUB_USER" in os.environ:
        #     logger.debug(
        #         "Found BAKERMAN_PLUGIN_DOCKER_HUB_USER using that for authentication"
        #     )
        # else:
        #     logger.error(
        #         "Could not find BAKERMAN_PLUGIN_DOCKER_HUB_USER environment variable."
        #     )
        #     sys.exit(1)

    def lookup(self, name):

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
