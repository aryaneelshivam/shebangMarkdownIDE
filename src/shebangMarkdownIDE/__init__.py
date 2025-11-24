# src/shebangMarkdownIDE/ __init__.py

"""
Shebang Markdown - Terminal-based Markdown IDE powered by Textual by Aryaneel Shivam.
"""

__all__ = ["run_app", "__version__"]

__version__ = "0.1.1"

from .app import run_app  # re-export for convenience

