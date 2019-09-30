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

import logging
import sys
import subprocess


def lookupVariables(handler, manifest):
    manifest_value_render_cache = {}
    variables = {}
    for entry in manifest:
        for value in entry["values"]:
            if entry["type"] not in manifest_value_render_cache:
                manifest_value_render_cache[entry["type"]] = handler(entry["type"])()
            variables[value["template_arg_name"]] = manifest_value_render_cache[
                entry["type"]
            ].lookup(value["name"])
    return variables


def getLogger(name=None):

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


def executeCommand(command, logger, return_output=False):
    c = " ".join(command)

    try:
        result = subprocess.run(command, capture_output=True, shell=False, check=True)
    except Exception as err:
        logger.error(f"Failed to executed command '{c}'. Reason: {err}")
        sys.exit(1)
    else:
        if result.returncode == 0:
            if return_output:
                return result.stdout.decode("utf-8").rstrip()
            else:
                return True
        else:
            output = result.stdout.decode("utf-8").rstrip()
            error = result.stderr.decode("utf-8").rstrip()
            logger.error(f"Failed to execute command '{c}'. Reason: {error} {output}")
            sys.exit(1)
