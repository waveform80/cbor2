from cbor2 import load

# This works from version 5.0.0
with open('stream.cbor', 'rb') as fp:
    while True:
        try:
            obj = load(fp)
            print(obj)
        except EOFError:
            break

print('done')

