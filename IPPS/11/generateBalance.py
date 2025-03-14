import pandas as pd
import generateOperation
import generateMachine

file_path = '../data/operation_data.xlsx'
operation_data = pd.read_excel(file_path, sheet_name='use')
num_station=23
def generate_balance_codes(code):
    constraint=[]
    balance_codes=[]
    tem_data = operation_data[['工序', '人力平衡',]]
    balance_data=[] #
    total_balance=0 #用于计算总的人力平衡
    # 遍历每个操作编码，查找对应的机器编码
    for entry in code:
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
        # 计算总平衡值
        total_balance += tem_balance
        # print(f"total_balance{total_balance}")
        # print(f"constraint{constraint}")
    if total_balance<num_station:
        print("!!!!!!!!!!!!!!!!wrong")


        # balance_layer.append(f"{code} -> {balance}")
        # balance_codes.append(constraint)
    return balance_codes,constraint

# _,code=generateMachine.generate_machine_codes(generateOperation.generate_operation_codes())
# generate_balance_codes(code)

