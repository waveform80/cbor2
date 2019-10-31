from cbor2 import dumps, loads, CBORTag
from collections import namedtuple

Pair = namedtuple('Pair', 'first second')

class MyType(object):
    def __init__(self, x, y):
        self.x = x
        self.y = y

def default_encoder(encoder, value):
    encoder.encode(CBORTag(3000, [value.first, value.second]))

def tag_hook(decoder, tag):
    if tag.tag != 3000:
        return tag

    return Pair(*tag.value)

s = dumps({Pair(1, 2): 'foo'}, default=default_encoder)
p = loads(s, tag_hook=tag_hook)
