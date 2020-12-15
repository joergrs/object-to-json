from objtojson.serialize import _Serialized, Serializer


class A(_Serialized):
    def __init__(self, integer=3, other=None):
        self.integer = integer
        self.other = other


class B(_Serialized):
    def __init__(self, a, b):
        self.a = a
        self.b = b


def test_serialize_flat():
    a = A(4, [5, 6])
    a_reloaded = Serializer.FromJson(a.ToJson())
    assert isinstance(a_reloaded, A)
    assert a.integer == a_reloaded.integer
    assert a.other == a_reloaded.other
    assert a == a_reloaded


def test_serialize_nested():
    a = A(4, [5, 6])
    b = B(a, {'a': a, 'b': B(7, 8)})
    b_reloaded = Serializer.FromJson(b.ToJson())
    assert isinstance(b_reloaded, B)
    assert b_reloaded.a == a == b.a
    assert b_reloaded.b == b.b
    assert b_reloaded.b['a'] == a == b.a
    assert b_reloaded.b['b'].a == 7
    assert b_reloaded.b['b'].b == 8
    assert b_reloaded.b['b'] == B(7, 8)
