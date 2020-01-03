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
import semver  # type: ignore
from functools import cmp_to_key
from typing import Optional, Type

logger = getLogger("plugin:lookup:gitlab_registry")


def discovery(name: str) -> Optional[Type["GitlabRegistry"]]:
    """
    Function expected by the `bakerman.handler.discoverLookupHandler` factory
    function to determine `bakerman.plugin.lookup.gitlab_registry.Handler` is
    the required Plugin for `name`.

    Arguments:
        name: The name of the lookup type

    Returns:
        The `GitlabRegistry` class or None
    """

    if name == "gitlab_registry":
        return GitlabRegistry

    else:
        return None


class GitlabRegistry:
    """
    The Bakerman version lookup plugin for Gitlab registry Docker images. This
    plugin does make a naive assumption that containers are always versioned
    using semver.  If that's not the case the outcome might be unpredictable.
    A better implementation is welcome.
    """

    def lookup(
        self, project_id: int, path: str, host: str = "gitlab.com", token: str = None
    ) -> str:
        """
        Returns the latest available version off the container with name `name`.

        Args:
            project_id: The Gitlab project ID holding the registry
            path: The path name of the registry ex: smetj/container-postfix
            host: The API hostname
            token: The authentication token to authenticate.

        Returns:
            A version number.
        """
        registry_id = self.__getRegistryID(host, project_id, path, token)

        if token:
            r = requests.get(
                f"https://{host}/api/v4/projects/{project_id}/registry/repositories/{registry_id}/tags",
                headers={"PRIVATE-TOKEN": token},
            )
        else:
            r = requests.get(
                f"https://{host}/api/v4/projects/{project_id}/registry/repositories/{registry_id}/tags",
            )
        r.raise_for_status()
        tags = self.__extractValidTags(r.json())
        latest_tag = self.__getLatestTag(tags)
        logger.debug(f"The latest tag for '{path}' is '{latest_tag}'")
        return latest_tag

    def __extractValidTags(self, data):
        valid_tags = []

        for tag in data:
            try:
                semver.parse(tag["name"])
            except Exception:
                pass
            else:
                valid_tags.append(tag["name"])
        logger.debug(f"Valid tags are {valid_tags}")
        return valid_tags

    def __getLatestTag(self, tags):
        return sorted(tags, key=cmp_to_key(semver.compare))[-1]

    def __getRegistryID(self, host, project_id, path, token):

        if token:
            r = requests.get(
                f"https://{host}/api/v4/projects/{project_id}/registry/repositories",
                headers={"PRIVATE-TOKEN": token},
            )
        else:
            r = requests.get(
                f"https://{host}/api/v4/projects/{project_id}/registry/repositories"
            )

        r.raise_for_status()

        for item in r.json():
            if item["path"] == path:
                return item["id"]

        raise Exception(
            f"No Gitlab repository for project {project_id} with path {path}"
        )
