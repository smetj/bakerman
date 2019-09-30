# Bakerman

Freshly baked containers

**Bakerman is in alpha development status**

## Introduction

Bakerman is a tool to automatically update repositories containing Docker
image container build files to include the latest available version of the
base container (FROM) and any other packages installed.

When a Dockerfile is regenerated, the changes get committed and pushed to your
repository, ideally triggering a rebuild of the container by your build system
resulting into always up-to-date containers using clear explicit versions.

Currently there's basic support for looking up the latest container from
docker hub and the latest version of a alpine packages. Bakerman has a plugin
system which should make it straight forward to plugin additional sources.

## Flow

The following logic steps are executed by Bakerman:

    # Clone or update `--repo` into `--workdir`.
    # Read the manifest file `manifest` and retrieve the latest versions of
      the defined variables.
    # Render `--template` using the version found in step 2 and write the
      outcome to `--dockerfile`.
    # Commit the changes defining which values have been updated.
    # Push commits to the remote repository.

## Usage

```
$ bakerman --help
usage: bakerman [-h] --repo REPO [--manifest MANIFEST] [--template TEMPLATE] [--workdir WORKDIR] [--dockerfile DOCKERFILE]

Update your Dockerfiles to include the latest containers and packages.

optional arguments:
  -h, --help            show this help message and exit
  --repo REPO           The URL of the repository containing the Dockerfile (default: None)
  --manifest MANIFEST   The Bakerman manifest containing the package and container versions. (default: bakerman.manifest)
  --template TEMPLATE   The Dockerfile template to render. (default: Dockerfile.template)
  --workdir WORKDIR     The local workdir in which the repository is cloned (default: /var/tmp/bakerman)
  --dockerfile DOCKERFILE
                        The path of the docker build file which --template will render into. (default: Dockerfile)
```

## Example config files

### Dockerfile template file

```
FROM            alpine:{{ alpine_version }}
MAINTAINER      Jelle Smet
RUN             apk update
RUN             apk add postfix={{ postfix_version }} rsyslog shadow incron
RUN             groupadd -g 2222 vmail && \
                usermod -u 2222 vmail && \
                groupmod -g 2222 vmail;
COPY            config/rsyslog /etc
COPY            config/startup.sh /startup.sh
COPY            config/postfix/ /etc/postfix/
EXPOSE          25
CMD             /startup.sh
```

### manifest file

The manifest file provides Bakerman the variables to lookup and what type they
are.  Currently Bakerman only supports lookups on *Docker hub* and *Alpine*
packages. Once a newer version is detected it's stored in this manifest.  The
manifest is then used to render the `--template` file.

```
[
  {
    "type": "docker_hub",
    "values": [
      {
        "current_value": "3.10.3",
        "locked": false,
        "name": "alpine",
        "template_arg_name": "alpine_version"
      }
    ]
  },
  {
    "type": "alpine_package",
    "values": [
      {
        "current_value": "3.4.7-r0",
        "locked": false,
        "name": "postfix",
        "template_arg_name": "postfix_version"
      }
    ]
  }
]
```
