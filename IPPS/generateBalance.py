from decimal import getcontext, Decimal

import pandas as pd

import generateOR
import generateOperation
import generateMachine


# file_path = 'data/operation_data.xlsx'
# operation_data = pd.read_excel(file_path, sheet_name='final')
# data=operation_data.copy()
# num_station=23
def generate_balance_codes(data,constraint_code,num_station):
    constraint=[]
    balance_codes=[]
    # tem_data = data[['工序', '标准工时','机器']]
    # data=data[['工序', '标准工时','机器']]
    tem_data=index_calculation(data,num_station)

    total_balance=0 #用于计算总的人力平衡
    # 遍历每个操作编码，查找对应的机器编码
    for entry in constraint_code:
        code, machine = entry.split("->")
        # 提取工序编号 j
        op_num = int(code.split(',')[1])  # 获取操作编码中的工序编号
        # print(op_num)
        # 查找工序编号对应的机器编码

        tem_balance = tem_data[tem_data['工序'] == op_num]['人力平衡'].values[0]

        decimal_part = tem_balance - int(tem_balance)
        if decimal_part <= 0.3:
            tem_balance=int(tem_balance)
        else:
            tem_balance=int(tem_balance) + 1  # 向上取整
        if tem_balance==0:
            tem_balance=1

        # 创建操作编码与机器编码的映射关系
        constraint.append(f"{code}->{machine}->{tem_balance}")
        balance_codes.append(tem_balance)
        # 计算总平衡值
        total_balance += tem_balance
        # print(f"total_balance{total_balance}")
        # print(f"constraint{constraint}")
    if total_balance<num_station:
        print("!!!!!!!!!!!!!!!!wrong")


        # balance_layer.append(f"{code} -> {balance}")
        # balance_codes.append(constraint)
    # print(balance_codes)
    return data,balance_codes,constraint



def index_calculation(data,num_station):
    # 添加一列新数据列并初始化为 None
    data['人力平衡'] = None
    # 计算所有工序的加工时间
    total_standard_time = data['标准工时'].sum().round(2)
    # print(f"总标准工时: {total_standard_time}")

    # 遍历data，填充新列
    for i, row in data.iterrows():
        # 按顺序给新列添加数据
        # 假设我们想用随机值填充新列
        # print(row['标准工时'])
        # print(type(row['标准工时']))
        # print(row['标准工时'].min())  # 打印最小值
        # print(row['标准工时'].max())  # 打印最大值
        # print(row['标准工时'].head())  # 打印前几行数据
        new_value=((row['标准工时'] / total_standard_time) * num_station).round(2)
        # print(f"new_value{new_value}")
        data.loc[i, '人力平衡'] =new_value
    # print(data)
    return data

# final_data,_=generateOR.generateOR(data)
# op_final_data,op_code=generateOperation.generate_operation_codes(final_data)
# data,mchine_codes,constraint=generateMachine.generate_machine_codes(op_code,op_final_data)
# generate_balance_codes(final_data,constraint,num_station)

