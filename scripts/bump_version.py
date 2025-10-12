#!/usr/bin/env python3
"""
Version management script for powersall.

Usage:
    python scripts/bump_version.py patch    # 2.0.0 -> 2.0.1
    python scripts/bump_version.py minor    # 2.0.0 -> 2.1.0
    python scripts/bump_version.py major    # 2.0.0 -> 3.0.0
    python scripts/bump_version.py 2.1.0    # Set specific version
"""

import argparse
import re
from pathlib import Path


def get_current_version():
    """Get current version from pyproject.toml"""
    pyproject_path = Path(__file__).parent.parent / "pyproject.toml"

    with open(pyproject_path, 'r') as f:
        content = f.read()

    version_match = re.search(r'version = "([^"]+)"', content)
    if version_match:
        return version_match.group(1)

    raise ValueError("Could not find version in pyproject.toml")


def bump_version(current_version, bump_type):
    """Bump version according to semver rules"""
    major, minor, patch = map(int, current_version.split('.'))

    if bump_type == 'major':
        return f"{major + 1}.0.0"
    elif bump_type == 'minor':
        return f"{major}.{minor + 1}.0"
    elif bump_type == 'patch':
        return f"{major}.{minor}.{patch + 1}"
    else:
        raise ValueError(f"Unknown bump type: {bump_type}")


def update_pyproject_version(new_version):
    """Update version in pyproject.toml"""
    pyproject_path = Path(__file__).parent.parent / "pyproject.toml"

    with open(pyproject_path, 'r') as f:
        content = f.read()

    # Replace version in pyproject.toml
    updated_content = re.sub(
        r'version = "[^"]+"',
        f'version = "{new_version}"',
        content
    )

    with open(pyproject_path, 'w') as f:
        f.write(updated_content)

    print(f"Updated version to {new_version} in pyproject.toml")


def update_powersall_version(new_version):
    """Update fallback version in powersall.py"""
    powersall_path = Path(__file__).parent.parent / "powersall" / "powersall.py"

    with open(powersall_path, 'r') as f:
        content = f.read()

    # Replace fallback version
    updated_content = re.sub(
        r'__version__ = "[\d\.]+"',
        f'__version__ = "{new_version}"',
        content
    )

    with open(powersall_path, 'w') as f:
        f.write(updated_content)

    print(f"Updated fallback version to {new_version} in powersall.py")


def main():
    parser = argparse.ArgumentParser(description="Bump version for powersall")
    parser.add_argument(
        'version_type',
        choices=['major', 'minor', 'patch'],
        nargs='?',
        help='Type of version bump (major, minor, patch)'
    )
    parser.add_argument(
        '--set',
        help='Set specific version (e.g., 2.1.0)'
    )

    args = parser.parse_args()

    try:
        current_version = get_current_version()
        print(f"Current version: {current_version}")

        if args.set:
            new_version = args.set
        elif args.version_type:
            new_version = bump_version(current_version, args.version_type)
        else:
            print("No version change specified. Use --help for options.")
            return

        print(f"New version: {new_version}")

        # Update version in files
        update_pyproject_version(new_version)
        update_powersall_version(new_version)

        print(f"\nVersion bumped to {new_version}")
        print("Don't forget to:")
        print(f"  1. Commit these changes: git add . && git commit -m 'Bump version to {new_version}'")
        print(f"  2. Tag the release: git tag v{new_version}")
        print(f"  3. Push changes and tags: git push && git push --tags")

    except Exception as e:
        print(f"Error: {e}")
        exit(1)


if __name__ == "__main__":
    main()
