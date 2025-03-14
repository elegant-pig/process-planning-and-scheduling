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


def generate_workstation_codes(code):
    constraint=[]
    balance_codes=[]
    op_len=len(code)
    # 定义平衡总和的允许范围
    balance_min, balance_max = 0.9, 1.1
    # print(f"op_len{op_len}")
    # 计算左边和右边的工作站数量
    left_count = num_stations // 2  # 左边的数量
    right_count = num_stations - left_count  # 右边的数量

    # 生成左边的编码
    left_side = [f"L{i + 1}" for i in range(left_count)]
    # 生成右边的编码
    right_side = [f"R{i + 1}" for i in range(right_count)]

    # 合并左右两边的工作站编码
    workstation_codes = left_side + right_side
    print(workstation_codes)
    op_groups = {}
    for entry in code:
        if "->" in entry:
            # parts=entry.split("->")
            code, machine, balance = entry.split("->")
            op_num = code.split(',')[0]  # 获取操作编码中的部件编号
            part_code=op_num[1:]

            # 根据工序编号将数据加入到分组
            if op_num not in op_groups:
                op_groups[op_num] = []  # 初始化新的工序编号组
            op_groups[op_num].append((code, machine, balance))

    # 将字典中的数据转换为多维数组格式
    op_groups_array = list(op_groups.values())

    for part in op_groups_array:
        for item in part:
            # 提取第一个部分，如 'O2,2' 和 'O2,3'
            code = item[0]
            # 按逗号拆分，并获取第二部分，转为整数
            op_number = int(code.split(",")[1])
            print(op_number)  # 输出每个工序的编号

def generate_workstation(num_station):
    left_count = num_stations // 2  # 左边的数量
    right_count = num_stations - left_count  # 右边的数量

    # 生成左边的编码
    left_side = [f"L{i + 1}" for i in range(left_count)]
    # 生成右边的编码
    right_side = [f"R{i + 1}" for i in range(right_count)]

    # 合并左右两边的工作站编码
    workstation = left_side + right_side
    # print(workstation)

    return workstation

def generate_workstation_codes_simple(code):
    # 创建工作站
    left_count = num_stations // 2  # 左边的数量
    right_count = num_stations - left_count  # 右边的数量
    # 生成左边的编码
    left_side = [f"L{i + 1}" for i in range(left_count)]
    # 生成右边的编码
    right_side = [f"R{i + 1}" for i in range(right_count)]
    # 合并左右两边的工作站编码
    workstation = left_side + right_side
    # print(workstation)

    # 分配工序
    # 记录工作站分配情况
    station_assignments = {f"L{i + 1}": [] for i in range(left_count)}
    station_assignments.update({f"R{i + 1}": [] for i in range(right_count)})
    print(f"station_assignments{station_assignments}")
    workstation_machines={}
    # workstation_machines = {f"L{i + 1}": [] for i in range(left_count)}
    # workstation_machines.update({f"R{i + 1}": [] for i in range(right_count)})

    operation_assignment = {}  # 工序分配记录
    total_operations = len(code)
    print(f"code{code}")
    tem_data = operation_data[['工序', '前继工序数量']]
    for entry in code:
        code, machine,balance = entry.split("->")
        op_num = int(code.split(',')[1])  # 获取操作编码中的工序编号
        # 查找工序编号对应的机器编码
        pre_op = tem_data[tem_data['工序'] == op_num]['前继工序数量'].values[0]
        balance=int(balance)

        for b in range(balance):
            print(f"balance{balance}")
            direction = random.choice(["L", "R"])
            if direction=='L':
                total_stations=left_count
                base="L"
            else:
                total_stations = right_count
                base = "R"
            # 选择工作站编号
            selected_station = base+str(calculate_direction(op_num, total_operations, total_stations))
            # print(f"selected_station{selected_station}")
            allocation_operation(selected_station,station_assignments,workstation_machines,machine,op_num)

    # print(station_assignments)
    # print(operation_assignment)

