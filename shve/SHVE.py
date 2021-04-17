import random

from shve import AES


class SHVE:

    default_flag = "0000000000000000".encode(encoding="utf-8")

    def __init__(self, size):
        self.msk = random.randint(0, 2**16-1)
        self.size = size
        self.bytes_size = 16

    # 生成陷门
    def trap_door(self, vec):
        if len(vec) != self.size:
            return TypeError("wrong")

        D0 = bytearray(self.bytes_size)
        # 记录位置信息的数组，下标表示向量对应的维度，若对应位置是*则置为1
        S = [0]*self.size
        true_key = AES.get_key_by_seed(self.msk)
        for index, bit in enumerate(vec):
            # 通配符只需将记录位置变为1
            if bit == '*':
                S[index] = 1
            else:
                # 将每个位置做aes加密之后得到一个bytes数组
                ast = AES.encrypt(AES.pad(bit+str(index)), true_key)
                # 取前16位做异或操作
                for i in range(len(ast)):
                    D0[i] ^= ast[i]
        # 生成一个对称加密的随机密钥
        k = AES.random_key(self.bytes_size)
        # 加密默认表示值得到密文D1
        D1 = AES.encrypt(SHVE.default_flag, k)
        # 将对称密钥k融入D0中
        for i in range(self.bytes_size):
            D0[i] ^= k[i]
        return S, D0, D1

    # 加密向量
    def encrypt(self, vec):
        true_key = AES.get_key_by_seed(self.msk)
        if len(vec) != self.size:
            return TypeError("wrong")
        C = []
        for index, bit in enumerate(vec):
            C.append(AES.encrypt(AES.pad(bit+str(index)), true_key))
        return C

    # 进行匹配查询
    @staticmethod
    def search(encrypted, gen):
        S = gen[0]
        D0 = gen[1]
        D1 = gen[2]
        for index, i in enumerate(S):
            if i == 0:
                bs = encrypted[index]
                for j in range(len(D0)):
                    D0[j] ^= bs[j]
        value = AES.decrypt(D1, bytes(D0[:16]))
        if value == SHVE.default_flag:
            return True
        else:
            return False