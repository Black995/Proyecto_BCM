import Crypto
import binascii

from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP


#Conviertiendo llaves
private_key = '3082025b02010002818100c7e9c4906fb3ae64496751e139cc15e859dc258cf29a7fd32d1d4c93c7a643cd8ed2878c224f3607b1332665d995fd4a0ea778d1b44af685c9dd7d94583eb25819ff38ef369042087ff6171b8ff7ba9eaf0646609b5149d2ea5da1e107d49c0d9d5f26ebf4c020445d6341698ee8adff8234d702c457c2f85b7c5a7609f37d03020301000102818049959f77b6d6019c0274d86bb9b5885ed52cb659b236f2540de819f6cf6740cfda015e49539baa7c9c5a02893cd4fbbd95b549408f4784846c706db7fbdf600f6c72a7879a9a1599cd84a8389fe68b4e7eb6f7b0269ff87b54a8dbe1a54d6a09fe72a3f6fe7595d41fb3fb866ae7855053095967ffb81db79ddbac0c5c2754f9024100cd196dd9fa30b6f20a611311faefddb8c3bd79b5aa364f87a325902509f9b70cbc32cdd27ebcfe153c080aed9f915f64719e821ac7cb9141a3c8f3559cda512f024100f986d870e9f629468ad2afbdb96b1e092ef6ee9d7b6cae36205d8e84ce4a49bb19435471cdbf980c1282332df0d3d190193d5d3e66a5e1c37fd03f7d4d7cd46d02404ae94bcf3eeb861697a5e7323d0659647fd1f7df5b8124c134dca66e70db4d79904fba0f750d107caf057d0057b4e033aeb0277322a07eb88bdafccdbb519e2f02407a7e03ca8a4fd93b53f2d16ae596fc0bae0e725cc4b6395f40cc2ca66d4e729b726f6708e6e3e3142a11d865f90f4294e68f053318d8ddd746eb47ff8f06749102404c72eca322eea0e1e996fee011ecf1d1f7e2842bc3bbe07eef8000f31282c3ba76c2f420f9e157d64eb0554c7315183ddbb7b2c15a8e3923150e5bb464705735'



#

private_key = RSA.importKey(binascii.unhexlify(private_key))




msj_enc = b"\x0f7\x9d\xef|\xe1\xb7^\xa6c\x1d\x83\x1a\x00\x95\xa0\xdf\xeb\xfeg\xa5\x7fl\xbc\xfb;M\x87\xd0\xe1\xfd\xb0\x83\x10{\x9d\x143\x9b\xb9\x18\xbe\x98\xb8\xfa\xd8\xccA\x8d\xd6\xc2\xf8\xc3\xf1\x8c\xdeE\xa3\x1c\xf0r\x85\x80\xca\x8e\xf2Vz\x02w]\xb3\x1b\xbb\xf4\xd1\xe9\xf3\xef\xbd\xbf\x07\xe1\xe9p`\x89w5\xb6\xf5\xcd\xf9\xa0\x10\x8a\x91e\xe2\xc8\x9e\x0c\x17\x94\x9e\x0c\x0cm\xfe\xa3\x96\xcaJ\xe8\x00X\x94\xe0d\xd0\x18\x00\xef\xc7\xf1U\xfb\xcd"



cipher = PKCS1_OAEP.new(private_key)

mensaje = cipher.decrypt(msj_enc)

print(mensaje)

