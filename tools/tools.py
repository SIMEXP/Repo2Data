# -*- coding: utf-8 -*-

import os
import hashlib

def dirhash(dirname):
    hash_func = hashlib.sha256

    if not os.path.isdir(dirname):
        raise TypeError('{} is not a directory.'.format(dirname))
    hashvalues = []
    for root, dirs, files in os.walk(dirname, topdown=True):
        hashvalues.extend(
            [
                _filehash(os.path.join(root, f), hash_func) 
                for f in files
            ]
        )
    return _reduce_hash(hashvalues, hash_func)


def _filehash(filepath, hashfunc):
    hasher = hashfunc()
    blocksize = 64 * 1024
    with open(filepath, 'rb') as fp:
        while True:
            data = fp.read(blocksize)
            if not data:
                break
            hasher.update(data)
    return hasher.hexdigest()


def _reduce_hash(hashlist, hashfunc):
    hasher = hashfunc()
    for hashvalue in sorted(hashlist):
        hasher.update(hashvalue.encode('utf-8'))
    return hasher.hexdigest()