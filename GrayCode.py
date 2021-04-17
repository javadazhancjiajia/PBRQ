import numpy as np
import random


# 用于生成数据集，每个数据包括(格雷码，位图)
class DataSet:
    def __init__(self, gray_table):
        self.gray_table = gray_table
        self.height = gray_table.__len__()-1
        self.width = gray_table[0].__len__()-1

    def random_list(self, n, m):
        rst = []
        for i in range(n):
            index_x = random.randint(0, self.height)
            index_y = random.randint(0, self.width)
            tmp = np.random.randint(2, size=m)
            gray_vector = self.gray_table[index_x][index_y]
            bit_vector = 0
            for num in tmp:
                bit_vector = (bit_vector << 1 | num)
            rst.append((gray_vector, bit_vector))
        return rst


# 格雷表
class Gray:
    def __init__(self, height, width):
        """
        :param height: 高度的二进制位数
        :param width: 宽度的二进制位数
        """
        self.height = height
        self.width = width
        self.height_list = self.iteration(height)
        self.width_list = self.iteration(width)

    def get_gray_value(self, x, y):
        return (self.height_list[x] << self.width) | self.width_list[y]

    def get_gray_str(self, x, y):
        return f'{{:0{self.height}b}}'.format(self.height_list[x]) + f'{{:0{self.width}b}}'.format(self.width_list[y])

    @staticmethod
    def gray(iteration_list, n):
        cycle_time = iteration_list.__len__() - 1
        token = 1 << n
        for i in range(cycle_time, -1, -1):
            iteration_list.append(token | iteration_list[i])

    def iteration(self, iteration_time):
        s = [0, 1]
        for i in range(1, iteration_time):
            self.gray(s, i)
        return s

    # 生成格雷码表
    def gray_matrix(self):
        height_list = self.iteration(self.height)
        width_list = self.iteration(self.width)
        self.height_list = height_list
        self.width_list = width_list
        # wb = openpyxl.Workbook()
        # sheet = wb.active
        # sheet.append([0] + width_list)
        gray_table = []
        for i in range(height_list.__len__()):
            row = []
            row2 = [height_list[i]]
            for j in range(width_list.__len__()):
                row.append(height_list[i] << self.width | width_list[j])
                # row2.append(f'{{:0{self.width+self.width}b}}'.format(row[row.__len__()-1]))
            # sheet.append(row2)
            gray_table.append(row)
        # wb.save(f'{self.width}x{self.height}.xlsx')
        return gray_table