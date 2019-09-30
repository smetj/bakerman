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
from bakerman.plugin import render
from bakerman.plugin import manifest
from bakerman.plugin import lookup
import importlib
import pkgutil


def discoverRepoHandler(url, workdir):

    for repo_plugin in pkgutil.iter_modules(repo.__path__):
        module = importlib.import_module(
            ".plugin.repo.%s" % repo_plugin.name, package="bakerman"
        )
        m = module.discovery(url, workdir)
        if m:
            return m

    raise NotImplementedError("No suitable 'repo' plugin found for '%s'" % (url))


def discoverRenderHandler(workdir, template):

    for plugin in pkgutil.iter_modules(render.__path__):
        module = importlib.import_module(
            ".plugin.render.%s" % plugin.name, package="bakerman"
        )
        m = module.discovery(workdir, template)
        if m:
            return m

    raise NotImplementedError(
        "No suitable 'render' plugin found for '%s/%s'" % (workdir, template)
    )


def discoverManifestHandler(workdir, man):

    for plugin in pkgutil.iter_modules(manifest.__path__):
        module = importlib.import_module(
            ".plugin.manifest.%s" % plugin.name, package="bakerman"
        )
        m = module.discovery(workdir, man)
        if m:
            return m

    raise NotImplementedError(
        "No suitable 'manifest' plugin found for '%s/%s'" % (workdir, manifest)
    )


def discoverLookupHandler(name):

    for plugin in pkgutil.iter_modules(lookup.__path__):
        module = importlib.import_module(
            ".plugin.lookup.%s" % plugin.name, package="bakerman"
        )
        m = module.discovery(name)
        if m:
            return m

    raise NotImplementedError("No suitable 'lookup' plugin found for type '%s" % (name))
