from random import random


def adjust_workstation_machine(child,station_num):
    print(f"170170")
    print(child)
    # print("----------------------------------------------")
    # 这个编码可能有缺失，所以要调整
    wk=child['individual']['workstation_code']

    # check_num,tem_wk_num=check_adjust_workstation(wk,23)

    # 获取每个工作站对应的机器：{'R1': 'A', 'R7': 'A'}
    workstation_machines = child['individual']['workstation_machines']
    # check_wk_ma(workstation_machines,23)
    # print(f"workstation_machines{workstation_machines}")

    # 将所有工作站从嵌套列表中提取出来，变成一个一维列表 提取出交叉后子代的工作站编码，这时候的工作站编码会缺失一些
    # 获取交叉后的wk编码（有缺失），将其提取出来，看是否会有缺失
    # {'L2', 'R10', 'L9', 'L6', 'R3', 'L7', 'R4', 'R9', 'L1', 'R8', 'R5', 'R2', 'L10', 'L11', 'L3', 'L8', 'R11', 'R12', 'L5', 'R6'}
    assigned_workstations = set(workstation for sublist in wk for workstation in sublist)

    # 获取所有的工作站，workstation_machines中出现的工作站
    all_workstations = set(workstation_machines.keys())


    # 获取没有分配的工作站
    missing_workstations = list(all_workstations - assigned_workstations)
    print(f"190190")
    print(f"workstation_machines{workstation_machines}")
    print(f"获取所有的工作站{all_workstations}")
    print(f"现有的工作站，即交叉后子代的编码，这时候有缺失{assigned_workstations}")
    # print(tem_wk_num)
    print(f"没有分配的工作站{missing_workstations}")

    # 当前个体需要的机器
    machine_codes = child['individual']['machine_code']
    machine_codes_set = set(machine_codes)
    print(f"当前个体需要的机器{machine_codes_set}")
    # print(f"当前个体需要的机器machine_codes{machine_codes_set}")

    # 获取 workstation_machines 中所有的机器类型
    workstation_machines_values = set(workstation_machines.values())
    print(f"原编码中的机器类型{workstation_machines_values}")

    # 找出 workstation_machines 中出现，但 machine_codes 中没有的机器类型
    # 有五种可能！！！
    unused_machines = workstation_machines_values - machine_codes_set
    print(f"原编码中的机器类型-先编码的机器类型，{unused_machines}")


    # 获取所有机器类型的工作站
    stations_using_machine = {}
    for machine in set(machine_codes):
        stations_using_machine[machine] = [station for station, m in workstation_machines.items() if m == machine]
    print(f"获取该编码所有机器类型对应的工作站stations_using_machine{stations_using_machine}")

    # 检查哪些机器类型已经分配到工作站
    assigned_machines = set(m for station in assigned_workstations for station, m in workstation_machines.items() if station in assigned_workstations)
    print(f"检查该编码哪些机器分配到工作站了{assigned_machines}")
    # print(f"assigned_machines{assigned_machines}")

    # 找出当前个体缺失的机器，即调整后该编码需要的机器-当前未调整的编码中已经分配了工作站的机器
    missing_machines = set(machine_codes) - assigned_machines
    print(f"当前缺失的机器{missing_machines}")
    # print(f"当前缺失的机器！！！")
    if missing_machines==set():
        print(f"当前没有缺失机器")

    # 处理交叉后没有的机器，即占用别的机器位置的机器
    if unused_machines:
        print("有问题，但是有时跑不出来！！！！！！")
        print(f"215hang")
        for i in unused_machines:
            if i in stations_using_machine:
                tem_unused_wk=stations_using_machine[unused_machines]
                # 将这些工作站添加到 missing_workstations 中
                missing_workstations.extend(stations_using_machine)
            # 删除 stations_using_machine 中对应机器的工作站数据
            for station in stations_using_machine:
                if station in workstation_machines:
                    del workstation_machines[station]  # 删除工作站对应的机器


    # 用来记录跳过的工作站，稍后进行处理
    pending_workstations = []

    for i in range(len(wk)):
        machine=machine_codes[i]
        tem_balance=child['individual']['balance_code'][i]
        op=child['individual']['operation_code'][i]

        # 如果当前机器属于未分配的机器
        if machine in missing_machines:
            # 遍历当前个体原来的工作站
            for j in range(len(wk[i])):
                tem_workstation=wk[i][j] #当前工作站
                # print(f"tem_workstation{tem_workstation}")
                # 如果当前个体工作站配对的机器不等于该工序所需要的机器
                if workstation_machines.get(tem_workstation) != machine:
                    # 如果 tem_workstation 不匹配，随机选择一个替代
                    # print(f"工作站 {tem_workstation} 的机器类型与 {machine} 不匹配，随机选择一个替换...")
                    # 如果当前存在未分配的工作站
                    if missing_workstations:
                        tem_arr = wk[i][j]
                        chosen_station=random.choice(missing_workstations)
                        # 修改workstation_code的值
                        child['individual']['workstation_code'][i][j]=
                        # 这个工作站分配完后就从未分配中删除
                        missing_workstations.remove(chosen_station)
                        # print(f"missing_workstations{missing_workstations}")
                        # 修改workstation_machines中该工作站对应机器的值
                        child['individual']['workstation_machines'][chosen_station]=machine
                        # 判断原本的工作站是否还有分配给别的工序，如果没有的话就加入未分配中
                        # 将所有工作站从嵌套列表中提取出来，变成一个一维列表
                        # assigned_workstations_tem = set(workstation for sublist in child['individual']['workstation_code'] for workstation in sublist)
                        assigned_workstations_tem = set()
                        for sublist in child['individual']['workstation_code']:

                            for workstation in sublist:
                                print(f"276276")
                                print(workstation)
                                assigned_workstations_tem.add(workstation)

                        if tem_arr not in assigned_workstations_tem:
                            missing_workstations.append(tem_arr)
                    else:
                        # 如果没有缺失工作站，记录下当前需要处理的工作站，稍后处理
                        # print("!!!!!!!!!!!!!!!!!!!!!!")
                        # print(f"当前工作站是{tem_workstation}")
                        # 将当前工作站的值赋为空
                        child['individual']['workstation_code'][i][j]=[]
                        print("assigned_workstations_tem")
                        # 之后判断tem_workstation是否有分配到其他工序，即是否还有在workstation_code中出现，没有的话就加入missing_workstations

                        assigned_workstations_tem = set()
                        # for sublist in child['individual']['workstation_code']:
                        #     for workstation in sublist:
                        #         if isinstance(workstation, list):
                        #             print(f"workstation{workstation}")
                        #
                        #             assigned_workstations_tem.add(workstation)
                        #         else:
                        #             assigned_workstations_tem = set( workstation for sublist in child['individual']['workstation_code'] for workstation in sublist)

                        # assigned_workstations_tem = set()
                        for sublist in child['individual']['workstation_code']:
                            for workstation in sublist:
                                # print("assigned_workstations_tem")
                                # print(f"workstation{workstation}")
                                if not workstation:
                                    continue
                                else:
                                    assigned_workstations_tem.add(workstation)

                        if tem_workstation not in assigned_workstations_tem:
                            missing_workstations.append(tem_workstation)
                        # print(f"工序{op}机器 {machine} 对应的工作站暂时未分配，跳过该工序，该工序的人力平衡是{tem_balance}")
                        pending_workstations.append({'op': op, 'machine': machine, 'tem_balance': tem_balance})
        else:
            # 当前机器已经分配过了，即没有未分配的机器
            for j in range(len(wk[i])):
                # print(f"wk[i][j]{wk[i][j]}")
                if wk[i][j] not in stations_using_machine[machine]:
                    # print("说明机器跟工作站不匹配")
                    # print(f"stations_using_machine[machine]{stations_using_machine[machine]}")
                    if missing_workstations:
                        # print(f"还有未分配的工作站")
                        tem_arr=wk[i][j]
                        chosen_station = random.choice(missing_workstations)
                        # 修改workstation_code的值
                        child['individual']['workstation_code'][i][j]=chosen_station
                        # 删除已经选中的工作站
                        missing_workstations.remove(chosen_station)
                        # 修改workstation_machines中的值
                        child['individual']['workstation_machines'][chosen_station] = machine
                        # assigned_workstations_tem = set(workstation for sublist in child['individual']['workstation_code'] for workstation in sublist)
                        assigned_workstations_tem = set()
                        for sublist in child['individual']['workstation_code']:
                            for workstation in sublist:
                                assigned_workstations_tem.add(workstation)

                        if tem_arr not in assigned_workstations_tem:
                            missing_workstations.append(tem_arr)
                    else:
                        # print(f"没有未分配的机器")
                        wk[i][j]=random.choice(stations_using_machine[machine])
                        child['individual']['workstation_code'][i][j] = wk[i][j]


    if pending_workstations:
        current_workstations=[]
        # print(f"有未处理的工序{pending_workstations}！！！！！！！！！！！！！！！！！！！！！！！！")
        for pending in pending_workstations:
            op = pending['op']
            machine = pending['machine']
            tem_balance = pending['tem_balance']
            # 确认当前机器是否存在于 stations_using_machine 中
            if machine in stations_using_machine:
                # 找到所有机器对应的工作站列表长度大于等于 tem_balance 的机器
                machines_with_sufficient_workstations = [machine for machine, workstations in stations_using_machine.items() if len(workstations) >= tem_balance]

                for i in range(tem_balance):
                    # print(f"机器对应长度大于{tem_balance}的数据{machines_with_sufficient_workstations}")
                    # 随机选择一个机器其工作站的值大于tem_balance
                    selected_machine = random.choice(machines_with_sufficient_workstations)
                    # print(f"selected_machine{selected_machine}")
                    # print(f"这个机器对应的工作站值是{stations_using_machine[selected_machine]}")

                    # 随机从这个机器对应的工作站中选择一个
                    selected_wk=random.choice(stations_using_machine[selected_machine])
                    # 将选择的工作站添加到现在机器对应的值中
                    stations_using_machine[machine].append(selected_wk)
                    # 添加到current_workstations，后面将current_workstations赋值给该位置的工序
                    current_workstations.append(selected_wk)
                    # 将选择的工作站从原来的机器中溢出
                    stations_using_machine[selected_machine].remove(selected_wk)
                    # 修改workstation_machines中的值
                    child['individual']['workstation_machines'][selected_wk] = machine

                    # 找到该工序对应的索引
                op_index = child['individual']['operation_code'].index(op)
                # 将原来交叉后的工作站值修改
                child['individual']['workstation_code'][op_index] = current_workstations
                # print(child['individual']['workstation_code'][op_index])
                # child['individual']['workstation_machine']=


    # 如果还有未分配的工作站
    if missing_workstations:
        # 提取出所有工作站，展平嵌套列表
        workstations_in_code = set(workstation for sublist in child['individual']['workstation_code'] for workstation in sublist)
        # 获取 workstation_machines 中的所有工作站
        workstations_in_machines = set(workstation_machines.keys())

        # print(f"workstations_in_code{workstations_in_code}")
        # print(f"workstations_in_machines{workstations_in_machines}")


        # 比较两个集合，确保工作站都存在
        if workstations_in_code == workstations_in_machines:
            print("所有工作站都匹配")
            print(f"383")
            print(f"workstations_in_code{workstations_in_code}")
            print(f"workstations_in_machines{workstations_in_machines}")

        else:
            print("有工作站未匹配")
            print(f"缺失的工作站{workstations_in_code - workstations_in_machines}")
    # print("--------------------------------")
    # print("最后调整的结果是：")
    # print(child['individual']['workstation_code'])
    # print("--------------------------------")
