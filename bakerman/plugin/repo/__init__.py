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

import os
import sys
from bakerman.helper import getLogger

logger = getLogger("plugin::repo")


class Skeleton:
    def __init__(self, workdir, uri=None):
        self.uri = uri
        self.workdir = os.path.abspath(workdir)

        try:
            logger.info("Checking prerequisites")
            self.checkPrerequisits()
        except Exception as err:
            logger.error("Prerequisites not met. Reason: %s" % (err))
            sys.exit(1)

        self.prepareDirectory()

        if self.checkValidRepo():
            logger.debug("%s is a valid repository." % (self.workdir))
        elif uri:
            logger.debug("%s is a not a valid repository. Cloning." % (self.workdir))
            self.clone()
        else:
            logger.debug(
                "%s is a not a valid repository and no URI to clone. Giving up."
                % (self.workdir)
            )
            sys.exit(1)

    def checkPrerequisites(self):
        raise NotImplementedError(
            "`%s` method not implemented by `%s` plugin."
            % (sys._getframe().f_code.co_name, self.__class__)
        )

    def checkValidRepo(self):
        raise NotImplementedError(
            "`%s` method not implemented by `%s` plugin."
            % (sys._getframe().f_code.co_name, self.__class__)
        )

    def clone(self):
        raise NotImplementedError(
            "`%s` method not implemented by `%s` plugin."
            % (sys._getframe().f_code.co_name, self.__class__)
        )

    def commit(self, message):
        raise NotImplementedError(
            "`%s` method not implemented by `%s` plugin."
            % (sys._getframe().f_code.co_name, self.__class__)
        )

    def push(self):
        raise NotImplementedError(
            "`%s` method not implemented by `%s` plugin."
            % (sys._getframe().f_code.co_name, self.__class__)
        )

    def incrementTag(self):
        raise NotImplementedError(
            "`%s` method not implemented by `%s` plugin."
            % (sys._getframe().f_code.co_name, self.__class__)
        )

    def prepareDirectory(self):
        if not os.path.exists(self.workdir):
            os.mkdir(self.workdir)
            logger.debug("Creating directory %s" % (self.workdir))
        if not os.path.isdir(self.workdir):
            logger.error("'%s' is not a directory" % (self.workdir))
            sys.exit(1)
        if not os.access(self.workdir, os.R_OK) or not os.access(self.workdir, os.W_OK):
            logger.error("'%s' needs R/W access." % (self.workdir))
            sys.exit(1)
