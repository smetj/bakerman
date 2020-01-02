#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  __init__.py
#
#  Copyright 2018 Jelle Smet <development@smetj.net>
#
#  This rpogram is free software; you can redistribute it and/or modify
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

import jinja2
from bakerman.helper import getLogger
from bakerman.plugin.render import Skeleton
from typing import Type, Optional, Dict

logger = getLogger("plugin:render:jinja2")


def discovery(workdir: str, filename: str) -> Optional[Type["Jinja2"]]:
    """
    Function expected by the `bakerman.handler.discoverRenderHandler` factory
    function to determine `bakerman.plugin.render.jinja2.Handler` is
    the required Plugin for `filename`.

    Arguments:
        workdir: The directory containing the template
        filename: The file name of the template

    Returns:
        The the `Jinja2` class or None.
    """

    env = jinja2.Environment()
    try:
        with open("%s/%s" % (workdir, filename)) as t:
            env.parse(t.read())
    except Exception as err:
        logger.debug(
            "%s/%s is not a valid jinja2 template. Reason: %s"
            % (workdir, filename, err)
        )
        return None
    else:
        logger.debug(
            "%s/%s is a valid jinja2 template. Picking Jinja2 as template renderer."
            % (workdir, filename)
        )
        return Jinja2


class Jinja2(Skeleton):
    def __init__(self, workdir: str, template: str, target: str) -> None:
        """
        Bakerman render plugin offering Jinja2 support.

        Args:
            workdir: The directory containing the template file
            template: The filename of the template
            target: The target file containing the rendered result.
        """

        self.workdir = workdir
        self.template = template
        self.target = target

    def render(self, kwargs: Dict) -> None:
        with open(f"{self.workdir}/{self.template}") as r:
            template = jinja2.Template("".join(r.readlines()))
            with open(f"{self.workdir}/{self.target}", "w") as w:
                logger.debug(f"Writing {self.workdir}/{self.target}.")
                w.write(template.render(**kwargs))
