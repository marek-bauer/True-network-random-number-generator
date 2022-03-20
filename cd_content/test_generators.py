import secrets


def lcg(seed):
    x = seed
    while True:
        x = (2695477 * x + 1) & 0xffffffff
        yield x


def tarus(seed):
    s1 = seed
    s2 = s1 ^ 4291961294
    s3 = s2 ^ 4214937214
    while True:
        s1 = (((s1 & 4294967294) << 12) ^ (((s1 << 13) ^ s1) >> 19)) & 0xffffffff
        s2 = (((s2 & 4294967288) << 4) ^ (((s2 << 2) ^ s2) >> 25)) & 0xffffffff
        s3 = (((s3 & 4294967280) << 17) ^ (((s3 << 3) ^ s3) >> 11)) & 0xffffffff
        yield s1 ^ s2 ^ s3


def crng():
    while True:
        yield int.from_bytes(secrets.token_bytes(4), byteorder='big', signed=False)

