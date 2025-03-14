import random
import string
from decimal import Decimal

import numpy as np
import pandas as pd
import CODE
#工作站/员工/机器的总数

# 参数设置
population_size = 5  # 初始化20个个体
letters = list(string.ascii_uppercase)
# 读取 Excel 数据
file_path = '../data/operation_data.xlsx'
operation_data = pd.read_excel(file_path, sheet_name='use')
machine_data=pd.read_excel(file_path, sheet_name='machine')
staff_data=pd.read_excel(file_path,sheet_name='staff')
# asa=operation_data['机器']
employ_balance = operation_data['人力平衡']
machine_list=operation_data['机器']
num_stations=len(staff_data['员工'])-1
# print(num_stations)
# print(type(num_stations))
difficulty_priority = {'A': 1, 'B': 2, 'C': 3, 'D': 4}
# 定义最大的人力平衡值为 1.1
max_manpower_balance = Decimal(1.1)
preferred_balance = Decimal(1.0)  # 希望优先分配的人力平衡值
min_manpower_balance = Decimal(0.8)

def generate_operation_codes(machines_codes):
    # allocation_result = []
    remaining_operations  = []    # 记录剩余工序
    # remaining_machines  = machines_codes[:]
    tem=operation_data[['工序','机器','人力平衡']]
    # print(tem)
    # 匹配结果字典，用于存储每个机器和分配到的工序及人力平衡
    machine_operation_mapping = {m: {'工序': [], '总人力平衡': Decimal(0)} for m in machines_codes}

    # 1. 处理人力平衡大于等于 1 的工序
    for index, row in tem.iterrows():
        process = row['工序']
        machine_type = row['机器']
        # balance = row['人力平衡']
        balance = Decimal(str(row['人力平衡']))  # 确保转换为 Decimal 类型
        potential_machines = [m for m in machines_codes if m.startswith(machine_type)]
        machine_idx = 0  # 用于遍历 potential_machines
            # 从该机器类型中随机选择一个机器

        while balance > 0 and machine_idx < len(potential_machines):
            selected_machine = potential_machines[machine_idx]
            # print(selected_machine)
            # 当前机器已经分配的人力平衡
            current_balance = machine_operation_mapping[selected_machine]['总人力平衡']

            # 如果机器分配的人力平衡已满（达到1），不再分配，继续下一个机器
            if current_balance >= preferred_balance:
                machine_idx += 1
                continue

            # 如果工序的 balance 大于等于 1，直接按 1 分配
            if balance >= preferred_balance:
                assign_balance = preferred_balance
            else:
                # 工序的balance小于1,放入剩余工序中，后续处理
                remaining_operations.append({'工序': process, '机器': machine_type, '剩余人力平衡': balance})
                break

            # 更新机器的 balance
            machine_operation_mapping[selected_machine]['工序'].append(process)
            machine_operation_mapping[selected_machine]['总人力平衡'] += assign_balance

            # 更新剩余的 manpower_balance
            balance -= assign_balance
            # print(f"工序 {process} 分配 {assign_balance} 到机器 {selected_machine}")

            # 如果该机器达到1的总人力平衡，换下一个机器
            if machine_operation_mapping[selected_machine]['总人力平衡'] >= preferred_balance:
                machine_idx += 1

            # 如果剩余balance小于1，将其加入remaining_operations
            if 0 < balance < preferred_balance:
                remaining_operations.append({'工序': process, '机器': machine_type, '剩余人力平衡': balance})
                break

    # 2.处理剩余工序，即人力平衡小于1的工序
    grouped_operations = {}
    machine_idx2 = 0
    type_count = {}
    remaining_machine=[machine for machine, data in machine_operation_mapping.items() if not data['工序']]
    print(f"未分配机器{remaining_machine}")
    allocation = {machine: [] for machine in remaining_machine}
    print(f"allocation{allocation}")
    balance_status = {machine: Decimal('0') for machine in remaining_machine}
    print(f"balance_status{balance_status}")
    for operation in remaining_operations:
        machine_type = operation['机器']
        balance = operation['剩余人力平衡']

        # 如果机器类型不存在于 grouped_operations 中，则初始化
        if machine_type not in grouped_operations:
            grouped_operations[machine_type] = []

        # 将工序及其人力平衡添加到相应的机器类型列表中
        grouped_operations[machine_type].append((operation['工序'], balance))

    # 计算剩余各类机器的数量
    for machine_count in remaining_machine:
        machine_type_count = machine_count[0]
        # print(machine_type_count)
        # 更新类型计数
        if machine_type_count in type_count:
            type_count[machine_type_count] += 1
        else:
            type_count[machine_type_count] = 1


    for macine_type,tasks in grouped_operations.items():
        if macine_type in type_count:
            tem_array=grouped_operations[macine_type]
            for i in tem_array:
                selected_machine=remaining_machine.startwith()
    # for i in remaining_operations:
    #     print(i)
    # # 分配算法
    # for machine in remaining_machine:
    #     machine_type = machine[0]  # 机器类型
    #     # 获取与机器类型匹配的所有工序
    #     compatible_ops = [op for op in remaining_operations if op['机器'] == machine_type]
    #     print(f"compatible_ops{compatible_ops}")
    #     # 检查是否有可分配的工序
    #     if not compatible_ops:
    #         print(f"机器 {machine} 没有可分配的工序")
    #         continue  # 如果没有可分配工序，跳过该机器
    #
    #     # 尝试分配符合人力平衡要求的工序
    #     for op in compatible_ops:
    #         new_balance = balance_status[machine] + op['剩余人力平衡']
    #         if min_manpower_balance <= new_balance <= max_manpower_balance:
    #             allocation[machine].append(op)
    #             balance_status[machine] = new_balance
    #             remaining_operations.remove(op)  # 移除已分配工序
    #             break
    #
    #     # 如果没有满足人力平衡的工序，分配最接近的工序
    #     if len(allocation[machine]) == 0:
    #     # if machine not in allocation or len(allocation[machine]) == 0:
    #         closest_op = min(compatible_ops,
    #                          key=lambda op: abs(balance_status[machine] + op['剩余人力平衡'] - min_manpower_balance))
    #         allocation[machine].append(closest_op)
    #         balance_status[machine] += closest_op['剩余人力平衡']
    #         remaining_operations.remove(closest_op)  # 移除已分配工序
    #
    # # 输出分配结果
    # for machine, ops in allocation.items():
    #     print(f"机器 {machine} 分配的工序: {ops}, 总人力平衡: {balance_status[machine]}")


    # # 打印未分配完的工序
    # print("\n未分配完的工序:")
    # for rem_op in remaining_operations:
    #     print(f"工序 {rem_op['工序']} 剩余人力平衡: {rem_op['剩余人力平衡']}")
    return remaining_operations,machine_operation_mapping

