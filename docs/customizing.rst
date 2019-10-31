Customizing encoding and decoding
=================================

.. currentmodule:: cbor2

Both the encoder and decoder can be customized to support a wider range of
types.

On the encoder side, this is accomplished by passing a callback as the
*default* argument to :func:`dump`, :func:`dumps`, or to the
:class:`CBOREncoder` constructor. This callback will receive an object that the
encoder could not serialize on its own. The callback should then return a value
that the encoder can serialize on its own, although the return value is allowed
to contain objects that also require the encoder to use the callback, as long
as it won't result in an infinite loop.

On the decoder side, you have two options: *tag_hook* and *object_hook*. The
former is called by the decoder to process any semantic tags that have no
predefined decoders. The latter is called for all newly decoded :class:`dict`
objects, and is mostly useful for implementing a JSON compatible custom type
serialization scheme. Unless your requirements restrict you to JSON compatible
types only, it is recommended to use :attr:`~CBORDecoder.tag_hook` for this
purpose.


Using the CBOR tags for custom types
------------------------------------

The most common way to use :attr:`~CBOREncoder.default` is to call
:meth:`CBOREncoder.encode` to add a custom tag in the data stream, with the
payload as the value:

.. literalinclude:: examples/custom_tags.py
    :lines: 1-10

The corresponding :attr:`~CBORDecoder.tag_hook` would be:

.. literalinclude:: examples/custom_tags.py
    :pyobject: tag_hook

Finally, you can verify that the object is de-serialized correctly:

.. literalinclude:: examples/custom_tags.py
    :lines: 19-


Using dicts to carry custom types
---------------------------------

The same could be done with :attr:`~CBORDecoder.object_hook`, but less
efficiently (with this method the attribute names of the custom object end up
in the encoded stream as part of the encapsulating :class:`dict`):

.. literalinclude:: examples/custom_dicts.py

.. note::

    You should ensure that whichever method you decide to use for
    distinguishing your "specially marked" dicts from arbitrary data dicts,
    won't mistake one for the other.


.. _value_sharing:

Value sharing with custom types
-------------------------------

In order to properly encode and decode cyclic references with custom types,
some special care has to be taken. Suppose you have a custom type as below,
where every child object contains a reference to its parent and the parent
contains a list of children:

.. literalinclude:: examples/custom_cyclic.py
    :lines: 1-8

This would not normally be serializable, as it would lead to an endless loop
(in the worst case) and raise some exception (in the best case). Now, enter
CBOR's extension tags 28 and 29. These tags make it possible to add special
markers into the data stream which can be later referenced and substituted with
the object marked earlier.

To do this, in :attr:`~CBOREncoder.default` hooks used with the encoder you
will need to use the :meth:`shareable_encoder` decorator on your
:attr:`~CBOREncoder.default` hook function. It will automatically add the
object to the shared values registry on the encoder and prevent it from being
serialized twice (instead writing a reference to the data stream):

.. literalinclude:: examples/custom_cyclic.py
    :pyobject: default_encoder

On the decoder side, you will need to initialize an empty instance for shared
value lookup before the object's state (which may contain references to it) is
decoded. This is done with the :meth:`~CBORDecoder.set_shareable` method of the
decoder:

.. literalinclude:: examples/custom_cyclic.py
    :pyobject: tag_hook

You could then verify that the cyclic references have been restored after
deserialization:

.. literalinclude:: examples/custom_cyclic.py
    :lines: 33-


Decoding Tagged items as keys
-----------------------------

Since the CBOR specification allows any type to be used as a key in the mapping
type, the decoder provides a flag that indicates it is expecting an immutable
(and by implication hashable) type. If your custom class cannot be used this
way you can raise an exception if this flag is set:

.. literalinclude:: examples/custom_not_immutable.py
    :pyobject: tag_hook

An example where the data could be used as a dict key:

.. literalinclude:: examples/custom_immutable.py

The :attr:`~CBORDecoder.object_hook` can check for the immutable flag in the
same way.
