import string
import time

import numpy as np
import pandas as pd
import re

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



def adjust_employ_machine_num(employ_balance, num_stations):
    #先四舍五入
    workstation_num = np.round(employ_balance).astype(int)
    workstation_num[workstation_num == 0] = np.ceil(employ_balance[workstation_num == 0]).astype(int)

    current_sum = workstation_num.sum()
    # print(current_sum)
    # 确保每种机器至少有一个,值为1，长度等于workstation_num数组长度
    min_required_machines = np.ones(workstation_num.shape, dtype=int)

    # 如果当前总数超过目标数量，则需要减少
    if current_sum > num_stations:
        excess = current_sum - num_stations
        # 计算小数部分，并按机器数量和小数部分降序排列
        decimal_part = employ_balance - np.floor(employ_balance)

        # 先按工作站数量降序，再按小数部分升序排序
        indices = np.lexsort((decimal_part, -workstation_num))
        for idx in indices:
            if excess <= 0:
                break
            # 减少当前机器数量，直到满足目标
            while workstation_num[idx] > min_required_machines[idx] and excess > 0:
                workstation_num[idx] -= 1
                excess -= 1
                # print(workstation_num)

    # 如果当前总数小于目标数量，则需要增加
    elif current_sum < num_stations:
        deficit = num_stations - current_sum
        # 按照工作站数量降序排列，优先增加机器较多的
        indices = np.argsort(-workstation_num)
        for idx in indices:
            if deficit <= 0:
                break
            # 增加当前机器数量，直到满足目标
            while deficit > 0:
                workstation_num[idx] += 1
                deficit -= 1
    # 确保返回调整后的工作站数量和最终总数
    final_num = workstation_num.sum()
    # 确保最终总数严格等于目标总数
    if final_num != num_stations:
        raise ValueError(f"调整后的总数 {final_num} 不等于目标 {num_stations}，请检查代码逻辑。")

   #计算机器的设备需求
    tem=pd.DataFrame(workstation_num)
    tem.insert(0,'machine',machine_list)
    result=tem.groupby('machine')['人力平衡'].sum()


    # # 添加新列 'adjust_employ_balance'
    operation_data['adjust_employ_balance'] = workstation_num
    # machine_data['adjust_machine_num']=result
    machine_data['adjust_machine_num'] = machine_data['机器种类'].map(result)
    # # 使用 ExcelWriter 写入文件，并保留其他工作表
    with pd.ExcelWriter(file_path, engine='openpyxl', mode='a', if_sheet_exists='overlay') as writer:
        # 将修改后的 DataFrame 写回原始文件中的特定工作表，不改变其他工作表
        operation_data.to_excel(writer, sheet_name='use', index=False)
        machine_data.to_excel(writer,sheet_name='machine',index=False)
    return workstation_num, final_num

def generate_machine_codes(num_stations):
    adjusted_machine_types = set()
    print(adjusted_machine_types)
    encoded_machines=[]
    adjusted_counts = []
    tem=machine_data[['机器种类','机器需求']]
    # 获取原始需求的总和
    total_demand = tem['机器需求'].sum()
    # 检查 adjusted_counts 是否有效

    # 如果总需求量为0，抛出异常
    if total_demand <= 0:
        raise ValueError("总需求量必须大于0。")
    # 遍历提取的行
    for index, row in tem.iterrows():
        machine = row['机器种类']
        count = row['机器需求']

        # 计算上限和下限
        lower_bound = max(1, int(np.floor(count)))  # 确保下限大于0
        upper_bound = int(np.ceil(count))  # 确保上限不超过原始需求

        # 随机选择机器数量，并添加到列表中
        adjusted_count = np.random.randint(lower_bound, upper_bound + 1)
        adjusted_counts.append(adjusted_count)

        # # 生成编码，并添加到数组中
        # for i in range(1, adjusted_count + 1):
        #     encoded_machines.append(f"{machine}{i}")
        #     print(encoded_machines)
    current_total = sum(adjusted_counts)
        # 确保生成的机器数量总和等于 num_stations
    while current_total  != num_stations:
        # 随机选择一个机器的编码，且避免重复选择
        if len(adjusted_counts) == 0:
            break

        random_index = np.random.choice(range(len(adjusted_counts)))
        machine_count = adjusted_counts[random_index]
        machine_type = tem.iloc[random_index]['机器种类']

        # 如果该类型机器已经调整过，则跳过
        if machine_type in adjusted_machine_types:
            print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
            continue

        # 只在数量允许的情况下进行调整
        if current_total < num_stations:
                adjusted_counts[random_index] += 1
                current_total += 1
        elif current_total > num_stations and machine_count > 1:
                adjusted_counts[random_index] -= 1
                current_total -= 1
        # # 只在数量允许的情况下进行调整
        # if machine_count > 1:
        #     # 随机选择减少或增加
        #     if np.random.rand() < 0.5:  # 减少
        #         encoded_machines = [code for code in encoded_machines if
        #                             not code.startswith(machine_type) or code[-1] != str(machine_count)]
        #         adjusted_counts[random_index] -= 1
        #         if adjusted_counts[random_index] == 0:
        #             adjusted_counts.pop(random_index)
        #     else:  # 增加
        #         adjusted_count = np.random.randint(1, 2)  # 只能加一台
        #         adjusted_counts[random_index] += adjusted_count
        #         encoded_machines.append(f"{machine_type}{adjusted_counts[random_index]}")

        # 将该类型机器标记为已调整
        adjusted_machine_types.add(machine_type)

        # 最后确保每个机器的数量都是大于0
    final_encoded_machines = []
    for index, count in enumerate(adjusted_counts):
        machine_type = tem.iloc[index]['机器种类']
        for i in range(1, count + 1):
            final_encoded_machines.append(f"{machine_type}{i}")
    return final_encoded_machines

