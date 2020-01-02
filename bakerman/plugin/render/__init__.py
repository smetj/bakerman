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

import sys
from typing import Dict


class Skeleton:
    """
    Base class for all Render plugin modules
    """

    def __init__(self, workdir: str, template: str, target: str) -> None:
        self.workdir = workdir
        self.template = template
        self.target = target

    def render(self, kwargs: Dict) -> None:
        """
        Renders the defined template using the provided `kwargs`.

        Args:
            kwargs: A dictionary of key/values used to render the template.
        """
        raise NotImplementedError(
            "`%s` method not implemented by `%s` plugin."
            % (sys._getframe().f_code.co_name, self.__class__)
        )
