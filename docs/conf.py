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
release = '6.0.0'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = ['sphinx.ext.autodoc',
    'sphinx.ext.napoleon',
    'sphinx.ext.viewcode']

templates_path = ['_templates']
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']



# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = 'sphinx_rtd_theme'
html_context = {
    "display_github": True,
    "github_user": "Tomo404",
    "github_repo": "Python-group-project-for-scientific-python",
    "github_version": "main",  # or 'master', based on your repo
    "conf_py_path": "/docs/",  # path from the repo root to this conf.py file
}
html_static_path = ['_static']
master_doc = 'index'
