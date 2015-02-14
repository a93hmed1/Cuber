import gmpy2
from gmpy2 import mpz
import struct
from binascii import unhexlify


BITLEN = 2048

def icbrt (a1, a2):
    z = gmpy2.iroot(mpz(a1), 3)
    return z[0]

def forge_prefix(s, w, N):
    zd = BITLEN - w
    repas = s
    repa = (repas >> zd)
    cmax = N
    cmin = 0
    s = 0
    while True:

        c = (cmax + cmin + 1) / 2
        a1 = repas + c
        s = icbrt(a1, BITLEN)
        a2 = ((s * s * s) >> zd)
        if a2 == repa:
            break
        if c == cmax or c == cmin:
            print( " *** Error: The value cannot be found ***")
            return 0
        if a2 > repa:
            cmax = c
        else:
            cmin = c


    for d in range(zd / 3, 0, -1):
        mask = ((1 << d) - 1)
        s1 = s & (~mask)
        a2 = ((s1 * s1 * s1) >> zd)
        if a2 == repa:
            return s1
    return s

def long_to_bytes (val, endianness='big'):
    """
    Use :ref:`string formatting` and :func:`~binascii.unhexlify` to
    convert ``val``, a :func:`long`, to a byte :func:`str`.

    :param long val: The value to pack

    :param str endianness: The endianness of the result. ``'big'`` for
      big-endian, ``'little'`` for little-endian.

    If you want byte- and word-ordering to differ, you're on your own.

    Using :ref:`string formatting` lets us use Python's C innards.
    """

    # one (1) hex digit per four (4) bits
    width = val.bit_length()

    # unhexlify wants an even multiple of eight (8) bits, but we don't
    # want more digits than we need (hence the ternary-ish 'or')
    width += 8 - ((width % 8) or 8)

    # format width specifier: four (4) bits per hex digit
    fmt = '%%0%dx' % (width // 4)

    # prepend zero (0) to the width, to zero-pad the output
    s = unhexlify(fmt % val)

    if endianness == 'little':
        # see http://stackoverflow.com/a/931095/309233
        s = s[::-1]

    return s

def createsig():
    # modulus of of amazon certificate
    modulus = 0xBE744991DB098BB0B2CC3B2FF4AF8DAF935BDFA4CC4E1A2DE13ADDBABDCB77EDAC53956EC5751C1FB794E318B909697BA0368175A7E4FA6D08D158566E307CCE18A4A9998E7BACA6AEF5D3EDB05D47BA3E844914A8F1CFB2B08134C47A5E4A9EDB0D74E367526F81A9844EE7A9E7267BBA839847CB2CDDA6433B4FA6FA1E2972B979CBEE556B001210B789465AFD18090FA1D8DCF8A09D74AF4203F73338B7FD9BADC60FB34499731ED73FFA54402314E21380E5788CD443DAF2ED2069E73B8A31CE8B5F9305B90E1D39E5B38B304D767456B0C2BD0FD4FA2C9DC11EF249C8235B83759EF527804C6CF6BF24BBA6FF255B
    # PKCS#1 v1.5 fixed prefix
    prefix = 0x0001FFFFFFFFFFFFFFFF000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000

    #load the hash from created file
    f = open("hash.abc", "rb")
    block = f.read(32)
    hash = struct.unpack('>4Q', block)
    hash0 = int(hash[0])<<192
    hash1 = int(hash[1])<<128
    hash2 = int(hash[2])<<64
    hash3 = int(hash[3])
    hash5 = hash0 + hash1 + hash2 + hash3
    # get hash to right position
    hash = hash5 << 1704

    #create forged prefix
    prefix = forge_prefix(prefix+hash, 86*8, modulus)

    # write signature to file
    pref = int(prefix)
    file = open("signature.abc","wb")
    file.write(long_to_bytes(pref, "big"))

createsig()