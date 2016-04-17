Introduction to bitloads
========================

To illustrate the practical advantages of bitloads, let's consider a simple
message that has two fields:

- 'id', which is an MD5 hexdigest
- 'count', which is a number between 0 and 15

An MD5 hexdigest has 32 hex digits, which translates to 128 bits (4 bits per
digit). Since 'count' can never be larger than 15, we can use 4 bits to
represent it. Our final bitload therefore has 128 + 4 bits, which is 132 bits
in total. To round it to whole bytes, we may add 4 more bits of pading. 
That is 17 bytes in total (or 17 ascii characters) to represent this
information.

In comparison, assuming a JSON representation of a dict that has the 'id' and
'count' keys, and using a string hexdigest and an integer number, we get a
string that typically uses around 440 bits (416 with whitespace stripped
away). ::

    >>> len('{"count":12,"id":"acbd18db4cc2f85cedef654fccc4a4d8"}') * 8
    416

The MD5 hash alone will use twice as many bits as the entire bitload!

When we are dealing with networks with low availability and high bandwidth
cost, transmitting small amounts of data quickly can mean the difference
between successful and unsuccessful transmission.

On the other hands, there are things bitloads are not very good at. In order to
tightly pack the data, the length of each field in the bitload must be known in
advance. This means that it is not possible to include data with arbitrary
length that is not known in advance (it is *technically* possible, but it would
make deserialization more involved).
