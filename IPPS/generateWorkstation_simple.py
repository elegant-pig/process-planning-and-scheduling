import math
import random

import pandas as pd
import generateBalance
import generateOR
import generateOperation
import generateMachine
import openpyxl


from check_code import  check_generateWorkstation

# 会出现一个位置分配同一个工作站！！！！
# 有无必要！！！！

file_path = 'data/operation_data.xlsx'
operation_data = pd.read_excel(file_path, sheet_name='final')
data=operation_data.copy()
num_station=23

weight_rules={
    "front": 1,
    "back": 1,
    "side": 0.8,
    "diagonal_front": 0.6,
    "diagonal_back": 0.4
}


def generate_workstation(num_station):
    left_count = num_station // 2  # 左边的数量
    right_count = num_station - left_count  # 右边的数量

    # 生成左边的编码
    left_side = [f"L{i + 1}" for i in range(left_count)]
    # 生成右边的编码
    right_side = [f"R{i + 1}" for i in range(right_count)]
    workstation = left_side + right_side
    return workstation

def assignment_operation(data,constraint,num_stations):
    """

    返回：
    -data(dataform):表格数据
    -workstation_codes(list):工序编码
    -workstation_assignments：工作站分配工序信息
    -result_constraint：总约束
    """
    workstation=generate_workstation(num_stations)
    # 合并左右两边的工作站编码
    left_count = num_stations // 2  # 左边的数量
    right_count = num_stations - left_count  # 右边的数量

    while True:
        avialable_stations = workstation.copy()
        workstation_assignments = {f"L{i + 1}": [] for i in range(left_count)}
        workstation_assignments.update({f"R{i + 1}": [] for i in range(right_count)})
        # operation_assignment = {f"{i+1}":[] for i in range(total_operations)}  # 工序分配记录
        operation_assignment={op:[] for op in data['工序']}
        # print(operation_assignment)
        workstation_machines={}
        workstation_codes=[]
        # result_operation_allocation=[]
        result_constraint=[]
        tem_data = data[['工序', '标准工时']]
        # print(f"tem_data: {tem_data}")
        # print(f"constraint{constraint}")
        # print(f"avialable_stations{avialable_stations}")


        for entry in constraint:
            code, machine, balance = entry.split("->")
            op_num = int(code.split(',')[1])  # 获取操作编码中的工序
            process_time = tem_data[tem_data['工序'] == op_num]['标准工时'].values[0]
            balance=int(balance)
            # print(f"balance{balance}")
            # 按照人力平衡进行分配
            for i in range(balance):
                # 如果还有可用工作站（即该完全未分配过工序的工作站）
                if len(avialable_stations) > 0:
                    # 随机选择一个工作站
                    selected_station = random.choice(avialable_stations)
                    # 将该工序使用的机器分配给该工作站
                    workstation_machines[selected_station] = machine
                    # 记录工作分配哪些工序
                    workstation_assignments[selected_station].append(code)
                    # 记录工序分配到哪些工作站
                    # operation_assignment[op_num].append(selected_station)
                    operation_assignment[op_num].append(selected_station)

                    # 将选择过的工作站删去
                    avialable_stations.remove(selected_station)
                    continue
                else:
                    # 如果没有可用工作站，就重新将可用工作站赋值
                    avialable_stations = workstation.copy()
                    # 随机选择一个工作站
                    selected_station = random.choice(avialable_stations)
                    # 如果选择的工作站的机器与该工序需要的机器相同
                    if  workstation_machines[selected_station] == machine:
                        workstation_assignments[selected_station].append(code)  # 分配工序
                        operation_assignment[op_num].append(selected_station)

                        continue
                    else:
                        # 如果该工序与选择的工作站上所用的机器不一致时，就重新选择
                        while workstation_machines[selected_station] != machine:
                            selected_station = random.choice(avialable_stations)  # 继续随机选择

                        # 直到找到匹配的工作站后分配工序
                        workstation_assignments[selected_station].append(code)  # 分配工序
                        operation_assignment[op_num].append(selected_station)

                        continue

            # 取出当前工序分配到的工作站
            tem_workstation_data=operation_assignment[op_num].copy()

            # 将工序分配放入约束中
            workstation_codes.append(tem_workstation_data)
            # check_workstation(tem_workstation_data,num_stations)
            result_constraint.append(f"{code}->{machine}->{balance}->{tem_workstation_data}->{process_time}")
            # print(workstation_codes)
            # print(f"workstation_assignments{workstation_assignments}")
            # print(f"workstation_machines{workstation_machines}")
        # print(f"121")
        # print(workstation_codes)
        # 检查分配是否符合要求
        value=check_generateWorkstation(workstation_codes,23)
        if value:
            return data,workstation_codes,workstation_assignments,result_constraint,workstation_machines



# final_data,_=generateOR.generateOR(data)
# op_final_data,op_code=generateOperation.generate_operation_codes(final_data)
# data,mchine_codes,constraint=generateMachine.generate_machine_codes(op_code,op_final_data)
# tem_data,balance_codes,constraint= generateBalance.generate_balance_codes(final_data, constraint, num_station)
# workstation=generate_workstation(num_station)
# assignment_operation(tem_data,constraint,num_station)
