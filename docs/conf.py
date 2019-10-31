# coding: utf-8
#!/usr/bin/env python
import pkg_resources


extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.intersphinx'
]

templates_path = ['_templates']
source_suffix = '.rst'
master_doc = 'index'
project = 'cbor2'
author = u'Alex Grönholm'
copyright = u'2016, ' + author

v = pkg_resources.get_distribution(project).parsed_version
version = v.base_version
release = v.public

language = None

exclude_patterns = ['_build']
pygments_style = 'sphinx'
highlight_language = 'python'
todo_include_todos = False

html_theme = 'sphinx_rtd_theme'
html_static_path = ['_static']
htmlhelp_basename = project.replace('-', '') + 'doc'

intersphinx_mapping = {
    'python': ('https://docs.python.org/3', None),
}

# Similar hack to that used in conftest; ensure our view of the module is the
# pure Python module
def py_cbor2():
    import cbor2.types
    import cbor2.encoder
    import cbor2.decoder
    class Module:
        pass
    module = Module()
    for source in (cbor2.types, cbor2.encoder, cbor2.decoder):
        for name in dir(source):
            setattr(module, name, getattr(source, name))
    return module

import sys
sys.modules['cbor2'] = py_cbor2()

# Hack to make wide tables work properly in RTD
# See https://github.com/snide/sphinx_rtd_theme/issues/117 for details
def setup(app):
    app.add_stylesheet('style_override.css')
