import Crypto
import binascii
import random
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP



#Conviertiendo llaves

public_key = '30819f300d06092a864886f70d010101050003818d0030818902818100c7e9c4906fb3ae64496751e139cc15e859dc258cf29a7fd32d1d4c93c7a643cd8ed2878c224f3607b1332665d995fd4a0ea778d1b44af685c9dd7d94583eb25819ff38ef369042087ff6171b8ff7ba9eaf0646609b5149d2ea5da1e107d49c0d9d5f26ebf4c020445d6341698ee8adff8234d702c457c2f85b7c5a7609f37d030203010001'



public_key = RSA.importKey(binascii.unhexlify(public_key))

strSerial = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890'
mensaje= ''
i = 0
seccion = ''
while len(mensaje) < 25:
    char = random.choice(strSerial)
    mensaje += char
    seccion += char

    if len(seccion) == 4:
        mensaje += '-'
        seccion = ''
mensaje = mensaje[:-1]
mensaje = mensaje.encode()



cipher = PKCS1_OAEP.new(public_key)

msj_enc = cipher.encrypt(mensaje)

print('Llave: ', msj_enc.decode('unicode-escape').encode('ISO-8859-1'))


