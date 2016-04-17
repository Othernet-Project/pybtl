import pytest
from bitarray import bitarray

from btl import utils as mod


MOD = mod.__name__


@pytest.mark.parametrize('n,b', [
    (12,
     bitarray('00000000'
              '00000000'
              '00000000'
              '00000000'
              '00000000'
              '00000000'
              '00000000'
              '00001100')),
    (1212121212,
     bitarray('00000000'
              '00000000'
              '00000000'
              '00000000'
              '01001000'
              '00111111'
              '10000000'
              '01111100')),
])
def test_int_to_bitarray(n, b):
    assert mod.int_to_bita(n) == b


def test_int_to_bitarray_signed():
    with pytest.raises(ValueError):
        mod.int_to_bita(-1)


@pytest.mark.parametrize('b,n', [
    (bitarray('00000000'
              '00000000'
              '00000000'
              '00000000'
              '00000000'
              '00000000'
              '00000000'
              '00001100'),
     12),
    (bitarray('1100'),
     12),
    (bitarray('00000000'
              '00000000'
              '00000000'
              '00000000'
              '01001000'
              '00111111'
              '10000000'
              '01111100'),
     1212121212),
    (bitarray('00000000'
              '00000000'
              '00000000'
              '00000000'
              '00000000'
              '00000000'
              '01001000'
              '00111111'
              '10000000'
              '01111100'),
     1212121212),
    (bitarray('11101000'
              '00000000'
              '00000000'
              '00000000'
              '00000000'
              '00000000'
              '01001000'
              '00111111'
              '10000000'
              '01111100'),
     1212121212),
])
def test_bita_to_int(b, n):
    assert mod.bita_to_int(b) == n


@pytest.mark.parametrize('h,b', [
    ('0', bitarray('0000')),
    ('1', bitarray('0001')),
    ('2', bitarray('0010')),
    ('3', bitarray('0011')),
    ('4', bitarray('0100')),
    ('5', bitarray('0101')),
    ('6', bitarray('0110')),
    ('7', bitarray('0111')),
    ('8', bitarray('1000')),
    ('9', bitarray('1001')),
    ('a', bitarray('1010')),
    ('b', bitarray('1011')),
    ('c', bitarray('1100')),
    ('d', bitarray('1101')),
    ('e', bitarray('1110')),
    ('f', bitarray('1111')),
    ('12', bitarray('0010')),  # always only considers last digit, so 2
    pytest.mark.xfail(('z', None)),
    pytest.mark.xfail(('12', bitarray('1100'))),
])
def test_hex_digit_to_bita(h, b):
    assert mod.hex_digit_to_bita(h) == b


@pytest.mark.parametrize('h,b', [
    ('f12a',
     bitarray('1111' '0001'
              '0010' '1010')),
    ('d6331',  # odd number of digits
     bitarray('1101' '0110'
              '0011' '0011'
              '0001')),
])
def test_hex_to_bita(h, b):
    assert mod.hex_to_bita(h) == b


@pytest.mark.parametrize('b,h', [
    (bitarray('1111' '0001'
              '0010' '1010'),
     'f12a'),
    (bitarray('1101' '0110'
              '0011' '0011'
              '0001'),
     'd6331'),
])
def test_bita_to_hex(b, h):
    assert mod.bita_to_hex(b) == h


@pytest.mark.parametrize('v,b', [
    (True, bitarray('1')),
    (False, bitarray('0')),
    (1, bitarray('1')),
    (12, bitarray('1')),
    (0, bitarray('0')),
    ('', bitarray('0')),
    (None, bitarray('0')),
])
def test_bool_to_bita(v, b):
    assert mod.bool_to_bita(v) == b


@pytest.mark.parametrize('b,v', [
    (bitarray('0'), False),
    (bitarray('1'), True),
    (bitarray('111'), True),
    (bitarray('000'), False),
    (bitarray('10011'), True),
    (bitarray('10010'), False),
])
def test_bita_to_bool(b, v):
    assert mod.bita_to_bool(b) == v
