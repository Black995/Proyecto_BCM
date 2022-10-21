import Crypto
import binascii
import random
import rsa
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
from Crypto.Hash import SHA256
from Crypto.Signature import PKCS1_PSS

def file_open(file):
    key_file = open(file,'rb')
    key_data = key_file.read()
    key_file.close()
    return key_data

#public_key = '30819f300d06092a864886f70d010101050003818d0030818902818100c7e9c4906fb3ae64496751e139cc15e859dc258cf29a7fd32d1d4c93c7a643cd8ed2878c224f3607b1332665d995fd4a0ea778d1b44af685c9dd7d94583eb25819ff38ef369042087ff6171b8ff7ba9eaf0646609b5149d2ea5da1e107d49c0d9d5f26ebf4c020445d6341698ee8adff8234d702c457c2f85b7c5a7609f37d030203010001'
pubkey =rsa.PublicKey.load_pkcs1(file_open('publickey.key'))
#pkPWC = RSA.importKey(binascii.unhexlify(pkPWC))
#pubPWC = pkPWC.publickey()

strSerial = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890'
flag = False

while (not flag):

    mensaje= ''
    seccion = ''
    while len(mensaje) < 20:
        char = random.choice(strSerial)
        mensaje += char
        seccion += char

        if len(seccion) == 4:
            mensaje += '-'
            seccion = ''
    mensaje = mensaje[:-1]
    
    if ( 1507 <= sum(ord(ch) for ch in mensaje) <= 1607) and (('P' in mensaje or 'p' in mensaje) or ('W' in mensaje or 'W' in mensaje) or ('C' in mensaje or 'c' in mensaje))  :
        flag = True

print()
print (mensaje)


msj_enc = rsa.encrypt(mensaje.encode('ascii'),pubkey)

#print('Llave: ', msj_enc.decode('unicode-escape').encode('ISO-8859-1'))

print()
print()
#msj = msj_enc.decode('unicode-escape').encode('ISO-8859-1')

print(msj_enc)

privPWC = rsa.PrivateKey.load_pkcs1(file_open('privatekeyPWC.key'))

hash_value = rsa.compute_hash(msj_enc,'SHA-512')

signature = rsa.sign(msj_enc,privPWC,'SHA-512')

print()
print()
print(signature)

