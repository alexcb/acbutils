def fnv32a(buf):
    hval = 0x811c9dc5
    fnv_32_prime = 0x01000193
    uint32_max = 2 ** 32
    for s in buf:
        hval = hval ^ ord(s)
        hval = (hval * fnv_32_prime) % uint32_max
    return hval

def get_partition(key, num_partitions):
    x = fnv32a(key)
    assert x >= 0
    return x % num_partitions
