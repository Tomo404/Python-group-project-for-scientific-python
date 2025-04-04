import os
import sys


sys.path.insert(0, os.path.abspath(".."))

# -- Project information -----------------------------------------------------
project = 'pandemic'
copyright = '2025, Bartha Lilla, Kerényi Kornél, Tolvaj Tamás'
author = 'Bartha Lilla, Kerényi Kornél, Tolvaj Tamás'
release = '0.1.0'

# -- General configuration ---------------------------------------------------
extensions = [
    'sphinx.ext.autodoc',  # Auto-generate documentation from docstrings
    'sphinx.ext.napoleon',  # Support for Google-style and NumPy-style docstrings
    'sphinx.ext.viewcode'   # Add links to highlighted source code
]

templates_path = ['_templates']
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']

# -- Options for HTML output -------------------------------------------------
html_theme = 'alabaster'
html_static_path = ['_static']
