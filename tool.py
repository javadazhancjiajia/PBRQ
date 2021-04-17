import pandas as pd


# 读取数据
def get_test_data(keys_path, data_path, num):
    keys = []
    data = []

    with open(keys_path, 'r') as file:
        for line in file:
            keys.append(line.strip('\n'))

    df = pd.read_csv(data_path)
    head_list = df.columns.values.tolist()
    for idx, row in df.iterrows():
        if idx == num:
            break
        temp = []
        for title in head_list:
            temp.append(row[title])
        data.append([int(temp[0]), int(temp[1]), temp[2:-1]])
    return keys, data