def generate_operation_codes(machines_codes):
    allocation_result = []
    remaining_tasks = []    # 记录剩余工序
    remaining_machines  = machines_codes[:]
    tem=operation_data[['工序','机器','人力平衡']]

    # 1. 处理人力平衡大于等于 1 的工序
    for index, row in tem.iterrows():
        process = row['工序']
        machine_type = row['机器']
        balance = row['人力平衡']
        assigned_machines = []  # 用于记录已经分配的机器
        while balance >= 1 and remaining_machines:
            for i, machine in enumerate(remaining_machines):
                if machine.startswith(machine_type):  # 匹配前缀
                    allocated_machine = machine  # 找到匹配的机器
                    assigned_machines.append(allocated_machine)  # 记录分配的机器
                    # 记录匹配结果
                    allocation_result.append({'process': process, 'machine': allocated_machine})
                    balance -= 1  # 减去1人力平衡，继续处理剩余部分
                    remaining_machines.pop(i)
                    break  # 匹配到机器后跳出循环，继续检查 balance

                # 处理 balance < 1 的情况
                if balance > 0:
                    remaining_tasks.append({'process': process, 'machine': machine_type, 'balance': balance})

            # 2. 处理剩余的工序（balance < 1），允许上下浮动 ±0.5 来凑整
            task_by_machine = {}
            for task_info in remaining_tasks:
                task, machine, balance = task_info['process'], task_info['machine'], task_info['balance']
                print(task_info)
                # print("$*YHIUT&*$&F")
                if machine not in task_by_machine:
                    task_by_machine[machine] = []
                task_by_machine[machine].append((task, balance))

            for machine, tasks in task_by_machine.items():
                available_machines = [m for m in remaining_machines if m.startswith(machine)]

                for available_machine in available_machines:
                    current_balance = 0
                    current_task_list = []

                    # 尝试在允许的浮动范围内（±0.5）凑整
                    for task, balance in tasks:
                        if current_balance + balance <= 1.5:  # 增加浮动范围到±0.5
                            current_task_list.append(task)
                            current_balance += balance
                        else:
                            break  # 当超过浮动范围时停止

                    # 分配当前任务
                    if current_task_list:
                        allocation_result.append({'process': current_task_list, 'machine': available_machine})
                        remaining_machines.remove(available_machine)

                    # 移除已分配的工序
                    for task in current_task_list:
                        tasks = [t for t in tasks if t[0] != task]

            # 3. 动态调整剩余工序组合，确保所有机器都被分配到工序
            operation_codes = [''] * len(machines_codes)
            for allocation in allocation_result:
                process = allocation['process']
                machine = allocation['machine']

                if machine in machines_codes:
                    index = machines_codes.index(machine)
                    operation_codes[index] = process

            # 获取未分配的机器
            remaining_unassigned_machines = [m for i, m in enumerate(machines_codes) if operation_codes[i] == '']

            # 动态调整工序组合以匹配未分配的机器
            if remaining_unassigned_machines:
                remaining_tasks_to_assign = [t['process'] for t in remaining_tasks]

                for machine in remaining_unassigned_machines:
                    # 如果有剩余工序，可以重新组合这些工序进行分配
                    if remaining_tasks_to_assign:
                        best_fit_task_list = None
                        best_fit_balance = 0

                        # 寻找最佳组合
                        for i in range(1, len(remaining_tasks_to_assign) + 1):
                            for task_combo in itertools.combinations(remaining_tasks_to_assign, i):
                                total_balance = sum(
                                    [operation_data.loc[operation_data['工序'] == task, '人力平衡'].values[0] for task
                                     in task_combo])
                                if best_fit_balance < total_balance <= 1.5:  # 确保不超过1.5
                                    best_fit_task_list = task_combo
                                    best_fit_balance = total_balance

                        # 分配最佳组合的工序到机器
                        if best_fit_task_list:
                            for task in best_fit_task_list:
                                remaining_tasks_to_assign.remove(task)
                            process = list(best_fit_task_list) if len(best_fit_task_list) > 1 else best_fit_task_list[0]
                            index = machines_codes.index(machine)
                            operation_codes[index] = process
                    else:
                        raise ValueError("Error: Unable to allocate tasks to all machines without exceeding limits.")

            # 确保所有位置都有填充，并且长度一致
            if len(operation_codes) != len(machines_codes):
                raise ValueError("Error: The length of operation_codes does not match machines_codes.")

            if any(code == '' for code in operation_codes):
                raise ValueError("Error: There are unassigned positions in operation_codes.")

        # index = machines_codes.index(machine)
        # operation_codes[index] = process

    return operation_codes

