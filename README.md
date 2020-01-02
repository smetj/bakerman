# Bakerman

A tool to automatically regenerate and commit configuration files to contain
the latest artifact version values.

## Introduction

Bakerman is a tool to lookup the latest version of artifacts and use the
results to render new config files if said version have changed. Bakerman has
a plugin system to lookup version info of said artifacts such as base Docker
containers and Alpine packages.

If a file is regenerated, bakerman commits and pushes the changes to your
repository, ideally triggering a rebuild of the project resulting into always
up-to-date builds using clear, explicit version definitions.

Currently there's support for looking up the latest container from docker hub
and the latest version of a alpine packages. Bakerman's plugin system allows
adding additional lookup systems.

## Flow

This is a high level logic:

    # Clone or update `--repo` into `--workdir`.
    # Read the manifest file `manifest` and retrieve the latest versions of
      the defined variables.
    # Render `--template` using the version found in step 2 and write the
      outcome to the `--result_dir` directory.
    # Commit the changes defining which values have been updated.
    # Push commits to the remote repository.

## Usage

```
$ bakerman --help
usage: bakerman [-h] --repo REPO [--manifest MANIFEST] [--template TEMPLATE] [--workdir WORKDIR] [--target TARGET]

Automatically regenerate config files to include the latest artifact versions.

optional arguments:
  -h, --help           show this help message and exit
  --repo REPO          The URL of the repository to update. (default: None)
  --manifest MANIFEST  The Bakerman manifest containing the package and container versions. (default: bakerman.manifest)
  --template TEMPLATE  The template to render. (default: bakerman.template)
  --workdir WORKDIR    The local workdir in which the repository is cloned (default: /var/tmp/bakerman)
  --target TARGET      The path of the target build file which --template will render into. (default: bakerman.target)
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
