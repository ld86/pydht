from hashlib import sha1
from random import randint


def entropy(length):
    return ''.join(chr(randint(0, 255)) for _ in xrange(length))


def sha(message):
    hash = sha1()
    hash.update(message)
    return hash.digest()


def random_id():
    return sha(entropy(40))
