# Configuration file for the Sphinx documentation builder.
#
# This file only contains a selection of the most common options. For a full
# list see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Path setup --------------------------------------------------------------

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.
#
import os
import sys
sys.path.insert(0, os.path.abspath('../src'))


# -- Project information -----------------------------------------------------

project = 'FOTS-Prover'
copyright = '2022, Alef Keuffer, Alexandre Rodrigues Balde, Bruno Filipe Jardim Machado, Pedro Paulo Costa Pereira'
author = 'Alef Keuffer, Alexandre Rodrigues Balde, Bruno Filipe Jardim Machado, Pedro Paulo Costa Pereira'


# -- General configuration ---------------------------------------------------

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.mathjax',
    # 'sphinx.ext.imgmath',
    'sphinx_autodoc_typehints',
    'sphinx.ext.viewcode',
    'sphinx.ext.doctest',
    # https://sphinx-exec-code.readthedocs.io/en/latest/configuration.html
    'sphinx_execute_code',
    'sphinx.ext.githubpages',
    'sphinx.ext.graphviz',
    'sphinx.ext.todo',
]

exec_code_working_dir = '../src'
exec_code_folders = ['../src']

# Add any paths that contain templates here, relative to this directory.
templates_path = ['_templates']

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']


# -- Options for HTML output -------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
#
# html_theme = 'agogo'
# html_theme = 'sphinx_book_theme'
html_theme = 'python_docs_theme'
html_show_sphinx = False
html_experimental_html5_writer = True
html_theme_options = {
    # 'body_min_width': 0,
    'body_max_width': False,
}


# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ['_static']

latex_engine = 'xelatex'

mathjax3_config = {                  
    "tex": {                        
        "macros": {                 
            "Inv": '{\\operatorname{Inv}}',
            "lift": '{\\operatorname{lift}}',
            "strenghten": '{\\operatorname{strenghten}}',
            }                       
        }                           
    }