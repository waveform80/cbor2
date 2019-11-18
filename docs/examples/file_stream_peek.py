from cbor2 import load

# This works with version 4.x
with open('stream.cbor', 'rb') as fp:
    while fp.peek(1):
        obj = load(fp)
        print(obj)

print('done')

