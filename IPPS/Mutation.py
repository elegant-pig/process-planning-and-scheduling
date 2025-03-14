import random
from collections import defaultdict

import pandas as pd

import Crossover
import generateOperation
from check_code import check_adjust_workstation


def mutate(individual, mutation_rate):
    for i in individual:
        # check_adjust_workstation(i['individual']['workstation_code'],23)
        # print(f"mutate")
        # check_adjust_workstation(i['individual']['workstation_code'], 23)

        print(f"变异！！")
        # print(i['individual']['employ_code'])
        # 交叉变异，修改个体的or、op、machine值
        mutation_or_op_machine_node(mutation_rate,i)
        mutate_worstation_code(mutation_rate,i)
        mutate_employ_code(mutation_rate,i)
        print(f"workstation_machines is {i['individual']['workstation_machines']}")
        print(f"result_employ_allocation is {i['individual']['result_employ_allocation']}")

        # 'balance_code': balance_code,
        # 'workstation_machines': workstation_machines, 不需要调整，都是在同样机器上的工作站上选择
        # 'result_employ_allocation': result_employ_allocation
    return individual


def mutation_or_op_machine_node(mutation_rate,individual):
    print(mutation_rate)
    print(individual)
    replace_ops = individual['individual']['replace_op']
    or_node = individual['individual']['OR_CODE']
    file_path = 'data/operation_data.xlsx'
    operation_data = pd.read_excel(file_path, sheet_name='final')
    data = operation_data.copy()
    machine_code=[]
    mutate_num = int(round((mutation_rate * len(or_node)))) #变异的基因个数
    if mutate_num == 0:
        mutate_num = 1

    # 对or_node进行变异,并相应修改op_code
    for i in range(mutate_num):
        kk=random.choice(replace_ops)
        # 遍历 or_node 并替换符合条件的值
        for node in or_node:
            for key, value in node.items():
                if value in kk:
                    # 选择 kk 中的另一个随机值（排除当前值）
                    new_value = random.choice([x for x in kk if x != value])
                    node[key] = new_value  # 替换值

    # 创建一个空列表用于存储 C1 未选择的替换工序
    non_selected_operations = []
    # print()
    # 从 OR_CODE 提取已选择的工序编号
    selected_operations = [list(item.values())[0] for item in or_node]  # 提取工序编号，比如 [6, 12]

    # 遍历 tem_array，提取未选择的工序
    for operation_pair in replace_ops:
        for operation in operation_pair:
            if operation not in selected_operations:
                non_selected_operations.append(operation)
    data = data[~data['工序'].isin(non_selected_operations)]
    data = data[['部件', '工序', '机器', '标准工时', '难易度', '前继工序', '前继工序数量']]

    _, operation_codes = generateOperation.generate_operation_codes(data)
    # 修改个体的or_node值
    individual['individual']['OR_CODE']=or_node
    # 修改个体的operation_code值
    individual['individual']['operation_code'] = operation_codes
    # 修改个体的machine_code值
    # 遍历每个操作编码，查找对应的机器编码
    for code in operation_codes:
        print(f"747474")
        # 提取工序编号 j
        op_num = int(code.split(',')[1])  # 获取操作编码中的工序编号
        # print(op_num)
        # 查找工序编号对应的机器编码
        current_machine_code = data[data['工序'] == op_num]['机器'].values[0]
        machine_code.append(current_machine_code)
        # print(f'machine_code{machine_code}')
    individual['individual']['machine_codes'] = machine_code
    print(f"individual['individual']['machine_codes']{individual['individual']['machine_codes']}")

