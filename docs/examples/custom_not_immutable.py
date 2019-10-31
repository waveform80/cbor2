from cbor2 import dumps, loads, CBORDecodeError, CBORTag

class MyType(object):
    def __init__(self, x, y):
        self.x = x
        self.y = y

def default_encoder(encoder, value):
    encoder.encode(CBORTag(3000, [value.x, value.y]))

def tag_hook(decoder, tag):
    if tag.tag != 3000:
        return tag

    if decoder.immutable:
        raise CBORDecodeError(
            'MyType cannot be used as a key or set member')

    return MyType(*tag.value)

s = dumps({MyType(1, 2): 'foo'}, default=default_encoder)
# Should raise CBORDecodeError
p = loads(s, tag_hook=tag_hook)
