import socket
import cbor2

s = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
s.bind('/tmp/cbor-stream')
s.listen()
t = s.accept()[0]
f = t.makefile('rb')
decoder = cbor2.CBORDecoder(f)
while True:
    try:
        print('Received %r' % decoder.decode())
    except:
        # Will only happen when the remote end closes
        break
