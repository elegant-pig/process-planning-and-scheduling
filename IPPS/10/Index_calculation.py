import pandas as pd
from openpyxl import load_workbook
import numpy as np
# 读取Excel文件
file_path = '../data/data1.xlsx'
# 手动指定引擎
df = pd.read_excel(file_path, engine='openpyxl')
# df = pd.read_excel(file_path)

# 打印数据框的列名以确认列名
print(df.columns)

# 去除列名中的空格（可选）
df.columns = df.columns.str.strip()

# 计算所有工序标准工时之和
total_standard_time = df['标准工时'].sum()

# 员工总数
total_workers = 22  # 假设总共有30名员工，根据实际数据调整

# 计算每个工序需要的人力平衡，并保留一位小数
df['人力平衡'] = ((df['标准工时'] / total_standard_time) * total_workers).round(2)

# 计算机器需求数量
machine_demand = df.groupby('机器')['人力平衡'].sum().reset_index()
machine_demand.columns = ['机器', '需求数量']  # 重命名列

# 四舍五入需求数量为整数
machine_demand['需求数量'] = machine_demand['需求数量'].round().astype(int)

# 对机器的需求数量进行四舍五入并确保每个机器的数量不为零
machine_demand['需求数量'] = np.ceil(machine_demand['需求数量']).astype(int)

# 确保每个机器的数量都不为零
machine_demand['需求数量'] = machine_demand['需求数量'].replace(0, 1)

# 计算总需求数量和员工数
total_demand = machine_demand['需求数量'].sum()


# 如果总需求数量小于员工数，调整需求数量
if total_demand < total_workers:
    additional_needed = total_workers - total_demand
    for i in range(additional_needed):
        # 按顺序为机器增加需求
        machine_demand.loc[i % len(machine_demand), '需求数量'] += 1

# 输出机器需求数量以进行确认
print("机器需求数量：")
print(machine_demand)
# 计算总的机器数量
total_machines = machine_demand['需求数量'].sum()
print(total_machines)
# 输出结果以确认添加成功
print(df[['工序', '标准工时', '人力平衡']])

# 将更新后的数据写入原始Excel文件的同一个工作表
with pd.ExcelWriter(file_path, engine='openpyxl') as writer:
    df.to_excel(writer, index=False, sheet_name='Sheet1')
    machine_demand.to_excel(writer, index=False, sheet_name='Sheet2')
print("人力平衡数据已成功写入原始文件。")