def sakd(remaining_operations,machine_operation_mapping):
    print(f"remaining_operations{remaining_operations}")
    potential_machines = [machine for machine, data in machine_operation_mapping.items() if not data['工序']]
    # for row in remaining_operations:
    #     process = row['工序']
    #     machine_type = row['机器']
    #     balance = Decimal(str(row['人力平衡']))  # 确保转换为 Decimal 类型
    #     potential_machines = [m for m in potential_machines if m.startswith(machine_type)]
    #     print(f"potential_machines{potential_machines}")


def adjust_remaining_operations(remaining_operations,machine_codes,machine_operation_mapping):
    # 对剩余工序按机器类型分组
    grouped_operations = {}
    type_count={}
    # 找到工序值为空的机器并存入 remaining_machine
    remaining_machine = []
    successful_combination = []  # 存储找到的有效组合
    attempts = 0  # 尝试次数计数器
    max_attempts = 5  # 最大尝试次数
    allocation = {m: [] for m in remaining_machine}


    # 找到工序值为空的机器并存入 remaining_machine
    remaining_machine = [machine for machine, data in machine_operation_mapping.items() if not data['工序']]
    print(f"remaining_machine{remaining_machine}")

    # 遍历 remaining_operations，将工序按机器类型分组
    for operation in remaining_operations:
        machine_type = operation['机器']
        balance = operation['剩余人力平衡']

        # 如果机器类型不存在于 grouped_operations 中，则初始化
        if machine_type not in grouped_operations:
            grouped_operations[machine_type] = []

        # 将工序及其人力平衡添加到相应的机器类型列表中
        grouped_operations[machine_type].append((operation['工序'], balance))
    # print(f"grouped_operations{grouped_operations[A]}")

    # 计算剩余各类机器的数量
    for machine_count in remaining_machine:
        machine_type_count = machine_count[0]
        # print(machine_type_count)
        # 更新类型计数
        if machine_type_count in type_count:
            type_count[machine_type_count] += 1
        else:
            type_count[machine_type_count] = 1
    print(f"type_count{type_count}")

    for macine_type,tasks in grouped_operations.items():
        filter_machine=[machine for machine in remaining_machine if machine.startswith(macine_type)]
        print(f"filter_machine{filter_machine}")
        # 结果存储所有符合条件的组合
        valid_combinations = []
        all_valid_combinations = []  # 存储所有工序组合
        used_combinations = set()  # 用于存储已组合的工序
        if macine_type in type_count:
            tem_array=grouped_operations[macine_type]
            total_machine=type_count[macine_type]
            # 提取 Decimal 值
            decimal_values = [value for _, value in tem_array]
            print(f"tem_array{tem_array}")
            total_balance=sum(decimal_values )
            average_balance=round(total_balance/total_machine,2)

            for i,(op,balance) in tem_array:
                if filter_machine:
                    selected_machine = random.choice(filter_machine)
                    allocation[selected_machine].append(op)
            # 计算人力平衡
            tem_balance = {m: len(allocation[m]) for m in allocation}
            average_balance = np.mean(list(tem_balance.values()))

            # 计算标准差
            std_dev = np.sqrt(
                np.sum((np.array(list(tem_balance.values())) - average_balance) ** 2) / len(tem_balance))

            # 如果标准差大于0.3，则需要重新分配
            if std_dev > 0.3:
                print("需要重新分配工序")
                # 重新分配逻辑（可在此处实现）
            else:
                print("分配满意:", allocation)

            # for op in tem_array:
            #     machine_type = op['machine_type']
            #     available_machines = [m for m in remaining_machine if m.startswith(machine_type)]
            #     print(f"available_machines{available_machines}")
            #     if available_machines:
            #         selected_machine = random.choice(available_machines)
            #         allocation[selected_machine].append(op)
            #         print(f"allocation{allocation}")



    # # 打印最终机器分配情况
    # print("\n最终机器分配情况:")
    # for machine, data in machine_operation_mapping.items():
    #     print(f"机器 {machine}: 工序 {data['工序']}，总人力平衡 {data['总人力平衡']}")


def valid_combination(combination, min_balance, max_balance):
    """
    检查给定组合的人力平衡总和是否在允许的范围内。

    :param combination: 要检查的工序组合
    :param min_balance: 最小人力平衡
    :param max_balance: 最大人力平衡
    :return: 如果总和在范围内返回True，否则返回False
    """
    # 计算组合中所有工序的人力平衡总和
    total_balance = sum(item[1] for item in combination)
    # 检查总和是否在指定范围内
    return min_balance <= total_balance <= max_balance


sdj=generate_operation_codes(CODE.generate_machine_codes(CODE.num_stations))
# first,_=generate_operation_codes(CODE.generate_machine_codes(CODE.num_stations))
# _,second=generate_operation_codes(CODE.generate_machine_codes(CODE.num_stations))
# print(f"first{first}")
# print(f"second{second}")

# dbjjb=adjust_remaining_operations(first, CODE.generate_machine_codes(CODE.num_stations), second)
# sdhsh=sakd(first,second)
# print(dbjjb)
print(sdj)