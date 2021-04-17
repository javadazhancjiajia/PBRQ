# 设置最小单元格为1,加密
from shve.SHVE import SHVE


# 区域节点，也就是树中的非叶子节点
class PNode:
    def __init__(self, p, token, keys, is_elementary_unit=False):
        self.bounders = p
        self.gray_vec = token
        self.bitmap = keys
        self.is_elementary_unit = is_elementary_unit
        self.nodes = []

    def add(self, node, enc):
        if node is not None:
            self.bitmap |= node.bitmap
            self.nodes.append(node)
            node.bitmap = enc.encrypt(node.bitmap)


# 数据类，每个节点表示一个数据，每个叶子节点包含多个数据
class DNode:
    def __init__(self, user, keys):
        self.user_id = user
        self.bitmap = keys


# 复现的PBQ树
class PBQTree2:
    def __init__(self, t, gray, gray_shve, bit_shve):
        self.side_length = t
        self.gray = gray
        self.gray_shve = gray_shve
        self.bit_shve = bit_shve
        self.root = None
        self.count = 0
        self.bitmap_table = None

    # 建树
    def create_tree(self, key_set, data_set):
        # 处理关键字集合
        key_hash = {}
        hash_count = 0
        for key in key_set:
            key_hash[key] = 1 << hash_count
            hash_count += 1

        new_data_set = []
        for data in data_set:
            bitmap = 0
            for key in data[2]:
                bitmap |= key_hash[key]
            new_data_set.append([data[0], data[1], bitmap])

        # 生成一个height·width大小的表格
        bitmap_table = []
        for i in range(self.side_length):
            temp = []
            for j in range(self.side_length):
                p = self.gray_shve.encrypt(self.gray.get_gray_str(i, j))
                temp.append(PNode([p], self.gray_shve.trap_door(self.gray.get_gray_str(i, j)), 0, True))
            bitmap_table.append(temp)
        # 将每个数据存放到对应的表格下面
        for d in new_data_set:
            for index1 in range(self.side_length):
                for index2 in range(self.side_length):
                    if d[1] == self.gray.get_gray_value(index1, index2):
                        bitmap_table[index1][index2].bitmap |= d[2]
                        bitmap_table[index1][index2].nodes.append(DNode(d[0], self.bit_shve.encrypt(d[2])))
                        break
                    break
        self.bitmap_table = bitmap_table
        s2 = self.gray.height_list.__len__()-1
        e2 = self.gray.width_list.__len__()-1
        self.root = self.down_to_up(0, s2, 0, e2, 0, 0)
        self.root.bitmap = self.bit_shve.encrypt(self.root.bitmap)

    # 存储数据
    def down_to_up(self, s1, s2, e1, e2, n, m):
        if s1 >= self.side_length or e1 >= self.side_length:
            return None
        if s2 == s1 and e2 == e1:
            return self.bitmap_table[s1][e1]
        else:
            p1 = self.gray.get_gray_str(s1, e1)
            bn = p1[0:n] + "*" * (self.gray.height - n) + p1[self.gray.height:self.gray.height + m] + "*" * (
                    self.gray.width - m)

            p1 = self.gray_shve.encrypt(p1)
            p2 = self.gray_shve.encrypt(self.gray.get_gray_str(s1, e2))
            p3 = self.gray_shve.encrypt(self.gray.get_gray_str(s2, e1))
            p4 = self.gray_shve.encrypt(self.gray.get_gray_str(s2, e2))

            none_leaf_node = PNode([p1, p2, p3, p4], self.gray_shve.trap_door(bn), 0)
            if s2 - s1 == 1 and e2 - e1 != 1:
                none_leaf_node.add(self.down_to_up(s1, s2, e1, (e1 + e2) // 2, n, m + 1), self.bit_shve)
                none_leaf_node.add(self.down_to_up(s1, s2, (e1 + e2) // 2 + 1, e2, n, m + 1), self.bit_shve)
            elif e2 - e1 == 1 and s2 - s1 != 1:
                none_leaf_node.add(self.down_to_up(s1, (s1 + s2) // 2, e1, e2, n + 1, m), self.bit_shve)
                none_leaf_node.add(self.down_to_up((s1 + s2) // 2 + 1, s2, e1, e2, n + 1, m), self.bit_shve)
            else:
                none_leaf_node.add(self.down_to_up(s1, (s1 + s2) // 2, e1, (e1 + e2) // 2, n + 1, m + 1), self.bit_shve)
                none_leaf_node.add(self.down_to_up(s1, (s1 + s2) // 2, (e1 + e2) // 2 + 1, e2, n + 1, m + 1), self.bit_shve)
                none_leaf_node.add(self.down_to_up((s1 + s2) // 2 + 1, s2, e1, (e1 + e2) // 2, n + 1, m + 1), self.bit_shve)
                none_leaf_node.add(self.down_to_up((s1 + s2) // 2 + 1, s2, (e1 + e2) // 2 + 1, e2, n + 1, m + 1), self.bit_shve)
            return none_leaf_node


# s_data的数据格式为[搜索的区域token, 中心点的gray, 要满足的bitmap]
# 最小单元格为1
def search_PBRQ2(node, s_data, rst):
    if SHVE.search(node.bitmap, s_data[2]):
        flag1 = False

        # 判断点是否在搜索区域
        if SHVE.search(s_data[1], node.gray_vec):
            flag1 = True
        # 判断边界点是否在搜索区域中
        if not flag1:
            for b in node.bounders:
                for tup in s_data[0]:
                    if SHVE.search(b, tup):
                        flag1 = True
                        break
                if flag1:
                    break

        # 满足中心点在被搜索区域或者边界点在搜索区域中则继续向下搜索
        if flag1:
            if node.is_elementary_unit:
                for data in node.nodes:
                    if SHVE.search(data.bitmap, s_data[2]):
                        rst.append(data.user_id)
            else:
                for next_node in node.nodes:
                    search_PBRQ2(next_node, s_data, rst)
