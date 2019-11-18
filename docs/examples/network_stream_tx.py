import socket
import cbor2

s = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
s.connect('/tmp/cbor-stream')
f = s.makefile('wb')
enc = cbor2.CBOREncoder(f)
i = 0
while True:
    input('Press enter to send %d' % i)
    enc.encode(i)
    f.flush()  # force the send now
    i += 1
