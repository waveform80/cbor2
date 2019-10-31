import cbor2

class Point(object):
    def __init__(self, x, y):
        self.x = x
        self.y = y

def default_encoder(encoder, value):
    # Tag number 4000 was chosen arbitrarily
    encoder.encode(cbor2.CBORTag(4000, [value.x, value.y]))

def tag_hook(decoder, tag, shareable_index=None):
    if tag.tag != 4000:
        return tag

    # tag.value is now the [x, y] list we serialized before
    return Point(*tag.value)

s = cbor2.dumps(Point(1, 2), default=default_encoder)
p = cbor2.loads(s, tag_hook=tag_hook)
assert isinstance(p, Point) and p.x == 1 and p.y == 2
