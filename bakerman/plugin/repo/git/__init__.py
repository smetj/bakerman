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
from socket import gethostname
from typing import Type, Optional
from git import Repo  # type: ignore
from git.remote import Remote  # type: ignore
from git.util import Actor
import os
import semver  # type: ignore
import git


logger = getLogger("plugin:repo:git")


def discovery(uri: str, workdir: str) -> Optional[Type["Git"]]:
    """
    Function expected by the `bakerman.handler.discoverRepoHandler` factory
    function to determine `bakerman.plugin.lookup.alpine_package.Handler` is
    the required Plugin for `name`.

    Arguments:
        uri: The CVS URI.
        workdir: The directory to store the CVS content

    Returns:
        The the `Git` class or None.
    """

    if uri and uri.endswith(".git"):
        return Git
    elif Repo(workdir).git_dir:
        return Git
    else:
        return None


class Git(Skeleton):
    def __init__(self, uri: str, workdir: str) -> None:
        """
        The Bakerman CVS plugin handler for Git.

        Arguments:
            uri: The Git based repo URI
            workdir: The directory containing the repo
        """

        Skeleton.__init__(self, uri=uri, workdir=workdir)

    def checkPrerequisits(self) -> None:
        """
        Validates whether we can find the "git" command.
        """

        return None

    def checkValidRepo(self) -> bool:

        if Repo(self.workdir).git_dir:
            return True
        else:
            return False

    def clone(self) -> None:

        Repo().clone_from(self.uri, self.workdir)
        return None

    def commit(self, message: str) -> None:
        git.cmd.Git(self.workdir).commit(["-m", message, "-a"])
        logger.debug(f"Committed changes.")
        self.__addIncrementedTag()

        return None

    def push(self) -> None:
        git.cmd.Git(self.workdir).push(["--tags", "origin", "master"])
        logger.debug(f"Pushing commit.")
        return None

    def __addIncrementedTag(self) -> None:

        current_tag = self.__getLatestTag()
        if current_tag is None:
            tag = "1.0.0"
        else:
            tag = semver.bump_minor(current_tag)

        git.cmd.Git(self.workdir).tag([tag])

        logger.debug(f"Added tag {tag} to current commit.")

        return None

    def __getLatestTag(self) -> Optional[str]:

        try:
            return git.cmd.Git("./").describe(["--abbrev=0", "--tag"])
        except git.exc.GitCommandError:
            return None
