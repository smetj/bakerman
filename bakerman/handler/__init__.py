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

from bakerman.plugin import repo
from bakerman.plugin.repo import Skeleton as SkeletonRepo

from bakerman.plugin import render
from bakerman.plugin.render import Skeleton as SkeletonRender

from bakerman.plugin import manifest
from bakerman.plugin.manifest import Skeleton as SkeletonManifest

from bakerman.plugin import lookup
from bakerman.plugin.lookup import Skeleton as SkeletonLookup

import importlib
import pkgutil

from typing import Type


def discoverRepoHandler(uri: str, workdir: str) -> Type[SkeletonRepo]:
    """
    Factory function which returns a suitable Module for the provided arguments.

    Args:
        uri: The CVS URI identifying the remote repository.
        workdir: The directory to which the remote repo will be stored.

    Returns:
        A `bakerman.plugin.repo` module capable to handle `uri`.

    Raises:

        NotImplementedError: No suitable repo plugin was found for the
                             provided `uri`.
    """

    for repo_plugin in pkgutil.iter_modules(repo.__path__):  # type: ignore  # mypy issue #1422
        module = importlib.import_module(
            ".plugin.repo.%s" % repo_plugin.name, package="bakerman"
        )
        m = module.discovery(uri=uri, workdir=workdir)  # type: ignore # I don't understand this
        if m:
            return m

    raise NotImplementedError("No suitable 'repo' plugin found for '%s'" % (uri))


def discoverRenderHandler(workdir: str, filename: str) -> Type[SkeletonRender]:
    """
    Factory function which returns a suitable Module for the provided arguments.

    Args:
        workdir: The location containing the filename.
        filename: The name of the template file for which a suitable plugin
                  has to be discovered.

    Returns:
        A `bakerman.plugin.render` module capable to handle `filename`.

    Raises:
        NotImplementedError: No suitable repo plugin was found for the
                             provided `filename`.
    """
    for plugin in pkgutil.iter_modules(render.__path__):  # type: ignore  # mypy issue #1422
        module = importlib.import_module(
            ".plugin.render.%s" % plugin.name, package="bakerman"
        )
        m = module.discovery(workdir, filename)  # type: ignore
        if m:
            return m

    raise NotImplementedError(
        "No suitable 'render' plugin found for '%s/%s'" % (workdir, filename)
    )


def discoverManifestHandler(workdir: str, filename: str) -> Type[SkeletonManifest]:
    """
    Factory function which returns a suitable Module for the provided arguments.

    Args:
        workdir: The location containing the filename.
        filename: The name of the template file for which a suitable plugin
                  has to be discovered.

    Returns:
        A `bakerman.plugin.render` module capable to handle `filename`.

    Raises:
        NotImplementedError: No suitable repo plugin was found for the
                             provided `filename`.
    """
    for plugin in pkgutil.iter_modules(manifest.__path__):  # type: ignore  # mypy issue #1422
        module = importlib.import_module(
            ".plugin.manifest.%s" % plugin.name, package="bakerman"
        )
        m = module.discovery(workdir, filename)  # type: ignore
        if m:
            return m

    raise NotImplementedError(
        "No suitable 'manifest' plugin found for '%s/%s'" % (workdir, filename)
    )


def discoverLookupHandler(name: str) -> Type[SkeletonLookup]:
    """
    Factory function which returns a suitable Module for the provided arguments.

    Args:
        name: A string identifying the lookup type.  The `discovery` functions
              use this string to identify the plugin.

    Returns:
        A `bakerman.plugin.render` module capable to handle `filename`.

    Raises:
        NotImplementedError: No suitable repo plugin was found for the
                             provided `filename`.
    """
    for plugin in pkgutil.iter_modules(lookup.__path__):  # type: ignore  # mypy issue #1422
        module = importlib.import_module(
            ".plugin.lookup.%s" % plugin.name, package="bakerman"
        )
        m = module.discovery(name)  # type: ignore
        if m:
            return m

    raise NotImplementedError("No suitable 'lookup' plugin found for type '%s" % (name))
