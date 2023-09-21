# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project tries to adhere to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

Historic and pre-release versions aren't necessarily included.

## [Unreleased]

### Added

- This changelog
- Public functions documented in README 
- Dev/test dependencies: ruff
- Enforce linting with isort, black, ruff and static type checking with mypy in CI 
  using GitHub Actions

### Fixed

- Reliability issues when getting data from Club Manager pages with
 `get_private_member_counts()`. See 'Changed'.

- Use of `assert` in production code

### Changed

- BREAKING CHANGE: Simplify package structure.
  
  `import britishcycling-clubs.main` should be replaced with `import 
  britishcycling-clubs`

- Use [Playwright](https://playwright.dev/python/) instead of Selenium when getting 
  data from Club Manager pages with `get_private_member_counts()`.

  This makes deployment easier, as Playwright simplifies browser installation and
  updates, and a separate driver executable is no longer required. README updated to 
  cover this.

- Update dev/test dependencies: black, mypy, pytest, types-requests, 
  types-beautifulsoup4

### Removed

- Trivial test which didn't have any real value 
- Dev dependencies: pylint


## [0.2.5] - 2023-05-30

### Changed

- Minor code, type hinting and docstring improvements

- Update dev dependencies: mypy, pylint, test, types-requests, types-beautifulsoup4

[unreleased]: https://github.com/elliot-100/britishcycling-clubs/compare/v0.2.5...HEAD
[0.2.5]: https://github.com/elliot-100/britishcycling-clubs/compare/v0.2.3...v0.2.5
