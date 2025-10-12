"""
Legacy setup.py for backward compatibility.
Modern installation should use: pip install -e .
Or with uv: uv pip install -e .
"""
from setuptools import setup

# This setup.py exists for backward compatibility
# The modern approach uses pyproject.toml with uv
setup()
