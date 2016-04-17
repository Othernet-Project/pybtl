import pytest

from btl import bitload as mod
from btl import utils


MOD = mod.__name__


def test_init_creates_layout():
    serializer = lambda x: x
    deserializer = lambda x: x
    msgfmt = (
        ('id', 'int', 16),
        ('done', 'bool'),
        ('user', 'str', 20 * 8),
        (None, 'pad', 3),
        ('time', 'user', 12, serializer, deserializer)
    )
    bl = mod.Bitload(msgfmt)
    assert bl.layout['id'].start == 0
    assert bl.layout['id'].end == 16
    assert bl.layout['id'].length == 16
    assert bl.layout['id'].serializer == utils.int_to_bita
    assert bl.layout['id'].deserializer == utils.bita_to_int
    assert bl.layout['done'].start == 16
    assert bl.layout['done'].end == 17
    assert bl.layout['done'].length == 1
    assert bl.layout['done'].serializer == utils.bool_to_bita
    assert bl.layout['done'].deserializer == utils.bita_to_bool
    assert bl.layout['user'].start == 17
    assert bl.layout['user'].end == 177
    assert bl.layout['user'].length == 160
    assert bl.layout['user'].serializer == utils.str_to_bita
    assert bl.layout['user'].deserializer == utils.bita_to_str
    assert bl.layout['time'].start == 180
    assert bl.layout['time'].end == 192
    assert bl.layout['time'].length == 12
    assert bl.layout['time'].serializer == serializer
    assert bl.layout['time'].deserializer == deserializer
    assert bl.length == 192


def test_autopad():
    serializer = lambda x: x
    deserializer = lambda x: x
    msgfmt = (
        ('id', 'int', 16),
        ('done', 'bool'),
        ('user', 'str', 20 * 8),
        ('time', 'user', 12, serializer, deserializer)
    )
    bl = mod.Bitload(msgfmt)
    assert bl.length == 192
    bl = mod.Bitload(msgfmt, autopad=False)
    assert bl.length == 189


def test_serialization():
    msgfmt = (
        ('id', 'hex', 8),
        (None, 'pad', 4),
        ('num', 'int', 4),
    )
    data = {
        'id': 'f4',
        'num': 12,
    }
    b = mod.Bitload(msgfmt)
    assert b.serialize(data) == '\xf4\x0c'


def test_serialization_missing_key():
    msgfmt = (
        ('id', 'hex', 8),
        (None, 'pad', 4),
        ('num', 'int', 4),
    )
    data = {
        'id': 'f4'
    }
    b = mod.Bitload(msgfmt)
    with pytest.raises(KeyError):
        b.serialize(data)


def test_serialization_trims_values():
    msgfmt = (
        ('id', 'hex', 8),
        (None, 'pad', 4),
        ('num', 'int', 4),
    )
    data = {
        'id': 'f0f4',  # this gets trimmed to f4 because of the length limit
        'num': 12,
    }
    b = mod.Bitload(msgfmt)
    assert b.serialize(data) == '\xf4\x0c'


def test_deserialize():
    bitload = '\xf4\x0c'
    msgfmt = (
        ('id', 'hex', 8),
        (None, 'pad', 4),
        ('num', 'int', 4),
    )
    b = mod.Bitload(msgfmt)
    ret = b.deserialize(bitload)
    assert ret['id'] == 'f4'
    assert ret['num'] == 12
    assert list(ret) == ['id', 'num']  # retains the order


def test_deserialize_with_wrong_length_bitload():
    bitload = '\x90'
    msgfmt = (
        ('id', 'hex', 8),
        (None, 'pad', 4),
        ('num', 'int', 4),
    )
    b = mod.Bitload(msgfmt)
    with pytest.raises(ValueError):
        b.deserialize(bitload)
