import Crypto
import binascii
from Crypto.PublicKey import RSA
import rsa

'''
(pubkey,privkey) = rsa.newkeys(2048)

with open('publickeyPWC.key','wb') as key_file:
    key_file.write(pubkey.save_pkcs1('PEM'))

with open('privatekeyPWC.key','wb') as key_file:
    key_file.write(privkey.save_pkcs1('PEM'))
'''

