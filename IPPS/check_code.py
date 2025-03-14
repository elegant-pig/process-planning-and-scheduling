from itertools import chain


def check_employ_efficiency(code,num):
    # print(f"check_workstation")
    # print(code)
    unique_workstations = set()
    unique_ids = set()

    # 遍历 wk_staff 结构，提取唯一的 workstation 和 id
    for group in code:
        for entry in group:
            unique_workstations.add(entry['workstation'])
            unique_ids.add(entry['id'])

    # 获取去重后的数量
    workstation_count = len(unique_workstations)
    id_count = len(unique_ids)

    # 检查是否都等于 num
    if workstation_count == id_count == num:
        return True
    else:
        print(f"Workstation 去重后数量: {workstation_count}")
        print(f"ID 去重后数量: {id_count}")
        print(f"预期数量 (num): {num}")
        return False

def check_generateWorkstation(code,num):
    # print(code)
    unique_items = set()

    # 遍历列表，将所有元素添加到集合中
    for sublist in code:
        unique_items.update(sublist)

    # 计算去重后的元素个数
    unique_count = len(unique_items)
    # print(f"去重后的个数是{unique_count}")
    # print(f"是否等于num{unique_count == num, unique_count}")

    if unique_count != num:
        raise ValueError("生成的工作站数量不对")
    else:
        return unique_count == num
def check_adjust_workstation(code,num):
    print(f"414141")
    print(code)
    unique_stations=set(station for sublist in code for station in sublist)
    unique_count = len(unique_stations)
    print(f"unique_count{unique_count}")
    if unique_count != num:
        raise ValueError("工作站数量不对")

    # # 将所有工作站从嵌套列表中提取出来，变成一个一维列表
    # assigned_workstations = set(workstation for sublist in wk for workstation in sublist)
def check_wk_ma(code,num):
    print(f"575757")
    # {'L7': 'A', 'R3': 'A', 'L8': 'A', ……}
    print(code)
    # unique_stations = set(station for sublist in code for station in sublist)
    # 计算唯一键的个数
    unique_key_count = len(set(code.keys()))
    print(f"unique_key_count{unique_key_count}")
    # 检查数量是否等于 num
    is_equal = (unique_key_count == num)
    print(f"is_equal{is_equal}")
    if unique_key_count != num:
        raise ValueError("工作站数量不对")
    # return is_equal

def check_wk_ma2(code,num):
    print(code)
    print(code.values())
    # 提取所有键的值并去重
    unique_workstations = set(chain.from_iterable(code.values()))
    # 计算去重后的数量
    unique_count = len(unique_workstations)
    if unique_count != num:
        print(unique_count)
        raise ValueError("工作站数量不对")


def check_employ_code(code ,num):
    print(code)
    # 提取所有的 employ 值
    employ_values = [entry['employ'] for entry in code]

    # 去重
    unique_employ_values = set(employ_values)

    # 检查去重后的数量是否等于 23
    if len(unique_employ_values) == num:
        print("员工ID的数量等于23")
    else:
        print(f"员工ID的数量为 {len(unique_employ_values)}")
        raise ValueError('员工数量不对')

def check_adjust_employ(code,num):
    # unique_employs = set()  # 存储唯一的 (workstation, id) 组合
    #
    # for employ_list in code:
    #     for employ in employ_list:
    #         unique_employs.add((employ['workstation'], employ['id']))  # 转换为 tuple 以便存入 set
    #
    # if len(unique_employs)!=num:
    #     print(f"{len(unique_employs)}")
    #     raise ValueError('数量不一致')
    # 提取所有 id 并去重
    unique_ids = {emp['id'] for sublist in code for emp in sublist}
    print(f"unique_ids{unique_ids}")

    # 判断去重后的 id 数量是否等于 23
    if len(unique_ids) == num:
        print("ID 数量正确，去重后的数量为 23")
    else:
        print(f"ID 数量不正确，去重后的数量为 {len(unique_ids)}")
        raise ValueError('员工数量不对')

def check_result_employ_allocation(code,num):
    print(code)

    # 使用字典的方式按 `workstation` 去重
    unique_data_workstation = {entry['workstation']: entry for entry in code}.values()

    # 按 `employ` 去重
    unique_data_employ = {entry['employ']: entry for entry in code}.values()

    # 按 `workstation` 和 `employ` 同时去重
    unique_data_both = {f"{entry['workstation']}_{entry['employ']}": entry for entry in code}.values()

    # 获取去重后的数量
    len_workstation = len(unique_data_workstation)
    len_employ = len(unique_data_employ)
    len_both = len(unique_data_both)

    # 断言三个去重方式的结果数量必须相同，否则报错
    assert len_workstation == len_employ == len_both ==num, f"去重后数量不一致: workstation={len_workstation}, employ={len_employ}, both={len_both}"

    print(f"去重后数量一致")

