import pandas as pd
import numpy as np
import os
import time

def process_lottery_data(file_path, save_dir, lottery_type):
    # 读取CSV文件，指定第一行为header
    df = pd.read_csv(file_path, encoding='utf-8-sig', header=0)

    # 打印前几行数据以检查
    print("DataFrame 的前几行:")
    # print(df.head())

    # 获取列名（即第一行，B列到H列的标题）
    columns = df.columns[1:8]
    print("列名（应该是中文标题）:")
    # print(columns)

    # 使用列名作为文件名
    file_names = columns.tolist()
    print("文件名（来自列名）:")
    # print(file_names)

    # 创建保存目录，如果不存在的话
    os.makedirs(save_dir, exist_ok=True)

    # 直接使用数据，不需要移除第一行（因为它已经是列名了）
    df = df.iloc[:, 1:]

    # 遍历每一列
    for col_index, (col_name, file_name) in enumerate(zip(columns, file_names)):
        # 取当前列数据，并逆序（这里加reset_index确保数据顺序不丢失）
        col_data = df[col_name].iloc[::-1].reset_index(drop=True)

        # 打印当前列名和数据量
        print(f"\n处理{lottery_type.upper()}列 {file_name}，数据量：{len(col_data)}")
        
        # 确定表格的行数
        if lottery_type == 'dlt':
            rows = 35 if col_index < 5 else 12
        else:  # ssq
            rows = 33 if col_index < 6 else 16

        # 创建一个空的表格
        new_data = np.zeros((rows, len(col_data)), dtype=int)
        
        for row_index, value in enumerate(col_data):
            # 将读取的值转换为整数，然后在对应的行上标记为1
            try:
                value_index = int(value) - 1  # 因为数组从0开始，且值对应行号
                if value_index < rows:  # 确保索引在有效范围内
                    new_data[value_index, row_index] = 1
            except ValueError:
                print(f"警告: 列 {file_name} 中的值 '{value}' 无法转换为整数，已跳过。")
        
        # 将生成的矩阵转换为DataFrame
        new_df = pd.DataFrame(new_data)
        
        # 保存为CSV文件，使用之前获取的文件名，不保存列名
        csv_file_name = f"{file_name}.csv"
        csv_file_path = os.path.join(save_dir, csv_file_name)  # 生成保存路径
        new_df.to_csv(csv_file_path, index=False, header=False)  # 不保存索引和列名
        print(f"文件 {csv_file_path} 已保存")

# 处理大乐透数据
dlt_file_path = 'dlt_lottery_data.csv'
dlt_save_dir = './output_csv_files/dlt'
process_lottery_data(dlt_file_path, dlt_save_dir, 'dlt')

# 处理双色球数据
ssq_file_path = 'ssq_lottery_data.csv'
ssq_save_dir = './output_csv_files/ssq'
process_lottery_data(ssq_file_path, ssq_save_dir, 'ssq')

print()
# 倒数2秒
for i in range(2, 0, -1):
    print(f"程序将在 {i} 秒后退出...")
    time.sleep(1)