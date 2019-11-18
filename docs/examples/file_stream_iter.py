from cbor2 import CBORDecoder

def decode_stream(fname, *args, **kwargs):
    with open(fname, 'rb') as fp:
        decoder = CBORDecoder(fp, *args, **kwargs)
        while True:
            try:
                yield decoder.decode()
            except EOFError:
                break

for obj in decode_stream('stream.cbor'):
    print(obj)

print('done')

