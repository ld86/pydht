from hashlib import sha1
from random import randint


def entropy(length):
    return ''.join(chr(randint(0, 255)) for _ in xrange(length))


def random_id():
    hash = sha1()
    hash.update(entropy(40))
    return hash.digest()
