Describing binary bitload fields
================================

Each bitload is a sequence of simple python values (numbers, bytestrings,
booleans) in binary format. Each value is associated with a name, data type,
and, in most cases, length of the field in bits.

Let's take a look at a simple example::

    >>> message_format = (
    ...    ('id', 'hex', 128),
    ...    ('count', 'int', 4)
    ... )

This example defines two fields, 'id', and 'count'. The 'id' field is a hex
field and it's 128 bits long. The other field is 4 bits long and it's data type
is an integer.

The following data types are supported:

- 'str': string
- 'bytes': raw bytestring
- 'int': unsigned integer number
- 'hex': hexadecimal representation of a number in string format
- 'bool': boolean value
- 'pad': padding bits

Here are some more examples::

    >>> another_message = (
    ...     ('done', 'bool'),
    ...     (None, 'pad', 2)
    ...     ('note', 'str', 256),
    ... )

.. note::
    The 'bool' data type does not need a length, since it is always 1 bit.

.. note::
    The name of a field with 'pad' data type is ignored. By convention, we use
    ``None`` so it stands out, but you can use names like ``'*** PADDING ***'``
    for a more dramatic effect.

The order in which the fields are added to bitloads is the order in which they
appear in the tuple/iterable.

It is important to understand the limits of your data. There are no checks to
make sure the source data will fit the bitload field, so you may get unexpected
results if you are no careful (e.g., inserting a 10-bit integer into a 4-bit
field will yield the wrong value after deserialization).

About the built-in types
------------------------

The built-in types have conversion functions in the :py:mod:`~btl.utils`
module. The functions use names that follow the ``'{:type}_to_bita'`` and
``'bita_to_{:type}'``' format. The following table gives an overview of
possible input (serializable) and output (deserialized) values:

===========  ================================  ================================
type         inputs                            outputs
===========  ================================  ================================
str          ``bytes``, ``str``/``unicode``    ``str``/``unicode``
-----------  --------------------------------  --------------------------------
bytes        ``bytes``                         ``bytes``
-----------  --------------------------------  --------------------------------
int          ``int`` (unsigned)                ``int`` (unsigned)
-----------  --------------------------------  --------------------------------
hex          ``bytes``, ``str`` (``unicode``)  ``bytes``
             (hex number as a string)          (hex number as a string)
-----------  --------------------------------  --------------------------------
bool         any value                         ``bool``
             (coerced using :py:func:`bool`)
-----------  --------------------------------  --------------------------------
pad          n/a                               n/a
===========  ================================  ================================

.. note::
    All unicode strings are stored as UTF-8.


Dealing with other types of data
--------------------------------

In order to deal with values that aren't directly supported by one of the
standard types, there are two possible strategies we can employ.

One strategy is to adapt the python values. For example,
:py:class:`~datatime.datetime` objects can be represented as unsigned integers.
Floats can also be represented as a product of an integer and negative power of
10, and we can therefore store only the integer and restore the float by
multiplying with the same negative power of 10 after deserializing it. Signed
integers can be represented by scaling them such as 0 represents the smallest
negative value.

Another strategy is to use a custom type. This data type allows one to add
completely new types with relative ease.  The tuple for this data type looks
like this::

    >>> ('myfield', 'user', 24, serializer, deserializer)

.. note::
    The use of ``'user'`` type name is just an example. Any type that is not
    one of the types listed in this section can be used (i.e., any type other
    than 'str', 'bytes', 'int', 'hex', 'bool', and 'pad').

Two additional elements are the ``serializer`` and ``deserializer`` functions.

The ``serializer`` function takes a python value, and is expected to return a
:py:class:`~bitarray.bitarray` instance. The length of the output is not
important as it will be adjusted to the correct length during serialization by
padding with 0 or trimming off surplus bits. Keep in mind, though, that surplus
bits *are* going to be trimmed off, which may not be what you want.

The ``deserializer`` function takes a :py:class:`~bitarray.bitarray` instance,
and is expected to return a python value. There are no restrictions on the
return value.

.. note::
    The bitarray documentation can be found `on GitHub
    <https://github.com/ilanschnell/bitarray/blob/master/README.rst>`_.