def generate_workstation_codes(operation_codes):
    # 计算左边和右边的工作站数量
    left_count = num_stations // 2  # 左边的数量
    right_count = num_stations - left_count  # 右边的数量

    # 生成左边的编码
    left_side = [f"L{i+1}" for i in range(left_count)]
    # 生成右边的编码
    right_side = [f"R{i+1}" for i in range(right_count)]

    # 合并左右两边的工作站编码
    workstation_codes = left_side + right_side
    # 保持工作站按编号排序
    # workstation_codes.sort()
    workstation_codes = natural_sort(workstation_codes)
    # 记录未分配的工作站
    unassigned_stations = workstation_codes[:]
    # 用于记录分配结果
    allocation_result = []

    for operation in operation_codes:
        if isinstance(operation, list):  # 处理工序列表
            operation.sort()  # 按工序编号排序
            for task in operation:
                # 从未分配的工作站中选出编号最小的
                if unassigned_stations:
                    selected_station = unassigned_stations.pop(0)
                    allocation_result.append({'process': task, 'station': selected_station})
        else:  # 处理单个工序
            if unassigned_stations:
                selected_station = unassigned_stations.pop(0)
                allocation_result.append({'process': operation, 'station': selected_station})

    return workstation_codes

# 根据 operation_code 生成难易度编码
def generate_difficulty_codes(operation_codes):
    difficulty_codes = []
    for operation in operation_codes:
        difficulty = get_highest_difficulty(operation)  # 获取当前工序（或工序组合）的难度
        difficulty_codes.append(difficulty)
    return difficulty_codes

def generate_staff_codes(num_stations):
    tem_codes = list(range(1,num_stations+1))
    # print(tem_codes)
    # tem_codes=list(range(1,int(num_stations)+1))
    # staff_num_list=staff_data['员工'].to_numpy()
    # np.random.shuffle(staff_num_list)
    staff_codes=np.random.permutation(tem_codes)
    # print(staff_codes)
    # 随机打乱员工编号
    # staff_codes=staff_num_list
    return staff_codes


