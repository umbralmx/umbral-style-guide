"""umbral-lint — conformance checker for the Umbral design system.

Severities and fix hints come from `rules/rules.json`, never from this package, so a
rule moving from `warning` to `error` changes behaviour without a code change.
"""
from .cli import main

__version__ = "1.1.0"
__all__ = ["main"]
