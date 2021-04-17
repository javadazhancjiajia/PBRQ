import random

from Crypto.Cipher import AES
from Crypto import Random
from hashlib import md5

model = AES.MODE_ECB


# 处理加密字符长度满足128位
def pad(data):
    length = (16 - len(data) % 16) % 16
    return data.encode(encoding='utf-8') + ("0"*length).encode(encoding='utf-8')


# 生成n byte的随机的key
def random_key(n):
    return Random.new().read(n)


# 根据seed值生成密钥
def get_key_by_seed(seed):
    random.seed(seed)
    key = bytearray(16)
    for i in range(16):
        key[i] |= random.randint(1, 2**8-1)
    return bytes(key[:16])


# AES加密
def encrypt(content, key):
    aes = AES.new(key, model)
    return aes.encrypt(content)


# AES解密
def decrypt(content, key):
    aes = AES.new(key, model)
    return aes.decrypt(content)


if __name__ == '__main__':
    s = random_key(16)
    print(type(s))