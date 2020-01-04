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
import argparse

import sys
from bakerman.handler import discoverRepoHandler
from bakerman.handler import discoverRenderHandler
from bakerman.handler import discoverManifestHandler
from bakerman.handler import discoverLookupHandler
from bakerman.helper import lookupVariables
from bakerman.helper import getLogger

COMMIT_MESSAGE = """
Bakerman committed following changes:
%s
"""


def parseArguments() -> argparse.Namespace:
    """
    Defines and parses the CLI provided arguments.

    Returns:
        - NameSpace object containing all arguments
    """

    parser = argparse.ArgumentParser(
        description="Automatically regenerate config files to include the latest artifact versions.",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument(
        "--repo",
        type=str,
        dest="repo",
        default=None,
        help="The URL of the repository to update. If omitted --workdir is expected to already contain a repo.",
    )
    parser.add_argument(
        "--manifest",
        type=str,
        dest="manifest",
        default="bakerman.manifest",
        help="The Bakerman manifest containing the package and container versions.",
    )
    parser.add_argument(
        "--template",
        type=str,
        dest="template",
        default="bakerman.template",
        help="The template to render.",
    )
    parser.add_argument(
        "--workdir",
        type=str,
        dest="workdir",
        required=True,
        help="The local workdir containing the repository",
    )
    parser.add_argument(
        "--target",
        type=str,
        dest="target",
        default="bakerman.target",
        help="The path of the target build file which --template will render into.",
    )
    parser.add_argument(
        "--no-repo",
        dest="no_repo",
        default=False,
        action="store_true",
        help="If defined, no repo commit & push is done.",
    )

    return parser.parse_args()


def start(args: argparse.Namespace) -> None:
    """
    Main Bakerman logic.
    Performs

    Raises:
        Exception: An unhandled error happened and should be made clear to the
        user as this indicates a bug for which a report should be made.
    """

    logger = getLogger("main")
    commit_message = []
    try:

        # Get the repository handler which is responsible for doing all the
        # CVS interaction in which the container build and Bakerman files are
        # stored.
        repo_cls = discoverRepoHandler(workdir=args.workdir, uri=args.repo)
        repo = repo_cls(uri=args.repo, workdir=args.workdir)

        # Get the render handler which is responsible for rendering the
        # `--template` file using the arguments the manifest handler comes up
        # with
        render_cls = discoverRenderHandler(args.workdir, args.template)
        target_file = render_cls(args.workdir, args.template, args.target)

        # Get the manifest handler which is responsible for reading and
        # writing the manifest file and returning a Python data structure.
        manifest_cls = discoverManifestHandler(args.workdir, args.manifest)
        manifest = manifest_cls(args.workdir, args.manifest)
        manifest_content = manifest.read()

        # Get all the different lookup handlers needed to discover the latest
        # values requested in the manifest file.  lookupVariables() is just a
        # convenience function which takes care of this.
        variables = lookupVariables(discoverLookupHandler, manifest_content)

        # Update the content of the manifest for each variable we have found.
        # And write it
        for key, value in variables.items():
            if manifest.updateVariable(key, value):
                message = f"Variable '{key}' has been updated to '{value}'."
                commit_message.append("- " + message)
                logger.info(message)
            else:
                logger.debug(f"Variable '{key}' has not changed.")

        # Write the manifest to disk
        manifest_updated = manifest.write()

        # Render the template file using the new found version numbers.
        if manifest_updated:
            logger.info(
                f"The manifest has been updated. Regenerating target file '{args.workdir}/{args.target}'"
            )
            target_file.render(variables)

            if args.no_repo:
                logger.info(f"--no-repo set, not committing nor pushing any changes.")
            else:
                logger.info(f"Committing changes and pushing repo.")
                repo.commit(COMMIT_MESSAGE % "\n".join(commit_message))
                repo.push()
        else:
            logger.info(
                f"The manifest has not been updated. Not regenerating target file '{args.workdir}/{args.target}'"
            )

    except NotImplementedError as err:
        logger.error("Fatal Error. Reason: %s" % (err))
        sys.exit(1)

    except Exception as err:
        print(
            "An unhandled error occurred. Please submit a bug report including the manifest, template and CLI command used. Reason: %s"
            % (err)
        )
        raise


def main():

    arguments = parseArguments()
    start(arguments)


if __name__ == "__main__":
    main()
