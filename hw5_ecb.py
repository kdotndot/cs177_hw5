import pyaes
import os


LOGO1 = 'logo_1.bmp'


#Parsing logos
data = ""
with open(LOGO1, "rb") as f:
    data = f.read()
bytes1 = []
for x in data:
    bytes1.append(x)

#Keeping header
header1 = bytes1[0:122]
for x in range(0, len(header1)):
    header1[x] = hex(header1[x])[2:]

def pad_and_sep(bytes):
    length = len(bytes)
    for i in range(0, length, 16): 
        if length - i < 16:
            temp = bytes[i:i + 16]
            pad = 16 - len(temp)
            for x in range(0, pad):
                temp.append(pad)
            yield temp
        else:
            yield (bytes[i:i + 16])
    
    

padded = list(pad_and_sep(bytes1))

#Encrypting

key = os.urandom(16)
aes = pyaes.AES(key)

encrypted = []
for x in padded:
    print(x)
    temp = aes.encrypt(x)
    for y in temp:
        encrypted.append(hex(y)[2:])

encrypted[0:122] = header1

print(encrypted)
for x in range(0,len(encrypted)):
    if len(encrypted[x]) == 1:
        encrypted[x] = "0" + encrypted[x]
    encrypted[x] = bytes.fromhex(encrypted[x])

LOGO1ENCRYPT = open("logo1_encrypted_ECB.bmp", "wb")
for x in encrypted:
    LOGO1ENCRYPT.write(x) 





