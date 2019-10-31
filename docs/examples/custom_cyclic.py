from cbor2 import dumps, loads, shareable_encoder, CBORTag

class MyType(object):
    def __init__(self, parent=None):
        self.parent = parent
        self.children = []
        if parent:
            self.parent.children.append(self)

@shareable_encoder
def default_encoder(encoder, value):
    # The state has to be serialized separately so that the decoder would
    # have a chance to create an empty instance before the shared value
    # references are decoded
    serialized_state = encoder.encode_to_bytes(value.__dict__)
    encoder.encode(CBORTag(3000, serialized_state))

def tag_hook(decoder, tag):
    # Return all other tags as-is
    if tag.tag != 3000:
        return tag

    # Create a raw instance before initializing its state to make it
    # possible for cyclic references to work
    instance = MyType.__new__(MyType)
    decoder.set_shareable(instance)

    # Separately decode the state of the new object and then apply it
    state = decoder.decode_from_bytes(tag.value)
    instance.__dict__.update(state)
    return instance

parent = MyType()
child1 = MyType(parent)
child2 = MyType(parent)
serialized = dumps(parent, default=default_encoder, value_sharing=True)

new_parent = loads(serialized, tag_hook=tag_hook)
assert new_parent.children[0].parent is new_parent
assert new_parent.children[1].parent is new_parent
