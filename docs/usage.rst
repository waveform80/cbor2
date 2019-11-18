Basic usage
===========

.. currentmodule:: cbor2

Serializing and deserializing with cbor2 is pretty straightforward, and works
almost identically to the familiar :mod:`pickle` module::

    >>> import cbor2
    >>> cbor2.dumps(['hello', 'world'])
    b'\x82ehelloeworld'
    >>> cbor2.loads(b'\x82ehelloeworld')
    ['hello', 'world']

The usual :func:`load`, :func:`loads`, :func:`dump`, and :func:`dumps`
functions are all available:

.. literalinclude:: examples/basic_dump_load.py

Some data types, however, require extra considerations, as detailed below.


String/bytes handling on Python 2
---------------------------------

The :class:`str` type is encoded as binary on Python 2. If you want to encode
strings as text on Python 2, use the :class:`unicode` type instead.


Date/time handling
------------------

The CBOR specification does not support naïve datetimes (that is, datetimes
where ``tzinfo`` is missing). When the encoder encounters such a datetime, it
needs to know which timezone it belongs to. To this end, you can specify a
default timezone by passing a :class:`~datetime.tzinfo` instance to the
:func:`dump` or :func:`dumps` functions as the *timezone* argument. Decoded
datetimes are always timezone aware.

By default, datetimes are serialized in a manner that retains their timezone
offsets. You can optimize the data stream size by setting
*datetime_as_timestamp* to :data:`False` when calling the :func:`dump` or
:func:`dumps` functions, but this causes the timezone offset information to be
lost.

In versions prior to 5.0 the encoder would convert a :class:`datetime.date`
object into a :class:`datetime.datetime` prior to writing. This can cause
confusion on decoding so this has been disabled by default in the next version.
The behaviour can be re-enabled as follows:

.. literalinclude:: examples/date_as_datetime.py

A default timezone offset must also be provided.


Cyclic (recursive) data structures
----------------------------------

If the encoder encounters a container object (i.e. list or dict) within itself,
it will by default raise :exc:`CBOREncodeError` indicating that a cyclic
reference has been detected and value sharing was not enabled::

    >>> import cbor2
    >>> lst = []
    >>> lst.append(lst)
    >>> lst
    [[...]]
    >>> cbor2.dumps(lst)
    Traceback (most recent call last):
      File "<stdin>", line 1, in <module>
    _cbor2.CBOREncodeError: cyclic data structure detected but value sharing is disabled

CBOR has, however, an extension specification that allows the encoder to
reference a previously encoded value without processing it again. This makes it
possible to serialize such cyclic references, but value sharing has to be
enabled by setting *value_sharing* to :data:`True` when calling :func:`dump` or
:func:`dumps`::

    >>> cbor2.dumps(lst, value_sharing=True)
    b'\xd8\x1c\x81\xd8\x1d\x00'
    >>> cbor2.loads(b'\xd8\x1c\x81\xd8\x1d\x00')
    [[...]]

.. warning::

    Support for value sharing is rare in other CBOR implementations, so think
    carefully whether you want to enable it. It also causes some line overhead,
    as all potentially shareable values must be tagged as such (even if they
    are not later referenced).


.. _supported_types:

Type support
------------

The standard types supported by `CBOR`_, and their corresponding Python types
are as follows:

+------+---------------+--------------------------------------------------+
| Type | Semantics     | Python type(s)                                   |
+======+===============+==================================================+
| 0    | Positive int  | :class:`int`                                     |
+------+---------------+                                                  |
| 1    | Negative int  |                                                  |
+------+---------------+--------------------------------------------------+
| 2    | Byte-string   | :class:`bytes` (or :class:`str` in Python 2.x)   |
+------+---------------+--------------------------------------------------+
| 3    | UTF-8 string  | :class:`str` (or :class:`unicode` in Python 2.x) |
+------+---------------+--------------------------------------------------+
| 4    | List          | :class:`list` or :class:`tuple`                  |
+------+---------------+--------------------------------------------------+
| 5    | Map           | :class:`dict`                                    |
+------+---------------+--------------------------------------------------+
| 6    | Extensions    | See next section                                 |
+------+---------------+--------------------------------------------------+
| 7    | Floats and    | :class:`float`, :class:`bool`, :data:`None`      |
|      | simple values |                                                  |
+------+---------------+--------------------------------------------------+


