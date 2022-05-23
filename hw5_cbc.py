import pyaes
import os


LOGO1 = 'logo_1.bmp'


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
    
def xor_hex(string1, hex2):
    #Input: A string and a list of hex values, without the 0x part
    #Output: List of hex values xor'd
    if len(string1) != len(hex2):
        print("ERROR: INEQUAL LENGTH")
        return
    length = len(string1)
    ans = []
    for x in range(0, length):
        letter1 = ord(string1[x])
        letter2 = int(hex2[x], 16)
        temp = hex(letter1 ^ letter2)[2:]
        if len(temp) < 2:
            temp = "0" + temp
        ans.append(temp)
    return ans   

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



padded = list(pad_and_sep(bytes1))

#Encrypting

key = os.urandom(16)
# For some modes of operation we need a random initialization vector
# of 16 bytes
iv = "InitializationVe"
aes = pyaes.AES(key)

encrypted = []
for x in padded:
    temp = []
    for y in x:
        temp.append(hex(y)[2:])
    temp = xor_hex(iv, temp)
    for y in range(len(temp)):
        temp[y] = int(temp[y], 16)
        
    temp = aes.encrypt(temp)
    for y in temp:
        encrypted.append(hex(y)[2:])

encrypted[0:122] = header1

for x in range(0,len(encrypted)):
    if len(encrypted[x]) == 1:
        encrypted[x] = "0" + encrypted[x]
    encrypted[x] = bytes.fromhex(encrypted[x])

LOGO1ENCRYPT = open("logo1_encrypted_cbc.bmp", "wb")
for x in encrypted:
    LOGO1ENCRYPT.write(x) 