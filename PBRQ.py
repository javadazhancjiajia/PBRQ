# 设置最小单元格为1,未加密
import math


# 区域节点，也就是树中的非叶子节点
class PNode:
    def __init__(self, token, keys, is_elementary_unit=False):
        self.modify_vec = token[0]
        self.gray_vec = token[1]
        self.bitmap = keys
        self.is_elementary_unit = is_elementary_unit
        self.nodes = []

    def add(self, node):
        if node is not None:
            self.nodes.append(node)


# 数据类，每个节点表示一个数据，每个叶子节点包含多个数据
class DNode:
    def __init__(self, user, gray, keys):
        self.user_id = user
        self.gray_vec = gray
        self.bitmap = keys


# 复现的PBQ树,未加密
class PBQTree:
    def __init__(self, t, gray):
        self.side_length = t
        self.gray = gray
        self.height = gray.height_list.__len__()
        self.width = gray.width_list.__len__()
        self.height_bit = gray.height
        self.width_bit = gray.width
        self.root = None
        self.count = 0

    # 建树
    def create_tree(self):
        s1, e1 = 0, 0
        s2 = self.height-1
        e2 = self.width-1
        self.root = self.child_tree(s1, s2, e1, e2, self.height_bit, self.width_bit)
        return None

    # 插入数据
    def insert_data(self, key_set, data_set):
        # 处理关键字集合
        key_hash = {}
        hash_count = 0
        for key in key_set:
            key_hash[key] = 1 << hash_count
            hash_count += 1

        # 插入数据，先处理再插入
        for data in data_set:
            bitmap = 0
            for key in data[2]:
                bitmap |= key_hash[key]
            self.save(self.root, [data[0], data[1], bitmap])

    def child_tree(self, s1, s2, e1, e2, n, m):
        gray = self.gray.get_gray_value(s1, e1)

        if s1 >= self.side_length or e1 >= self.side_length:
            return None
        elif s2 == s1 and e2 == e1:
            self.count += 1
            return PNode([0, gray], 0, True)
        else:
            # 生成区域token值
            front_part = 2 ** n - 1
            last_part = 2 ** m - 1
            modify_vec = (front_part << self.width_bit) | last_part

            none_leaf_node = PNode([modify_vec, gray | modify_vec], 0)

            if s2 == s1 and e2 != e1:
                none_leaf_node.add(self.child_tree(s1, s2, e1, (e1 + e2) // 2, n, m-1))
                none_leaf_node.add(self.child_tree(s1, s2, (e1 + e2) // 2 + 1, e2, n, m-1))
            elif e2 == e1 and s2 != s1:
                none_leaf_node.add(self.child_tree(s1, (s1 + s2) // 2, e1, e2, n-1, m))
                none_leaf_node.add(self.child_tree((s1 + s2) // 2 + 1, s2, e1, e2, n-1, m))
            else:
                none_leaf_node.add(self.child_tree(s1, (s1 + s2) // 2, e1, (e1 + e2) // 2, n-1, m-1))
                none_leaf_node.add(self.child_tree(s1, (s1 + s2) // 2, (e1 + e2) // 2 + 1, e2, n-1, m-1))
                none_leaf_node.add(self.child_tree((s1 + s2) // 2 + 1, s2, e1, (e1 + e2) // 2, n-1, m-1))
                none_leaf_node.add(self.child_tree((s1 + s2) // 2 + 1, s2, (e1 + e2) // 2 + 1, e2, n-1, m-1))
            return none_leaf_node

    # 存储数据
    def save(self, node, data):
        if (node.modify_vec | data[1]) == node.gray_vec:
            node.bitmap |= data[2]
            if node.is_elementary_unit:
                node.nodes.append(DNode(data[0], data[1], data[2]))
            else:
                for i in node.nodes:
                    self.save(i, data)


# s_data的数据格式为[搜索的区域token, 要满足的bitmap]
# 最小单元格为1
def search_PBRQ(node, s_data, rst):
    if node.bitmap & s_data[2] == s_data[2]:
        flag1 = False

        # 判断边界点是否在搜索区域中
        for tup in s_data[0]:
            if (node.gray_vec | tup[0]) == (tup[1] | node.modify_vec):
                flag1 = True
                break

        # 满足中心点在被搜索区域或者边界点在搜索区域中则继续向下搜索
        if flag1:
            if node.is_elementary_unit:
                for data in node.nodes:
                    if (s_data[2] & data.bitmap) == s_data[2]:
                        rst.append((data.user_id, data.gray_vec, data.bitmap))
            else:
                for next_node in node.nodes:
                    search_PBRQ(next_node, s_data, rst)
