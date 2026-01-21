# Changelog

All notable changes to this project will be documented in this file.

## [1.0.0] - 2026-01-21

### Changed

- **Migrated from Poetry to uv** for dependency management and builds
  - Converted `pyproject.toml` to PEP 621 format
  - Switched build backend from `poetry.masonry.api` to `hatchling`
  - Replaced `poetry.lock` with `uv.lock`

- **Simplified codebase structure**
  - Merged `readsql/parse_args.py` into `readsql/__main__.py` (single module)
  - Renamed entry point from `command_line()` to `main()`
  - Standardized parameter naming: `file_name` → `path` throughout
  - Replaced `read_all_files_into()` with generator-based `collect_files()`
  - Replaced `format_files()` with simpler `run_on_files()`
  - Replaced `replace()` and `replace_part_of_string()` with `apply_rule()`
  - Renamed `read_regexes()` to `get_regexes()`
  - Removed `write_file()`, `get_message()`, `get_all_files()`, `validate()` helper functions

- **Bumped version** from 0.1.1 to 1.0.0

- **Updated minimum Python version** from 3.6 to 3.8
- **Consolidated linting tools**: Replaced `zimports` with `ruff` for import sorting and updated CI to show diffs on failure.

### Added

- GitHub Actions workflows:
  - `ci.yml` for testing and linting
  - `publish-pypi.yml` for publishing releases
- `AGENTS.md` with development commands and architecture documentation
- `CHANGELOG.md` to track changes

### Removed

- Removed `argparse` from dependencies (it's part of Python stdlib since 2.7)
- Deleted `setup.py` (replaced by PEP 621 metadata in `pyproject.toml`)
- Deleted `readsql/parse_args.py` (merged into `__main__.py`)
- Deleted `poetry.lock` (replaced by `uv.lock`)

### Fixed

- **Fixed SQL string detection in Python files**:
  - Regex now correctly identifies SQL strings wrapped in single quotes (`'''`) and triple double quotes (`"""`).
  - Fixed a bug where replacing content with a different length caused index drift, corrupting the file.
- Updated `tests/check.py` to use current API (`read_sql_file`, `read_python_file` with positional args)
- Updated `tests/test_files.py` to use `path=` instead of `file_name=` keyword argument
