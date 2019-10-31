.. image:: https://travis-ci.com/agronholm/cbor2.svg?branch=master
   :target: https://travis-ci.com/agronholm/cbor2
   :alt: Build Status

.. image:: https://coveralls.io/repos/github/agronholm/cbor2/badge.svg?branch=master
   :target: https://coveralls.io/github/agronholm/cbor2?branch=master
   :alt: Code Coverage

.. image:: https://readthedocs.org/projects/cbor2/badge/?version=latest
   :target: https://cbor2.readthedocs.io/en/latest/?badge=latest
   :alt: Documentation Status

This library provides encoding and decoding for the `Concise Binary Object
Representation`_ (CBOR) (`RFC 7049`_) serialization format from Python. The
CBOR format is not Python specific, and enjoys wide support across many
languages. It is a compact binary format, and is extensible with "semantic
tags", a feature that this implementation takes full advantage of. `Read the
docs`_ to learn more.

The library implemented in pure python with an optional C backend, and is
compatible with versions 2.7 and 3.5 onwards (it may work with earlier
versions, but these are not officially supported).

The optional C backend is only supported on CPython for versions 3.5 onwards
(it is not compatible with Python 2.x). The C module is named ``_cbor2`` and
will be implicitly used when available (in the same manner as ``pickle`` wraps
the ``_pickle`` C module in the Python Standard Library).

On PyPy, cbor2 runs with almost identical performance to the C backend.

.. _Concise Binary Object Representation: https://cbor.io/
.. _RFC 7049: https://tools.ietf.org/html/rfc7049
.. _Read the docs: https://cbor2.readthedocs.io/
