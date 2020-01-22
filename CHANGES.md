# Changes

## Version 1.2.7

- Fix various bugs related to repo handling

## Version 1.2.6

- Adding debug messages
- Use git commands directly

## Versionn 1.2.5

- Adding debug messages
- Use git commands directly

## Version 1.2.5

- Add `[skip ci]` to end of commit messages in order to prevent commit/job loops

## Version 1.2.4

- Fix bug in --no-repo logic
- Fix bug in setting Author on commit

## Version 1.2.3

- Add support for more granular Alpine package lookups
- Add --no-repo option which prevents any changes on the repo

## Version 1.2.2

- Remove `git pull` assume an existing repo is up to date.

## Version 1.2.1

- Replace all git shell execs with gitpython
- When incrementing the current tag version, increment minor.

## Version 1.2.0

- Fix bug when no tag exists 1.0.0 is generated
- Add `variables` dict to config which maps to the looup function

## Version 1.1.3

- Add support for Gitlab container repository lookups.

## Version 1.1.2

- Add missing dependency

## Version 1.1.1

- Allow Bakerman to when the --workdir contains a valid repo and clone isn't
  required anymore.

## Version 1.1.0

- Make Bakerman more generic by not only focussing on Dockerfiles.
- Use MyPy type hinting

## Version 1.0.0

- Initial commit
