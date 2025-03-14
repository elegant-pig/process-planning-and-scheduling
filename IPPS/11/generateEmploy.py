import math
import random
import generateWorkstation_simple

import pandas as pd
import generateBalance
import generateOperation
import generateMachine

file_path = '../data/operation_data.xlsx'
stffa_data = pd.read_excel(file_path, sheet_name='staff')
operation_data = pd.read_excel(file_path, sheet_name='use')
employ_data=stffa_data[['员工','A','B','C','D']]
difficulty_data=operation_data[['工序','难易度']]
num_stations=23

difficulty_weight={
    'A':1,
    'B':0.8,
    'C':0.6,
    'D':0.4
}
# 反向创建一个字典，方便根据权重查找对应的难易度字母
weight_to_difficulty = {v: k for k, v in difficulty_weight.items()}
def generateEmploy(workstation_assignments):
    result_employ_allocation = []
    max_difficulties={}
    tem_employ_data=employ_data.copy()
    for workstation,op in workstation_assignments.items():
        diff_coll = []
        # print(op)
        # print(f"workstation: {workstation}")
        for number in op:
            code = number.split(",")[1]
            code=int(code)
            diff = difficulty_data[difficulty_data['工序'] == code]['难易度'].values[0]
            weight=difficulty_weight[diff]
            diff_coll.append(weight)
            # print(diff_coll)
        if diff_coll:
            max_difficulty = max(diff_coll)
            # print(f"max_difficulty{max_difficulty}")
            max_difficulty_letter=weight_to_difficulty[max_difficulty]
            # 将 max_difficulty_letter 添加到 max_difficulties 字典中
            max_difficulties[workstation] = max_difficulty_letter

        employ_data_sorted = tem_employ_data.sort_values(by=max_difficulty_letter, ascending=False)
        top_employ=int(employ_data_sorted.iloc[0]['员工'])
        result_employ_allocation.append(f"{workstation}->{top_employ}")
        # 从 tem_employ_data 中删除该员工
        tem_employ_data = tem_employ_data.drop(tem_employ_data[tem_employ_data['员工'] == top_employ].index)
        # print(f"tem_employ_data{tem_employ_data}")
        # print(f"top_employ{top_employ}")
    # print(result_employ_allocation)
    return result_employ_allocation





# _,code=generateMachine.generate_machine_codes(generateOperation.generate_operation_codes())
# _,constraint=generateBalance.generate_balance_codes(code)
# workstation_codes,_=generateWorkstation_simple.generate_workstation(num_stations,constraint)
# _,workstation_assignments=generateWorkstation_simple.generate_workstation(num_stations,constraint)
# assa=generateEmploy(workstation_assignments)