Tag support
-----------

In addition to all standard `CBOR`_ tags, this library supports many `extended
tags`_:

+-----+---------------------------+-------------------------------------+
| Tag | Semantics                 | Python type(s)                      |
+=====+===========================+=====================================+
| 0   | Standard date/time string | :class:`datetime.datetime` (or      |
+-----+---------------------------+ :class:`datetime.date` with the     |
| 1   | Epoch-based date/time     | ``date_as_datetime`` parameter)     |
+-----+---------------------------+-------------------------------------+
| 2   | Positive bignum           | :class:`int` (or :class:`long` in   |
+-----+---------------------------+ Python 2.x)                         |
| 3   | Negative bignum           |                                     |
+-----+---------------------------+-------------------------------------+
| 4   | Decimal fraction          | :class:`decimal.Decimal`            |
+-----+---------------------------+                                     |
| 5   | Big-float                 |                                     |
+-----+---------------------------+-------------------------------------+
| 28  | Mark shared value         | n/a                                 |
+-----+---------------------------+                                     |
| 29  | Reference shared value    |                                     |
+-----+---------------------------+-------------------------------------+
| 30  | Rational number           | :class:`fractions.Fraction`         |
+-----+---------------------------+-------------------------------------+
| 35  | Regular expression        | ``_sre.SRE_Pattern`` (result of     |
|     |                           | :func:`re.compile`)                 |
+-----+---------------------------+-------------------------------------+
| 36  | MIME message              | :class:`email.message.Message`      |
+-----+---------------------------+-------------------------------------+
| 37  | Binary UUID               | :class:`uuid.UUID`                  |
+-----+---------------------------+-------------------------------------+
| 258 | Set                       | :class:`set` or :class:`frozenset`  |
+-----+---------------------------+-------------------------------------+
| 260 | Network address           | :class:`ipaddress.IPv4Address` or   |
|     |                           | :class:`ipaddress.IPv6Address`      |
+-----+---------------------------+-------------------------------------+
| 261 | Network prefix            | :class:`ipaddress.IPv4Network` or   |
|     |                           | :class:`ipaddress.IPv6Network`      |
+-----+---------------------------+-------------------------------------+

Arbitary tags can be represented with the :class:`CBORTag` class.

Streaming Applications
----------------------

Some applications require processing an unknown number of concatenated CBOR items
in a file. Originally this was not well supported due to the decoder interpreting an
:exc:`EOFError` as a generic :exc:`CBORDecodeError` with no way to distinguish it from
corrupted data.

It will now distinguish between an :exc:`EOFError` at the first byte of a new object
and a truncation while decoding a container.

Decoding can now be done from a stream as here:

.. literalinclude:: examples/file_stream_load.py

Or as here by re-using a decoder object and providing a generator:

.. literalinclude:: examples/file_stream_iter.py

If you want to avoid handling :exc:`EOFError` entirely and your file object supports
the :meth:`io.BufferedReader.peek` method, you can do the following:

.. literalinclude:: examples/file_stream_peek.py

Some network protocols can allow a socket to provide this kind of interface with the :meth:`socket.socket.makefile` method:

.. literalinclude:: examples/network_stream_tx.py

and the receiving end:

.. literalinclude:: examples/network_stream_rx.py

Use Cases
---------

Here are some things that the cbor2 library could be (and in some cases, is
being) used for:

- Experimenting with network protocols based on CBOR encoding
- Designing new data storage formats
- Submitting binary documents to ElasticSearch without base64 encoding overhead
- Storing and validating file metadata in a secure backup system
- RPC which supports Decimals with low overhead

.. _CBOR: https://tools.ietf.org/html/rfc7049
.. _extended tags: https://www.iana.org/assignments/cbor-tags/cbor-tags.xhtml
