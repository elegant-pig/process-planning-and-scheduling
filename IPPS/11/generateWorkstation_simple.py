import math
import random

import pandas as pd
import generateBalance
import generateOperation
import generateMachine

file_path = '../data/operation_data.xlsx'
operation_data = pd.read_excel(file_path, sheet_name='use')
num_stations=23

weight_rules={
    "front": 1,
    "back": 1,
    "side": 0.8,
    "diagonal_front": 0.6,
    "diagonal_back": 0.4
}


def generate_workstation(num_station,constraint):
    left_count = num_station // 2  # 左边的数量
    right_count = num_station - left_count  # 右边的数量

    # 生成左边的编码
    left_side = [f"L{i + 1}" for i in range(left_count)]
    # 生成右边的编码
    right_side = [f"R{i + 1}" for i in range(right_count)]

    # 合并左右两边的工作站编码
    workstation = left_side + right_side
    # print(workstation)
    selected_stations = []
    avialable_stations = workstation.copy()
    total_operations = len(constraint)
    workstation_assignments = {f"L{i + 1}": [] for i in range(left_count)}
    workstation_assignments.update({f"R{i + 1}": [] for i in range(right_count)})
    operation_assignment = {f"{i+1}":[] for i in range(total_operations)}  # 工序分配记录
    workstation_machines={}
    result_operation_allocation=[]
    # print(f"constraint{constraint}")
    # print(f"avialable_stations{avialable_stations}")
    for entry in constraint:
        code, machine, balance = entry.split("->")
        op_num = code.split(',')[1]  # 获取操作编码中的部件编号
        # print("___________________")
        # print(f"op_num{op_num}")
        # part_code = op_num[1:]
        balance=int(balance)
        for i in range(balance):
            if len(avialable_stations) > 0:
                selected_station = random.choice(avialable_stations)
                # print(selected_station)
                # if selected_station not in workstation_machines and not station_assignments[selected_station]:
                workstation_machines[selected_station] = machine
                workstation_assignments[selected_station].append(code)  # 分配工序
                operation_assignment[op_num].append(selected_station)
                # 将选择过的工作站删去
                avialable_stations.remove(selected_station)
                # print(f"avialable_stations{avialable_stations}")
                # print(f"工序{op_num}分配到工作站{selected_station}")
                # constraint.append(f"{code}->{machine}->{balance}->{selected_station}")
                continue
            else:
                avialable_stations = workstation.copy()
                selected_station = random.choice(avialable_stations)
                if  workstation_machines[selected_station] == machine:
                    workstation_assignments[selected_station].append(code)  # 分配工序
                    operation_assignment[op_num].append(selected_station)
                    # print(f"工序{op_num}分配到工作站{selected_station}")
                    # constraint.append(f"{code}->{machine}->{balance}->{selected_station}")
                    continue
                else:
                    while workstation_machines[selected_station] != machine:
                        selected_station = random.choice(avialable_stations)  # 继续随机选择
                        # print(f"重新随机选择的工作站: {selected_station}")
                        # 找到匹配的工作站后分配工序
                    workstation_assignments[selected_station].append(code)  # 分配工序
                    operation_assignment[op_num] = [selected_station]
                    # avialable_stations.remove(selected_station)  # 从可用工作站中删除
                    # constraint.append(f"{code}->{machine}->{balance}->{selected_station}")
                    # print(f"工序{op_num}分配到工作站{selected_station}")
                    continue

        # 取出当前工序分配到的工作站
        tem_workstation_data=operation_assignment[op_num].copy()
        # 将工序分配放入约束中
        # result_operation_allocation.append(f"{code}->{machine}->{balance}->{tem_workstation_data}")
        result_operation_allocation.append(tem_workstation_data)
        # constraint.append(f"{code}->{machine}->{balance}->{selected_station}")
        # print(f"workstation_assignments{workstation_assignments}")
        # print(f"operation_assignment{operation_assignment}")
        # print(f"workstation_machines{workstation_machines}")
        # print(result_operation_allocation)
        # print(workstation_assignments)

    return result_operation_allocation,workstation_assignments

# _,code=generateMachine.generate_machine_codes(generateOperation.generate_operation_codes())
# _,constraint=generateBalance.generate_balance_codes(code)
# generate_workstation(num_stations,constraint)