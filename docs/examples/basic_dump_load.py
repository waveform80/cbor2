from cbor2 import dumps, loads, dump, load

# Serialize an object as a bytestring
data = dumps(['hello', 'world'])

# Deserialize a bytestring
obj = loads(data)

# Efficiently deserialize from a file
with open('input.cbor', 'rb') as fp:
    obj = load(fp)

# Efficiently serialize an object to a file
with open('output.cbor', 'wb') as fp:
    dump(obj, fp)