def calculate_direction(num,total_num,count):
    target_station = (num / total_num) * count
    if target_station<1:
        lower_station=1
        upper_station=2
    else:
        lower_station = math.floor(target_station)
        upper_station = math.ceil(target_station)
    select=random.choice([lower_station,upper_station])
    return select



def allocation_operation(selected_station,station_assignments,workstation_machines,machine,op_num):
    if not station_assignments[selected_station]:
        return selected_station
    else:
        nearest_station=find_nearest_workstation(selected_station,workstation_machines,machine)
        if nearest_station:
            return nearest_station
        else:
            next_station = f"{selected_station[0]}{int(selected_station[1:]) + 1}"
            if next_station in workstation_machines:
                allocation_operation(selected_station, station_assignments,workstation_machines,machine)
            else:
                print("分配失败")
    return station_assignments[selected_station]

def find_nearest_workstation(selection_station,workstation,machine):
    side, index = selection_station[0], int(selection_station[1:])
    print(f"side{side}")
    print(f"index{index}")

    candidates = []
    # 定义邻近区域
    neighbors = [
        (f"{side}{index - 1}", weight_rules["front"]),
        (f"{side}{index + 1}", weight_rules["back"]),
        (f"{'R' if side == 'L' else 'L'}{index}", weight_rules["side"]),
        (f"{'R' if side == 'L' else 'L'}{index - 1}", weight_rules["diagonal_front"]),
        (f"{'R' if side == 'L' else 'L'}{index + 1}", weight_rules["diagonal_back"])
    ]

    # 检查每个邻近工作站是否未分配
    for station, weight in neighbors:
        if station in workstation and workstation[station] is None:
            candidates.append((station, weight))

    # 根据权重从高到低排序
    candidates.sort(key=lambda x: -x[1])
    return candidates[0][0] if candidates else None


# def assign_operation():
#     if not station_assignments[selected_station]:
#         workstation_machines[selected_station] = machine
#         station_assignments[selected_station].append(op_num)  # 分配工序
#         operation_assignment[op_num] = selected_station
#         print(station_assignments)
#         print(operation_assignment[op_num])
#         print("#$%^&*()")
#         continue
#
#     elif workstation_machines[selected_station]:
#         if selected_station == lower:
#             selected_station = upper
#         else:
#             selected_station = lower
#         if not station_assignments[selected_station]:
#             workstation_machines[selected_station] = machine
#             station_assignments[selected_station].append(op_num)  # 分配工序
#             operation_assignment[op_num] = selected_station
#             continue
#         elif workstation_machines[selected_station]:
#             if direction == "L":
#                 direction = "R"
#             else:
#                 direction = "L"
#             lower, upper = calculate_direction(op_num, total_operations, total_stations, base)
#             selected_station = random.choice([lower, upper])  # 在上下界随机选择
#
#             if not station_assignments[selected_station]:
#                 workstation_machines[selected_station] = machine
#                 station_assignments[selected_station].append(op_num)  # 分配工序
#                 operation_assignment[op_num] = selected_station
#                 continue
#             elif workstation_machines[selected_station]:
#                 if selected_station == lower:
#                     selected_station = upper
#                 else:
#                     selected_station = lower
#                 if not station_assignments[selected_station]:
#                     workstation_machines[selected_station] = machine
#                     station_assignments[selected_station].append(op_num)  # 分配工序
#                     operation_assignment[op_num] = selected_station
#                     continue
#                 elif workstation_machines[selected_station] == machine:
#                     station_assignments[selected_station].append(op_num)  # 分配工序
#                     operation_assignment[op_num] = selected_station
#                     continue
#                 else:
#                     print("无匹配！！！！！")
#                     break


_,second=generateMachine.generate_machine_codes(generateOperation.generate_operation_codes())
_,code=generateBalance.generate_balance_codes(second)
# print(code)
# print(second)
# generate_workstation_codes(code)
generate_workstation_codes_simple(code)
