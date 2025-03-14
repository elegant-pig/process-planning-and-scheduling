import pandas as pd
import string
import generateOperation

file_path = '../data/operation_data.xlsx'
operation_data = pd.read_excel(file_path, sheet_name='use')

def generate_machine_codes(operation_codes):
    mchine_codes=[]
    constraint=[]
    tem_data=operation_data[['工序','机器']]
    # 遍历每个操作编码，查找对应的机器编码
    for code in operation_codes:
        # 提取工序编号 j
        op_num = int(code.split(',')[1])  # 获取操作编码中的工序编号
        # print(op_num)
        # 查找工序编号对应的机器编码
        machine_code = tem_data[tem_data['工序'] == op_num]['机器'].values[0]

        # 创建操作编码与机器编码的映射关系
        constraint.append(f"{code}->{machine_code}")
        mchine_codes.append(machine_code)
    # print(mchine_codes)
    return mchine_codes,constraint

# generate_machine_codes(generateOperation.generate_operation_codes())


