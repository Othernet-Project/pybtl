Serializing and deserializing
=============================

The conversion of python values into a bitload is called 'serializing', and the
opposite operation is called 'deserializing'. In both cases, we need to supply
the message format description (see :doc:`describing_bitloads`). During
serialization, data is supplied as a Python dict. After deserialization, the
data comes out as a Python dict (technically a
:py:class:`~collections.OrderedDict` instance). The keys in the dict will
correspond to field names in the bitload description.

In the examples in this section we will use a description tuple that looks like
this::

    >>> message_format = (
    ...    ('id', 'hex', 128),
    ...    ('count', 'int', 4),
    ...    (None, 'pad', 4),
    ... )

For both serializing and deserializing, a :py:class:`btl.bitload.Bitload` class
is used. The :py:obj:`~btl.bitload.Bitload` objects are instantiated with the
description tuple::

    >>> from btl import Bitload
    >>> b = Bitload(message_format)

For serializing and deserializing, we can now call methods on this object.

Serializing
-----------

Let's create the source values. ::

    >>> data = {
    ...    'id': 'acbd18db4cc2f85cedef654fccc4a4d8',
    ...    'count': 12,
    ... }

To serialize this dict, we will use the serialize function::

    >>> b.serialize(data)
    '\xab\xcd\x18\xdbL\xc2\xf8\\\xed\xefeO\xcc\xc4\xa4\xd8\xc0'

A shortcut for one-off serialization is the :py:func:`~btl.bitload.serailize`
function::

    >>> from btl import serialize
    >>> serialize(message_format, data)
    '\xab\xcd\x18\xdbL\xc2\xf8\\\xed\xefeO\xcc\xc4\xa4\xd8\xc0'

.. note::
    In the input dict, keys that do not appear in the bitload description will
    simply be ignored. Keys that do appear in the description, but do not
    appear in the input dict with result in a :py:exc:`KeyError` exception.

Deserializing
-------------

Deserializing is equally simple as serializing::

    >>> bitload = '\xab\xcd\x18\xdbL\xc2\xf8\\\xed\xefeO\xcc\xc4\xa4\xd8\xc0'
    >>> b.deserialize(bitload)
    OrderedDict([('id', 'abcd18db4cc2f85cedef654fccc4a4d8'), ('count', 12)])

We can see that the return value is an :py:class:`~collections.OrderedDict`
object. This is so that the order of the key is predictable, and in line with
the bitload description. Unlike the plain dict, you can always depend on the
order of the keys.

A shortcut for one-off deserialization is the
:py:func:`~btl.bitload.deserialize` function::

    >>> from btl import deserialize
    >>> deserialize(message_format, bitload)
    OrderedDict([('id', 'abcd18db4cc2f85cedef654fccc4a4d8'), ('count', 12)])
