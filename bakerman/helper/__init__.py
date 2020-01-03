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

import logging
import sys
import subprocess
from typing import Dict, Union, Any, List


# TODO(smetj): Can't define type of lookup_handler as I'm running into a circular import issue
def lookupVariables(lookup_handler: Any, manifest: List[dict]) -> Dict[str, str]:
    """
    Does a lookup for each variable defined in the manifest.

    Args:
        lookup_handler: A `bakerman.handler.discoverLookupHandler` instance.
        manifest: Dict representation of the manifest file.

    Returns:
        A dictionary containing each variable and lookup value.
    """
    manifest_value_render_cache = {}  # type: ignore
    variables = {}
    for entry in manifest:
        for value in entry["values"]:
            if entry["type"] not in manifest_value_render_cache:
                manifest_value_render_cache[entry["type"]] = lookup_handler(
                    entry["type"]
                )()
            variables[value["template_arg_name"]] = manifest_value_render_cache[
                entry["type"]
            ].lookup(**value["variables"])
    return variables


def getLogger(name=None) -> logging.Logger:
    """
    Returns a logger object

    Args:
        name: The name of the logger object

    Returns:
        The `logging.Logger` instance.
    """

    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)

    handler = logging.StreamHandler(sys.stdout)
    handler.setLevel(logging.DEBUG)
    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    return logger


def executeCommand(
    command: List[str], logger: logging.Logger, return_output=False
) -> Union[str, bool]:
    """
    Executes a command in a shell environment

    Args:
        command: The command to execute
        logger: The logger obect to log messages
        return_output: If `True` returns the `command` output.
    """
    c = " ".join(command)

    try:
        result = subprocess.run(command, capture_output=True, shell=False, check=True)
    except Exception as err:
        logger.debug(f"Failed to executed command '{c}'. Reason: {err}")
        raise Exception(f"Failed to executed command '{c}'. Reason: {err}")

    else:
        if result.returncode == 0:
            if return_output:
                return result.stdout.decode("utf-8").rstrip()
            else:
                return True
        else:
            output = result.stdout.decode("utf-8").rstrip()
            error = result.stderr.decode("utf-8").rstrip()
            logger.debug(f"Failed to execute command '{c}'. Reason: {error} {output}")
            raise Exception(
                f"Failed to execute command '{c}'. Reason: {error} {output}"
            )
