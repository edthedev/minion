# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added

+ Basic `today`, `tomorrow` and `note` functionality via `PowerShell` on Windows.
+ Added alias examples for PowerShell.
+ Cleaned up the root directory - may require updates to your `.bashrc` if you referenced files in the root directly. See the new `profile` directory.

### Planned

+ Change default notes directory to `~/Journal` for compatibilty with [VSCode Journal Plugin][1]

[1]: https://marketplace.visualstudio.com/items?itemName=pajoma.vscode-journal

### Removed

+ Python2 modules deprecated.

### Coming Up

+ Search functionality via Go code is in progress.
+ May deprecate Bash alias commands - depending if we can find a co-maintainer for those.

## [1.9.2] - 2014-12-12

### Added

+ Allows using an alternate config file from the command line.

Useful for having separate aliases that act like separate notebooks.

## [1.8.0] - 2014-08-27

### Added

New and updated commands:

```
dates - now lists results in date order
last - re-opens the last modified file under the notes folder
openall - opens all matches, rather than asking you to sort down to a single match
recent - lists recently modified files under the notes folder
```

Also includes bug fixes for some corner cases. Releases from this one and later should become very stable, thanks to the newly added unit test suite.
Huge thanks to collaborator PavelK for the vision and for major code contributions to this release.

## [1.7.1] - 2014-04-30

### Added 

+ Updates to provide better default behavior on Mac OSX 10.9 Mavericks,
+ Ability to automatically open Google Drive documents with the default web browser, where possible.

For older releases see - https://github.com/edthedev/minion/releases
