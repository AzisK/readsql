import argparse
import ast
import functools
import re
import sys
from pathlib import Path
from typing import Dict, Generator, Iterable, List, Optional, Pattern, Union

# Define types for regex rules
RegexRule = Dict[str, Union[str, int, Pattern[str]]]


def main() -> None:
    args = parse_args()
    if args.string:
        print('\n'.join(read_replace(p) for p in args.path))
    else:
        run_on_files(args.path, args.python_var, dry_run=args.nothing)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        prog='readsql', description='Convert SQL to most human readable format'
    )
    parser.add_argument('path', nargs='+', help='Path to the file to be converted')
    parser.add_argument('-s', '--string', action='store_true', help='Read a string')
    parser.add_argument(
        '-n', '--nothing', action='store_true', help='Dry run (do not modify files)'
    )
    parser.add_argument(
        '-py',
        '--python_var',
        nargs='+',
        default=['query'],
        help='Variables to search in Python files (default: query)',
    )
    return parser.parse_args()


def run_on_files(
    paths: List[str], variables: List[str], dry_run: bool = False
) -> Optional[List[str]]:
    results: List[str] = []
    # Convert string paths to Path objects
    for file_path in collect_files(paths):
        lines = read_file(file_path, variables)
        if lines is None:
            continue

        if not dry_run:
            file_path.write_text(lines, encoding='utf-8')
        else:
            results.append(lines)

        action = 'would be reformatted' if dry_run else 'reformatted'
        print(f'{file_path} {action}:\n{lines}')

    return results if dry_run else None


def collect_files(paths: Iterable[str]) -> Generator[Path, None, None]:
    for p in paths:
        path = Path(p)
        if path.name.startswith('.'):
            continue

        if path.is_dir():
            # Recursive search excluding hidden files/dirs
            # We implement manual recursion to easily skip hidden directories
            for item in path.iterdir():
                if item.name.startswith('.'):
                    continue
                if item.is_dir():
                    yield from collect_files([str(item)])
                elif item.is_file():
                    yield item
        elif path.is_file():
            yield path
        else:
            print(f'Path does not exist: {path}', file=sys.stderr)
            sys.exit(1)


def read_file(path: Union[Path, str], variables: List[str]) -> Optional[str]:
    path_obj = Path(path) if isinstance(path, str) else path

    if path_obj.suffix == '.py':
        return read_python_file(path_obj, variables)
    elif path_obj.suffix == '.sql':
        return read_sql_file(path_obj)
    else:
        print(f'{path_obj} is not an SQL or Python file')
        return None


def read_sql_file(path: Union[Path, str]) -> str:
    path_obj = Path(path) if isinstance(path, str) else path
    content = path_obj.read_text(encoding='utf-8')
    return read_replace(content)


def read_python_file(
    path: Union[Path, str], variables: Optional[List[str]] = None
) -> str:
    path_obj = Path(path) if isinstance(path, str) else path
    variables = variables or ['query']
    content = path_obj.read_text(encoding='utf-8')

    try:
        tree = ast.parse(content)
    except SyntaxError:
        print(f'Syntax error in {path_obj}, skipping Python parsing.')
        return content

    # Find assignments to target variables
    replacements = []

    # Pre-calculate line offests to convert (lineno, col) to absolute index
    lines = content.splitlines(keepends=True)

    def get_offset(lineno: int, col_offset: int) -> int:
        # lineno is 1-based
        if lineno <= 0:
            return 0
        return sum(len(line) for line in lines[: lineno - 1]) + col_offset

    for node in ast.walk(tree):
        if isinstance(node, (ast.Assign, ast.AnnAssign)):
            # Check targets
            targets = []
            if isinstance(node, ast.Assign):
                targets = node.targets
            else:
                targets = [node.target]

            is_target = False
            for t in targets:
                if isinstance(t, ast.Name) and t.id in variables:
                    is_target = True
                    break

            if not is_target:
                continue

            # Check value (Constant string or JoinedStr/f-string)
            value_node = node.value
            if isinstance(value_node, (ast.Constant, ast.JoinedStr)):
                # We need the segments. AST supports end_lineno/end_col_offset in 3.8+
                if (
                    value_node.lineno is None
                    or value_node.col_offset is None
                    or value_node.end_lineno is None
                    or value_node.end_col_offset is None
                ):
                    continue

                start_idx = get_offset(value_node.lineno, value_node.col_offset)
                end_idx = get_offset(value_node.end_lineno, value_node.end_col_offset)

                raw_segment = content[start_idx:end_idx]

                # Regex to extract quote and content from the raw segment
                # This handles f-strings and normal strings, ensuring we only touch the inner content
                # We reuse the logic but applied to the exact segment identified by AST
                match = re.match(
                    r'^(?P<prefix>[uUrR]?f?)(?P<quote>"{3}|"{1}|\'{3}|\'{1})(?P<content>.*)(?P=quote)$',
                    raw_segment,
                    flags=re.DOTALL,
                )

                if match:
                    inner_content = match.group('content')
                    formatted_content = read_replace(inner_content)

                    if formatted_content != inner_content:
                        new_segment = (
                            match.group('prefix')
                            + match.group('quote')
                            + formatted_content
                            + match.group('quote')
                        )
                        replacements.append((start_idx, end_idx, new_segment))

    # Apply replacements in reverse order
    replacements.sort(key=lambda x: x[0], reverse=True)

    for start, end, text in replacements:
        # verify verification, ensure no overlap?
        # Since we sort reverse, simple string slicing works
        content = content[:start] + text + content[end:]

    return content


def read_replace(string: str) -> str:
    # Process regex replacements
    for rule in get_regexes():
        string = apply_rule(string, rule)
    return string


def apply_rule(text: str, rule: RegexRule) -> str:
    regex: Pattern[str] = rule['regex']  # type: ignore
    group: int = int(rule['group'])  # type: ignore
    substitute: str = str(rule['substitute'])

    def replacer(m: 're.Match[str]') -> str:
        # Reconstruct the match preserving surrounding groups, replacing only the target group
        prefix = text[m.start() : m.start(group)]
        suffix = text[m.end(group) : m.end()]
        return prefix + substitute + suffix

    return re.sub(regex, replacer, text)


@functools.lru_cache(maxsize=1)
def get_regexes() -> List[RegexRule]:
    # Use Path to find regexes.txt relative to this file
    regex_file = Path(__file__).parent / 'regexes.txt'
    rules: List[RegexRule] = []

    if not regex_file.exists():
        # Fallback or error?
        print(f'Warning: regex file not found at {regex_file}', file=sys.stderr)
        return []

    with regex_file.open(encoding='utf-8') as f:
        for line in f:
            if line.startswith('#') or not line.strip():
                continue
            parts = line.strip().split('__')
            rules.append(
                {
                    'substitute': parts[0],
                    'regex': re.compile(parts[1], flags=re.IGNORECASE),
                    'group': int(parts[2]),
                }
            )
    return rules


def command_line_file(args: argparse.Namespace) -> Optional[List[str]]:
    """Deprecated internal method kept for compatibility with tests"""
    return run_on_files(args.path, args.python_var, dry_run=args.nothing)


if __name__ == '__main__':
    main()
