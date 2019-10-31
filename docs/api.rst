API Reference
=============

.. module:: cbor2

The :mod:`cbor2` module implements protocols for serializing and de-serializing
Python objects to/from the `CBOR`_ encoding.


Standard Functions
------------------

The most common method of using the cbor2 library is via the :func:`load`,
:func:`loads`, :func:`dump`, or :func:`dumps` functions, which will be familiar
to anyone who's used the :mod:`pickle` or :mod:`json` modules from the standard
library.

.. autofunction:: dump

.. autofunction:: dumps

.. autofunction:: load

.. autofunction:: loads


Classes
-------

The encoder and decoder classes are available for esoteric use-cases which may
involve overriding specific methods. Note that you do *not* need to use the
classes simply to implement support for new types. See the :doc:`customizing`
chapter for more information.

.. autoclass:: CBOREncoder
    :members:

.. autoclass:: CBORDecoder
    :members:


Additional Types and Functions
------------------------------

.. autofunction:: shareable_encoder

.. autoclass:: CBORTag

.. autoclass:: CBORSimpleValue

.. autodata:: undefined

    The CBOR "undefined" simple value. This is a singleton, like :data:`None`.

.. autoclass:: FrozenDict


Exceptions
----------

All exceptions raised during encoding or decoding descend from the common base
:exc:`CBORError`. In addition, specific exceptions may descend from common
Python exception classes (like :exc:`ValueError`) for convenience.

.. autoexception:: CBORError

.. autoexception:: CBOREncodeError

.. autoexception:: CBOREncodeTypeError

.. autoexception:: CBOREncodeValueError

.. autoexception:: CBORDecodeError

.. autoexception:: CBORDecodeValueError

.. autoexception:: CBORDecodeEOF


Performance
-----------

Recent versions of cbor2 include a C optimized variant which is implicitly
imported on supported versions of Python (CPython 3.5 and above).


.. _CBOR: https://cbor.io/
