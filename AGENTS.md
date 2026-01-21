# AGENTS.md

This file provides guidance to AI agents (including Warp, Claude, Cursor, etc.) when working with code in this repository.

## Project Overview

readsql is a CLI tool that converts SQL keywords to uppercase for better readability. It processes both raw SQL files and SQL strings embedded in Python variables.

## Development Commands

```bash
# Install dependencies
uv sync --all-extras

# Run the CLI
uv run readsql "select sushi from tokyo" -s             # Format a string
uv run readsql tests/sql_example.sql                    # Format SQL file
uv run readsql tests/sql_in_python_example.py           # Format SQL in Python (looks for `query` variable)
uv run readsql file.py -py sql query_template           # Custom variable names to search
uv run readsql file1.sql file2.py folder/               # Process multiple files/folders

# Run tests
uv run pytest -v

# Type Check (MyPy)
uv run mypy .

# Pre-commit (uses black with -S flag, ruff)
pre-commit run --all-files
```

## Architecture

Entry point is `readsql/__main__.py:main()`, registered as `readsql` script in pyproject.toml.

The CLI accepts one or multiple files/folders as input. When given a folder, it recursively processes all `.sql` and `.py` files.

### Core Flow
1. `parse_args()` - Handles CLI arguments (`-s` for string mode, `-n` for dry-run, `-py` for custom Python variable names)
2. For strings: `read_replace()` applies regex substitutions directly
3. For files: `read_file()` dispatches to `read_sql_file()` or `read_python_file()` based on extension
4. `read_python_file()` uses `ast` module to safely extract SQL from variable assignments (default: `query`) while preserving formatting, then applies `read_replace()`

### Regex Rules (`readsql/regexes.txt`)
Format: `SUBSTITUTE__REGEX__GROUP` (double underscore delimited)
- `SUBSTITUTE`: The uppercase replacement text
- `REGEX`: Pattern to match (case-insensitive)
- `GROUP`: Capture group index to replace

Example: `SELECT__(?:^|\s|\()(select)(?:\s)__1` matches `select` keyword and replaces with `SELECT`.

To add new SQL keywords, append a line following this format.

### GHA workflows
- CI is at .github/workflows/ci.yml
- Publish to PyPI is at .github/workflows/publish-pypi.yml