def allocate_operations(initial_operations, remaining_operations, remaining_machines, operation_code, machine_code):
    # 首先对初始工序进行分配
    for op in initial_operations:
        machine_prefix = op['机器'][0]  # 取机器的前缀

        # 尝试分配到对应的机器
        for machine in remaining_machines:
            if machine[0] == machine_prefix:
                if 0.9 <= op['剩余人力'] <= 1.2:
                    operation_code[machine_code.index(machine)] = op['工序']
                    remaining_operations.remove(op)
                    print(f"Allocated initial operation {op['工序']} to {machine}.")
                    break  # 继续分配下一个初始工序
        else:
            raise ValueError(f"Error: No suitable machine found for initial operation {op['工序']}.")

    # 处理剩余工序的分配
    for machine in remaining_machines:
        machine_prefix = machine[0]  # 取机器的前缀（如 'A', 'B', 'C'）

        # 找到所有同类机器的工序
        candidate_operations = [op for op in remaining_operations if op['机器'][0] == machine_prefix]

        # 尝试组合这些工序
        if candidate_operations:
            success = False

            # 找到满足人力平衡在 0.9 - 1.2 之间的组合
            def find_valid_combinations(ops, min_balance=0.9, max_balance=1.2):
                from itertools import combinations
                valid_combos = []
                for r in range(2, len(ops) + 1):  # 从2个工序开始组合
                    for combo in combinations(ops, r):
                        total_balance = sum(op['剩余人力'] for op in combo)
                        if min_balance <= total_balance <= max_balance:
                            valid_combos.append(combo)
                return valid_combos

            # 优先尝试找到满足组合条件的工序
            combos = find_valid_combinations(candidate_operations)
            if combos:
                # 如果找到多个组合，选择第一个匹配的组合
                combo = combos[0]
                operation_code[machine_code.index(machine)] = [op['工序'] for op in combo]
                for op in combo:
                    remaining_operations.remove(op)
                remaining_machines.remove(machine)
                print(f"Matched operations {[op['工序'] for op in combo]} with {machine}.")
                success = True
            else:
                # 没有直接找到组合，开始从前面已经分配的工序里找剩余人力平衡
                for op in candidate_operations:
                    if op['剩余人力'] < 0.9:
                        # 如果工序的剩余人力小于0.9，寻找已经分配的机器
                        for previous_op in operation_code:
                            if previous_op and previous_op['机器'][0] == machine_prefix and previous_op['剩余人力'] > 0:
                                # 组合剩余人力平衡
                                remaining_balance = 1 - op['剩余人力']
                                if 0.9 <= remaining_balance <= 1.2:
                                    # 将其组合并记录
                                    operation_code[machine_code.index(machine)] = [previous_op['工序'], op['工序']]
                                    remaining_operations.remove(op)
                                    remaining_machines.remove(machine)
                                    print(
                                        f"Matched operation {op['工序']} with previous {previous_op['工序']} on {machine}.")
                                    success = True
                                    break
                    if success:
                        break

            # 如果仍然没有成功匹配，则报错
            if not success:
                raise ValueError(
                    f"Error: Unable to allocate remaining operations to machine {machine}. Please check the balance constraints.")
        else:
            # 如果没有同类机器的工序，报错
            raise ValueError(f"Error: No matching operations found for machine {machine}.")


# 示例调用
# initial_operations = [...]  # 初始工序列表
# remaining_operations = [...]  # 剩余工序列表
# remaining_machines = [...]  # 剩余机器列表
# operation_code = [...]  # 操作代码的初始化
# machine_code = [...]  # 机器代码列表

# allocate_operations(initial_operations, remaining_operations, remaining_machines, operation_code, machine_code)


# 提取工作站编号中的数字并进行排序
def natural_sort(workstation_codes):
    def extract_number(code):
        return int(re.findall(r'\d+', code)[0])  # 提取数字部分并转换为整数
    return sorted(workstation_codes, key=lambda code: extract_number(code))

# 获取最高难度的函数
# 获取最高难度的函数
def get_highest_difficulty(process):
    # 从 operation_data 中提取工序和难易度
    difficulty = operation_data[['工序', '难易度']]

    # 判断传入的 process 是单个工序还是列表
    if isinstance(process, list):  # 如果是列表，选择难易度最高的
        # print(f"Process is a list: {process}")
        # 遍历 process 列表，找到每个工序对应的难易度
        difficulties = []
        for p in process:
            matched_difficulty = difficulty.loc[difficulty['工序'] == p, '难易度'].values
            if len(matched_difficulty) > 0:
                difficulties.append(matched_difficulty[0])
            else:
                print(matched_difficulty)
                print(f"工序 {p} 未找到对应的难易度")

        # # 输出调试信息
        # print(f"Difficulties found: {difficulties}")

        # 使用 difficulty_priority 字典选择难度值最小的（即优先级最高的难易度）
        if difficulties:
            return min(difficulties, key=lambda d: difficulty_priority[d])
        else:
            print("未找到匹配的难易度")
            return None
    else:
        # 单个工序时，直接返回对应的难易度
        matched_difficulty = difficulty.loc[difficulty['工序'] == process, '难易度'].values
        if len(matched_difficulty) > 0:
            return matched_difficulty[0]
        else:
            print(f"工序 {process} 未找到对应的难易度")
            return None


