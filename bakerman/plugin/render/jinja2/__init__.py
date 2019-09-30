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

logger = getLogger("plugin:render:jinja2")


def discovery(workdir, template):

    env = jinja2.Environment()
    try:
        with open("%s/%s" % (workdir, template)) as t:
            env.parse(t.read())
    except Exception as err:
        logger.debug(
            "%s/%s is not a valid jinja2 template. Reason: %s"
            % (workdir, template, err)
        )
        return False
    else:
        logger.debug(
            "%s/%s is a valid jinja2 template. Picking Jinja2 as template renderer."
            % (workdir, template)
        )
        return Handler


class Handler(Skeleton):
    def __init__(self, workdir, template, dockerfile):

        self.workdir = workdir
        self.template = template
        self.dockerfile = dockerfile

    def render(self, kwargs):
        with open(f"{self.workdir}/{self.template}") as r:
            template = jinja2.Template("".join(r.readlines()))
            with open(f"{self.workdir}/{self.dockerfile}", "w") as w:
                logger.debug(f"Writing {self.workdir}/{self.dockerfile}.")
                w.write(template.render(**kwargs))
