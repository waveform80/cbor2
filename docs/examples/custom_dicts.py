import cbor2

class Point(object):
    def __init__(self, x, y):
        self.x = x
        self.y = y

def default_encoder(encoder, value):
    encoder.encode(dict(typename='Point', x=value.x, y=value.y))

def object_hook(decoder, value):
    if value.get('typename') != 'Point':
        return value

    return Point(value['x'], value['y'])

s = cbor2.dumps(Point(1, 2), default=default_encoder)
p = cbor2.loads(s, object_hook=object_hook)
assert p.x == 1 and p.y == 2