def allocate_remaining_operations(remaining_operations, remaining_machines, operation_code, machine_code):
    # 遍历剩余的机器，尝试分配工序
    for machine in remaining_machines:
        machine_prefix = machine[0]  # 取机器的前缀（如 'A', 'B', 'C'）

        # 先找到所有同类机器的工序
        candidate_operations = [op for op in remaining_operations if op['机器'][0] == machine_prefix]

        # 尝试组合这些工序
        if candidate_operations:
            success = False

            # 找到满足人力平衡在 0.9 - 1.2 之间的组合
            def find_valid_combinations(ops, min_balance=0.9, max_balance=1.2):
                from itertools import combinations
                for r in range(2, len(ops) + 1):  # 从2个工序开始组合
                    for combo in combinations(ops, r):
                        total_balance = sum(op['剩余人力'] for op in combo)
                        if min_balance <= total_balance <= max_balance:
                            return combo
                return None

            # 优先尝试找到满足组合条件的工序
            combo = find_valid_combinations(candidate_operations)
            if combo:
                # 匹配到的组合分配到机器上
                operation_code[machine_code.index(machine)] = [op['工序'] for op in combo]
                for op in combo:
                    remaining_operations.remove(op)
                remaining_machines.remove(machine)
                print(f"Matched operations {[op['工序'] for op in combo]} with {machine}.")
                success = True
            else:
                # 没有直接找到组合，开始从前面已经分配的工序里找剩余人力平衡
                for op in candidate_operations:
                    if op['剩余人力'] < 0.9:
                        # 如果工序的剩余人力小于0.9，寻找已经分配的机器
                        for previous_op in operation_code:
                            if previous_op and previous_op['机器'][0] == machine_prefix and previous_op['剩余人力'] > 0:
                                # 组合剩余人力平衡
                                remaining_balance = 1 - op['剩余人力']
                                if 0.9 <= remaining_balance <= 1.2:
                                    # 将其组合并记录
                                    operation_code[machine_code.index(machine)] = [previous_op['工序'], op['工序']]
                                    remaining_operations.remove(op)
                                    remaining_machines.remove(machine)
                                    print(
                                        f"Matched operation {op['工序']} with previous {previous_op['工序']} on {machine}.")
                                    success = True
                                    break
                    if success:
                        break

            # 如果仍然没有成功匹配，则报错
            if not success:
                raise ValueError(
                    f"Error: Unable to allocate remaining operations to machine {machine}. Please check the balance constraints.")
        else:
            # 如果没有同类机器的工序，报错
            raise ValueError(f"Error: No matching operations found for machine {machine}.")


# def generate_individual():
#     """
#     生成一个个体，包含机器编码、工序编码、工作站编码、难易度编码、员工编码。
#     """
#     # 1. 生成机器编码
#     machine_codes = generate_machine_codes()
#     print("%%%%%%%%%%%%")
#     # 2. 生成工序编码
#     operation_codes = generate_operation_codes(machine_codes)
#
#     # 3. 生成工作站编码
#     workstation_codes = generate_workstation_codes(operation_codes)
#
#     # 4. 生成难易度编码
#     difficulty_codes = generate_difficulty_codes(operation_codes)
#
#     # 5. 生成员工编码
#     staff_codes = generate_staff_codes(num_stations)
#
#     # 将所有编码组合成一个个体
#     individual = [
#          machine_codes,
#         operation_codes,
#         workstation_codes,
#         difficulty_codes,
#         staff_codes
#     ]
#
#     return individual


# def initialize_population(population_size):
#     population = []
#
#     # start_time=time.time()
#     for _ in range(population_size):
#         individual = generate_individual()
#         population.append(individual)
#         print(f"个体{_}")
#         for layer in individual:
#             print(layer)
#         # print(individual)
#         print()
#     return population


# 初始化种群
# population = initialize_population(population_size)

#
# # 输出生成的种群
# for i, individual in enumerate(population):
#     print(f"Individual {i + 1}:")
#     for layer in individual:
#         print(layer)

# aa=adjust_employ_machine_num(employ_balance, num_stations)
codes = generate_machine_codes(num_stations)
# generate_machine_codes(generate_machine_codes)
# sdf=generate_operation_codes(generate_machine_codes())
# codes2 = generate_workstation_codes(generate_operation_codes(generate_machine_codes()))
# jewu=generate_workstation_codes(generate_operation_codes(generate_machine_codes()))
# tge=generate_difficulty_codes(generate_operation_codes(generate_machine_codes()))
# yenr=generate_staff_codes(generate_operation_codes(generate_machine_codes()))
# print(codes)
# kddhewj=allocate_operations(generate_machine_codes())
# print(sdf)
print(codes)
# print(kddhewj)

