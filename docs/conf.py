# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

import os
import sys
import sys
from unittest.mock import MagicMock

MOCK_MODULES = ["tkinter", "_tkinter"]
sys.modules.update((mod, MagicMock()) for mod in MOCK_MODULES)
os.environ["SPHINX_BUILD"] = "1"
sys.path.insert(0, os.path.abspath('../')) 
sys.path.insert(0, os.path.abspath('../pandemic'))  # Adjust if needed

project = 'pandemic'
copyright = '2025, Bartha Lilla, Kerényi Kornél, Tolvaj Tamás'
author = 'Bartha Lilla, Kerényi Kornél, Tolvaj Tamás'
release = '2.0.0'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = ['sphinx.ext.autodoc',
    'sphinx.ext.napoleon',
    'sphinx.ext.viewcode']

templates_path = ['_templates']
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']



# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = 'alabaster'
html_static_path = ['_static']
master_doc = 'index'
