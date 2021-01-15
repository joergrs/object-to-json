import pytest

from objtojson import Serialized, Serializer, SerializeError


class SomeClass(Serialized):
    def __init__(self, someAttribute, other):
        self.someAttribute = someAttribute
        self.other = other


class AnotherClass(Serialized):
    def __init__(self, a, b):
        self.a = a
        self.b = b


def test_serialize_flat():
    a = SomeClass(4, [5, 6])
    a_reloaded = Serializer.FromJson(a.ToJson())
    assert isinstance(a_reloaded, SomeClass)
    assert a.someAttribute == a_reloaded.someAttribute
    assert a.other == a_reloaded.other
    assert a == a_reloaded


def test_serialize_nested():
    a = SomeClass(4, [5, 6])
    b = AnotherClass(a, {'a': a, 'b': AnotherClass(7, 8)})
    b_reloaded = Serializer.FromJson(b.ToJson())
    assert isinstance(b_reloaded, AnotherClass)
    assert b_reloaded.a == a == b.a
    assert b_reloaded.b == b.b
    assert b_reloaded.b['a'] == a == b.a
    assert b_reloaded.b['b'].a == 7
    assert b_reloaded.b['b'].b == 8
    assert b_reloaded.b['b'] == AnotherClass(7, 8)


def test_collection_types():
    a = SomeClass(['a', {'x': 34, 'b': AnotherClass(3, 4)}], (1, 2, 3))
    a_reloaded = Serializer.FromJson(a.ToJson())
    assert a == a_reloaded
    assert isinstance(a.other, tuple)
    assert isinstance(a_reloaded.other, list)


def test_bad_collection_types():
    a = SomeClass({AnotherClass(3, 4): 7}, 'x')
    with pytest.raises(SerializeError) as excinfo:
        Serializer.FromJson(a.ToJson())
    assert 'Only strings' in str(excinfo.value)

    a = SomeClass({7: 4}, 'x')
    with pytest.raises(SerializeError) as excinfo:
        Serializer.FromJson(a.ToJson())
    assert 'Only strings' in str(excinfo.value)


def test_example():
    a = SomeClass(4, [AnotherClass(['a', 'list'], {'mykey': 34}), 'somestring'])
    print(a.ToJson())


def test_None():
    a = SomeClass(None, [None, {'x': None}])
    a_reloaded = Serializer.FromJson(a.ToJson())
    assert isinstance(a_reloaded, SomeClass)
    assert a.someAttribute == a_reloaded.someAttribute
    assert a.other == a_reloaded.other
    assert a == a_reloaded
