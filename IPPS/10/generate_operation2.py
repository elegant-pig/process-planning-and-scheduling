import random
import string
from decimal import Decimal

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

    # 1. 分配工序
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

            # 随机一个值分配
            random_banlance=round(random.uniform(0.9,1.1),1)

            # 如果机器分配的人力平衡已满（达到1），不再分配，继续下一个机器
            if current_balance >= max_manpower_balance:
                machine_idx += 1
                continue

            # 如果工序的 balance 大于等于随机balance
            if balance >= random_banlance:
                assign_balance = random_banlance
            else:
                remaining_operations.append({'工序': process, '机器': machine_type, '剩余人力平衡': balance})
                break

            # 更新机器的 balance
            machine_operation_mapping[selected_machine]['工序'].append(process)
            machine_operation_mapping[selected_machine]['总人力平衡'] += assign_balance

            # 更新剩余的 manpower_balance
            balance -= assign_balance
            # print(f"工序 {process} 分配 {assign_balance} 到机器 {selected_machine}")

            # 如果该机器达到1的总人力平衡，换下一个机器
            if machine_operation_mapping[selected_machine]['总人力平衡'] >= min_manpower_balance:
                machine_idx += 1

            # 如果剩余balance小于1，将其加入remaining_operations
            if 0 < balance < min_manpower_balance:
                remaining_operations.append({'工序': process, '机器': machine_type, '剩余人力平衡': balance})
                break

    # 2.处理剩余工序，即人力平衡小于1的工序
    # adjust_remaining_operations(remaining_operations, machine_operation_mapping)
    for op in remaining_operations:
        process=op['']

    # remaining_operations, machines_codes, machine_operation_mapping
    # # 打印当前机器的分配情况
    # print("\n第一次分配结果：")
    # for machine, data in machine_operation_mapping.items():
    #     print(f"机器 {machine}: 工序 {data['工序']}，总人力平衡 {data['总人力平衡']}")
    #
    # 打印未分配完的工序
    print("\n未分配完的工序:")
    for rem_op in remaining_operations:
        print(f"工序 {rem_op['工序']} 剩余人力平衡: {rem_op['剩余人力平衡']}")
    return




def adjust_remaining_operations(remaining_operations,machine_operation_mapping):
    # 对剩余工序按机器类型分组
    grouped_operations = {}
    remaining_machine=[]
    type_count={}
    # 找到工序值为空的机器并存入 remaining_machine
    remaining_machine = []
    successful_combination = []  # 存储找到的有效组合
    attempts = 0  # 尝试次数计数器
    max_attempts = 5  # 最大尝试次数

    # 找到工序值为空的机器并存入 remaining_machine
    remaining_machine = [machine for machine, data in machine_operation_mapping.items() if not data['工序']]

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
    # print(f"type_count{type_count}")

    for macine_type,tasks in grouped_operations.items():
        combine=[]
        if macine_type in type_count:
            tem_array=grouped_operations[macine_type]
            # print(f"tem_array{tem_array}")
            # print(f"len!!!!!!!!!!{len(tem_array)}")
            tem_balance=0
            for i,balance in range(1,len(tem_array)+1):
                tem_balance+=balance

            # for i in type_count[macine_type]:
            #     combine=





        #     while attempts < max_attempts:  # 当尝试次数未达到最大值时循环
        #         random.shuffle(tem_array)  # 打乱工序顺序以增加随机性
        #         combinations = []  # 存储当前的有效组合
        #         current_combination = []  # 存储正在构建的当前组合
        #         current_balance = Decimal('0')  # 当前组合的人力平衡总和
        #
        #         for item in tem_array:  # 遍历每个工序
        #             current_combination.append(item)  # 将工序添加到当前组合
        #             current_balance += item[1]  # 累加当前组合的人力平衡
        #             # 检查当前组合是否在允许的人力平衡范围内
        #             # 检查当前组合是否在允许的人力平衡范围内
        #             if valid_combination(current_combination, min_manpower_balance, max_manpower_balance):
        #                 # 记录有效组合
        #                 if current_balance <= max_manpower_balance:
        #                     combinations.append(current_combination.copy())
        #                     print(f"当前有效组合: {combinations}")
        #                 else:
        #                     # 超过最大值则尝试拆分组合
        #                     while current_combination and current_balance > max_manpower_balance:
        #                         removed_item = current_combination.pop()  # 移除最后添加的工序
        #                         current_balance -= removed_item[1]  # 更新当前平衡
        #
        #                     # 将剩余的有效组合添加到组合列表
        #                     if current_combination:
        #                         combinations.append(current_combination.copy())
        #                     current_combination = [removed_item]  # 将被移除的工序重新开始新的组合
        #                     current_balance = removed_item[1]  # 重置当前平衡为被移除工序的人力平衡
        #
        #         # 验证组合数量是否等于type_count
        #         if len(combinations) == type_count[machine_type]:
        #             successful_combination = combinations  # 记录成功的组合
        #             break  # 找到有效组合，退出循环
        #         attempts += 1  # 增加尝试次数
        #
        #     # 如果没有找到有效的组合，输出提示信息
        #     if not successful_combination:
        #         print("未能在 5 次尝试内找到有效的组合。")
        #     else:
        #         print(successful_combination)
        #         # print("找到的有效组合：")  # 输出找到的组合
        #         # for idx, combo in enumerate(successful_combination):
        #         #     print(f"组合 {idx + 1}: {combo}")  # 打印每个组合的内容
        # else:
        #     print("该机器已经全部分配完工序了")
            # count = 0  # 或者其他默认值
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
# print(dbjjb)
print(sdj)