def mutate_worstation_code(mutation_rate,individual):
    old_wk=individual['individual']['workstation_code']
    machine_code=individual['individual']['machine_code']
    old_wk_ma=individual['individual']['workstation_machines']
    print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")

    print(f"原来的工作站编码 is {old_wk_ma}")
    mutate_num = int(round((mutation_rate * len(individual['individual']['workstation_code'])))) #变异的基因个数
    if mutate_num==0:
        mutate_num=1
    selected_indices=set()

    # print(f"individual is {individual}")
    for i in range(mutate_num):
        available_indices = [i for i in range(len(old_wk)) if i not in selected_indices]
        if not available_indices:  # 如果所有索引都选过了，停止
            break
        # 选择 old_wk 中的随机索引
        outer_index = random.randint(0, len(old_wk) - 1)
        selected_indices.add(outer_index)  # 记录已选索引
        # # 检查子列表长度
        # if len(old_wk[outer_index]) == 1:
        #     inner_index = 0  # 只有一个值，索引固定为 0
        # else:
        #     inner_index = random.randint(0, len(old_wk[outer_index]) - 1)

        tem_machine=machine_code[outer_index]
        tem_wk=old_wk=individual['individual']['workstation_code'][outer_index]
        print(f"当前对应的工作站是{tem_wk}")

        valid_workstations = [ws for ws, machine in old_wk_ma.items() if machine == tem_machine]
        print(f"valid_workstations is {valid_workstations}")
        # 如果没有符合的工作站，返回 None
        if not valid_workstations:
            return None

        new_wk = []
        for m in tem_wk:
            # 随机选择一个符合条件的工作站
            new_m = random.choice(valid_workstations)
            # m=random.choice(valid_workstations)
            new_wk.append(new_m)

        individual['individual']['workstation_code'][outer_index] = new_wk
        print(f"更新后的tem_wk  is {new_wk}")
    print(f"更改后的工作站编码")
    print(individual['individual']['workstation_code'])
    # check_adjust_workstation(individual['individual']['workstation_code'],23)

def mutate_employ_code(mutation_rate,individual):
    # print(f"工作站与员工的分配")
    # print(individual['individual'])
    # 用一个字典来存储每个工作站对应的唯一员工
    workstation_employ_dict = defaultdict(set)
    # print(individual['individual']['employ_code'])
    print(f"变异前的编码")
    print(individual['individual']['employ_code'])

    # 将数据整理到字典中，避免重复的员工
    for group in enumerate(individual['individual']['employ_code']):
        # print(f"group is {group}")
        for entry in group[1]:
            workstation = entry['workstation']
            employee_id = entry['id']
            workstation_employ_dict[workstation].add(employee_id)
    # 重建去重后的数据
    deduplicated_data = []
    for workstation, employees in workstation_employ_dict.items():
        for employee_id in employees:
            deduplicated_data.append({'workstation': workstation, 'id': employee_id})

    # 输出去重后的数据
    print(f"去重后的数据")
    print(deduplicated_data)

    mutate_num = int(round((mutation_rate * len(individual['individual']['employ_code']))))  # 变异的基因个数
    if mutate_num == 0 or mutate_num % 2 != 0:
        mutate_num += 1

    for i in range(mutate_num//2):
        # 随机选择两个不同的字典
        choice1, choice2 = random.sample(deduplicated_data, 2)
        # print(f"选择的两个值")
        # print(choice1)
        # print(choice2)
        # 交换它们的 id
        tem_id=choice1['id']
        choice1['id']=choice2['id']
        choice2['id']=tem_id
        # print(f"更改后的值")
        # print(f"choice1 is{choice1},id is {choice1['id']}")
        # print(f"choice2 is{choice2} ,id is {choice2['id']}")
    # print(f"变异后的值{deduplicated_data}")


    for group in individual['individual']['employ_code']:
        for wk in group:
            # 遍历修改后的数据，找到对应的 workstation
            for modified_item in deduplicated_data:
                # print(f"原来工作站{wk['workstation']},后面工作站{modified_item['workstation']}")
                # print(f"原来工作站员工{wk['id']}，后面工作站员工{modified_item['id']}")
                if wk['workstation'] == modified_item['workstation']:
                    # print(f"原来工作站员工{wk['id']}，后面工作站员工{modified_item['id']}")
                    wk['id'] = modified_item['id']

    print(f"变异后的编码")
    print(individual['individual']['employ_code'])





# 变异率设置为 0.05，即每个个体有 5% 的概率发生变异
mutation_rate = 0.05


