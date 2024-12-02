from tqdm import tqdm
from Crypto.Util import number
solver = True
x = {}
for k in range(0, 256):
    if not solver:
        break
    print('k', k)
    for m in range(1, 65535+1):
        z = pow((k<<16) + m, 65537, 797452064996036607633741733398429157877438385639196500619729)
        if z in x:
            print("Nope", (k<<16) + m)
        x[z] = m

d = -1
if not solver:
    print(pow(0x4142,65537, 888505838187809547711833896999795292417866051889833402645939))
    n = 888505838187809547711833896999795292417866051889833402645939
    n = 797452064996036607633741733398429157877438385639196500619729
    p = 1049689677999788387637650154823
    p = 949682225412977198398142321867
    q = n // p
    assert p* q == n

    phi_n = (p-1) * (q-1)
    def gcd_extended(a, b):
        """Extended Euclidean Algorithm to find gcd and coefficients x, y."""
        if a == 0:
            return b, 0, 1
        gcd, x1, y1 = gcd_extended(b % a, a)
        x = y1 - (b // a) * x1
        y = x1
        return gcd, x, y

    def mod_inverse(e, phi_n, p, q):
        """Compute modular multiplicative inverse of e modulo phi_n."""
        gcd, x, _ = gcd_extended(e, phi_n)
        if gcd != 1:
            print(p, q)
            raise ValueError("Modular inverse does not exist")
        return x % phi_n

    d = mod_inverse(65537, phi_n, p, q)
    # while True:
    #     p = number.getPrime(127)
    #     q = number.getPrime(127)
    #     phi_n = (p-1) * (q-1)
    #     d = mod_inverse(65537, phi_n, p, q)
    #     # print(d)

import base64

def rc4(key, data):
    """
    RC4 encryption/decryption.
    :param key: The key as a string.
    :param data: The data to encrypt/decrypt as bytes.
    :return: The encrypted/decrypted data as bytes.
    """
    # Key Scheduling Algorithm (KSA)
    key = [c for c in key]
    S = list(range(256))
    j = 0
    for i in range(256):
        j = (j + S[i] + key[i % len(key)]) % 256
        S[i], S[j] = S[j], S[i]
    
    # Pseudo-Random Generation Algorithm (PRGA)
    i = j = 0
    output = []
    for byte in data:
        i = (i + 1) % 256
        j = (j + S[i]) % 256
        S[i], S[j] = S[j], S[i]
        k = S[(S[i] + S[j]) % 256]
        output.append(byte ^ k)
    
    return bytes(output)

import struct
from Crypto.Cipher import ARC4
rc4_key = bytes([0x60, 0x80, 0xff, 0xf3, 0x50, 0x41, 0x40, 0x60, 0x80, 0x63, 0x41, 0x42, 0x43, 0x62, 0x80, 0x00])

cipher = ARC4.new(rc4_key)


import base64
h = base64.b64decode(open('/tmp/46d1e3a419c8815fb56348786fb35a3d55cb6b808a7f7e2d2b2777544f8bed2e-flag.png.enc', 'rb').read()).hex()
flag = b""
out = b''
for i in (range(0, len(h), 64)):
    if not solver:
        a1 = h[i:i+64]
        print(a1)
        c = int("0x"+a1, 16)
        # print('c', hex(pow(c, d, n)))
        cc = pow(c,d,n)
        # print(hex(cc))
        z = struct.pack("<L", cc)[:2]
        print(hex(cc))
        # z = struct.pack("<L", pow(c,d,n))[2:]
        # print(z)
        out += z
        # print(out)
        # print(rc4(rc4_key, out))
        continue
    else:
        msg = x[int("0x"+(h[i:i+64]), 16)]
        z = struct.pack("<H", msg)
        out += z

ret = rc4(rc4_key, out)
open("flag_out.png", "wb").write(ret)
