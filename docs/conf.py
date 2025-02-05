# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

import os
import sys

from recommonmark.transform import AutoStructify

sys.path.insert(0, os.path.abspath(".."))

master_doc = 'index'


project = 'macrodensity'
copyright = '2023, Walsh Materials Design Group'
author = 'Keith T. Butler, Liam Harnett-Caulfield, Calysta Tesiman'

# The full version, including alpha/beta/rc tags
release = '0.0.0'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = [
    'nbsphinx',
    'sphinx.ext.autodoc',
    'sphinx.ext.intersphinx',
    'sphinx.ext.mathjax',  # to show equations in html output
    'sphinx.ext.githubpages',
    'sphinx.ext.doctest',
    'sphinx_autodoc_annotation',
    'myst_nb',  # for jupyter notebooks
]


templates_path = ['_templates']
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store', '**.ipynb_checkpoints', 'notebooks']

source_suffix = {
    '.rst': 'restructuredtext',
    '.ipynb': 'myst-nb',
}

myst_enable_extensions = [
    "html_admonition",
    "amsmath",
    "dollarmath", # to recognize latex $$ syntax
]

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
html_theme = 'sphinx_book_theme' #'furo'
html_title = "MacroDensity"

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ['_static']


# If true, SmartyPants will be used to convert quotes and dashes to
# typographically correct entities.
html_use_smartypants = True

html_theme_options = {
    "repository_url": "https://github.com/WMD-group/MacroDensity",
    "repository_branch": "master",
    "path_to_docs": "docs",
    "use_repository_button": True,
    "home_page_in_toc": True,
}
# Adding “Edit Source” links on your Sphinx theme
html_context = {
    "display_github": True, # Integrate GitHub
    "github_user": "WMD-group", # Username
    "github_repo": "MacroDensity", # Repo name
    "github_version": "master", # Version
    "conf_py_path": "/docs/", # Path in the checkout to the docs root
}

# -- Options for autodoc -----------------------------------------------------
autoclass_content="both"

# -- Options for nb extension -----------------------------------------------
nb_execution_mode = "off"
nb_render_image_options = {"height": "300",}  # Reduce plots size
#myst_render_markdown_format = "gfm"
myst_heading_anchors = 2
github_doc_root = 'https://github.com/executablebooks/MyST-Parser/tree/master/docs/'
def setup(app):
    app.add_config_value('myst_parser_config', {
            'url_resolver': lambda url: github_doc_root + url,
            'auto_toc_tree_section': 'Contents',
            }, True)
    app.add_transform(AutoStructify)
