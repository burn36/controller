#! /usr/bin/env python
import sys, os, hashlib

m = hashlib.sha256()
file_name = sys.argv[1]
out_name = sys.argv[2]
if os.path.isdir(out_name):
    out_name = os.path.join(out_name, file_name)
BUF_SIZE = 64 * (1024 ** 2)

with open(file_name, 'rb') as ifp:
    with open(out_name, 'wb') as ofp:
        buf = ifp.read(BUF_SIZE)
        while buf:
            m.update(buf)
            ofp.write(buf)
            buf = ifp.read(BUF_SIZE)
with open(out_name+'.sha', 'wb') as fp:
    fp.write(m.hexdigest())
    # for line in fp:
    #     md5, fn = line.rstrip().split('  ', 1)
    #     if fn == file_name:
    #         assert m.hexdigest() == md5
    #         break
    # else:
    #     print('no hash found for ' + file_name)