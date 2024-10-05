import pandas as pd
import numpy as np
import os

# 读取Excel文件
file_path = 'dlt_lottery_data.xlsx'
df = pd.read_excel(file_path)

# 移除第一行和第一列
df = df.iloc[1:, 1:]

# 获取列名（即B列到H列的标题）
columns = df.columns[:7]  # 只取前6列（B到G）

# 设置保存路径（修改为你需要的路径）
save_dir = './output_csv_files'
os.makedirs(save_dir, exist_ok=True)  # 创建保存目录，如果不存在的话

# 遍历每一列，从B列到G列
for col_index, col_name in enumerate(columns):
    # 取当前列数据，并逆序（这里加reset_index确保数据顺序不丢失）
    col_data = df[col_name].iloc[::-1].reset_index(drop=True)

    # 打印当前列名和数据量
    print(f"\n处理列 {col_name}，数据量：{len(col_data)}")
    
    # 修改：创建一个空的表格，大小为 35 行，len(col_data) 列
    new_data = np.zeros((35, len(col_data)), dtype=int)
    
    for row_index, value in enumerate(col_data):
        # 将读取的值转换为整数，然后在对应的行上标记为1
        value_index = int(value) - 1  # 因为数组从0开始，且值对应行号
        new_data[value_index, row_index] = 1
    
    # 将生成的矩阵转换为DataFrame
    new_df = pd.DataFrame(new_data)
    
    # 保存为CSV文件，文件名为当前列名，不保存列名
    csv_file_name = f"号码{col_index + 1}.csv"
    csv_file_path = os.path.join(save_dir, csv_file_name)  # 生成保存路径
    new_df.to_csv(csv_file_path, index=False, header=False)  # 不保存索引和列名
    print(f"文件 {csv_file_path} 已保存")

    # 保存为TXT文件，文件名为当前列名，不保存列名
    # txt_file_name = f"号码{col_index + 1}.txt"
    # txt_file_path = os.path.join(save_dir, txt_file_name)  # 生成保存路径
    # new_df.to_csv(txt_file_path, index=False, header=False, sep=',')  # 使用逗号分隔符
    # print(f"文件 {txt_file_path} 已保存")


# 等待用户按任意键退出
print()
input("程序已完成，按任意键退出...")