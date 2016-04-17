*****
pybtl
*****

Bitloads, or bit payloads, are compact payloads containing binary
representations of data. It's a generic binary serialization format for Python
objects.

Today, serializing data in text-based formats JSON and XML is quite popular.
These formats are easy to handle, flexible, and don't rquire too much effort to
use. The tradeoff is the size in bytes serialized payload consumes. When
transmitting data over connections with limited bandwidth and/or high bandwidth
cost, a more efficient way of storing data may be needed. This library was
created to serve this need.

In bitloads, the structure and the *size* of each piece of data that goes into
the payload must be known in advance. It does not support complex sturctures
either. The lack the flexibility and convenience of text-based formats, is a
tradeoff for optimizing for size. Bitloads are somewhat similar to structs, but
they allow for even tighter packing of data.

The pybtl uses a declarative syntax for describing conversion of python
objects into bitloads and vice versa, and provides the tools for performing the
conversions. The name of the library has also been shotened to reflect its
purpose. :)

Source code
===========

The source code is available `on GitHub
<https://github.com/Outernet-Project/pybtl>`_

License
=======

pybtl is licensed under BSD license. Please see the ``LICENSE`` file in the
source tree for more information.

Documentation
=============

.. toctree::
    :maxdepth: 1

    introduction
    describing_bitloads
    serializing_and_deserializing
    apidoc
