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

import json
from bakerman.plugin.manifest import Skeleton
from bakerman.helper import getLogger
from typing import List, Dict, Optional, Type


logger = getLogger("plugin:manifest:json")


def discovery(workdir: str, manifest: str) -> Optional[Type["JSON"]]:
    """
    Function expected by the `bakerman.handler.discoverLookupHandler` factory
    function to determine `bakerman.plugin.lookup.docker_hub.Handler` is
    the required Plugin for `name`.

    Arguments:
        workdir: The directory containing the manifest.
        manifest: The file name of the manifest.

    Returns:
        The `JSON` class or `None`
    """

    try:
        with open("%s/%s" % (workdir, manifest)) as j:
            json.load(j)
    except Exception as err:
        logger.debug(
            "%s/%s is not a valid JSON file. Reason: %s" % (workdir, manifest, err)
        )
        return None
    else:
        logger.debug(
            "%s/%s is a valid JSON file. Picking JSON as manifest handler."
            % (workdir, manifest)
        )
        return JSON


class JSON(Skeleton):
    def __init__(self, workdir: str, filename: str) -> None:
        """
        The Bakerman manifest handling plugin responsible for reading,
        manipulating and updating the Bakerman manifest file.

        Arguments:
            workdir: The directory containing the manifest file
            filename: The filename of the manifest file.
        """

        self.workdir = workdir
        self.filename = filename
        self.__cache: List[Dict] = []
        self.__changed = False

    def read(self) -> List[Dict]:
        """
        Reads and returns the content of the manifest file.

        Returns:
            The contente of the manifest file.
        """

        with open(f"{self.workdir}/{self.filename}") as f:
            self.__cache = json.load(f)
            return self.__cache

    def updateVariable(self, name: str, value: str) -> bool:
        """
        Updates the version of a variable.

        Arguments:
            name: The name of the argument
            value: The new version value

        Returns:
            `True` when the value has been updated `False` if not.
        """

        for index_1, item in enumerate(self.__cache):
            for index_2, variable in enumerate(item["values"]):
                if (
                    name == variable["template_arg_name"]
                    and value != variable["current_value"]
                    and not variable["locked"]
                ):
                    self.__cache[index_1]["values"][index_2]["current_value"] = value
                    self.__changed = True
                    return True
        return False

    def write(self) -> bool:
        """
        Write the updated version of the manifest back to disk.
        """
        if self.__changed is True:
            logger.debug("The manifest has changed. Writing differences.")
            with open(f"{self.workdir}/{self.filename}", "w") as f:
                f.write(json.dumps(self.__cache, sort_keys=True, indent=2))
            return True
        else:
            logger.debug("The manifest has not changed.")
            return False
