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

from bakerman.plugin.repo import Skeleton
from bakerman.helper import getLogger
from bakerman.helper import executeCommand
from socket import gethostname
import os

logger = getLogger("plugin:repo:git")


def discovery(url, workdir):

    if executeCommand(["git", "-C", workdir, "status"], logger):
        return Handler
    elif url.endswith(".git"):
        return Handler
    else:
        return False


class Handler(Skeleton):
    def __init__(self, url, workdir):
        Skeleton.__init__(self, url, workdir)

    def checkPrerequisits(self):
        executeCommand(["which", "git"], logger)

    def checkValidRepo(self):

        try:
            executeCommand(
                ["git", "-C", self.workdir, "status"], logger,
            )
        except Exception:
            return False
        else:
            return True

    def clone(self):

        executeCommand(
            ["git", "-C", self.workdir, "clone", self.url, self.workdir], logger
        )

    def update(self):

        executeCommand(["git", "-C", self.workdir, "pull"], logger)

    def commit(self, message):
        hostname = gethostname()
        username = os.environ.get("USER")

        executeCommand(
            [
                "git",
                "-C",
                self.workdir,
                "commit",
                "--author",
                f"Bakerman <{username}@{hostname}>",
                "-m",
                message,
                self.workdir,
            ],
            logger,
        )

        self.__addIncrementedTag()

    def push(self):
        executeCommand(["git", "-C", self.workdir, "push"], logger)
        executeCommand(["git", "-C", self.workdir, "push", "--tags"], logger)

    def __addIncrementedTag(self):

        current_tag = self.__getLatestTag().split(".")
        current_tag[-1] = str(int(current_tag[-1]) + 1)
        tag = ".".join(current_tag)
        logger.debug(f"Tagging commit with '{tag}'")
        executeCommand(["git", "-C", self.workdir, "tag", f"{tag}"], logger)

    def __getLatestTag(self):

        result = executeCommand(
            ["git", "-C", self.workdir, "describe", "--abbrev=0", "--tag"],
            logger,
            return_output=True,
        )
        return result
