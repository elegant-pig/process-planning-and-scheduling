import random  # 导入随机库，用于随机打乱工序顺序
from decimal import Decimal  # 导入Decimal以精确处理人力平衡的浮点数


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


def combine_operations(tem_array, type_count):
    """
    尝试将工序组合成指定数量的有效组合。

    :param tem_array: 包含工序及其人力平衡的列表
    :param type_count: 需要生成的组合数量
    """
    # 设置人力平衡的允许范围
    min_balance = Decimal('0.8')
    max_balance = Decimal('1.2')
    attempts = 0  # 尝试次数计数器
    max_attempts = 5  # 最大尝试次数
    successful_combination = []  # 存储找到的有效组合

    while attempts < max_attempts:  # 当尝试次数未达到最大值时循环
        random.shuffle(tem_array)  # 打乱工序顺序以增加随机性
        combinations = []  # 存储当前的有效组合
        current_combination = []  # 存储正在构建的当前组合
        current_balance = Decimal('0')  # 当前组合的人力平衡总和

        for item in tem_array:  # 遍历每个工序
            current_combination.append(item)  # 将工序添加到当前组合
            current_balance += item[1]  # 累加当前组合的人力平衡

            # 检查当前组合是否在允许的人力平衡范围内
            if valid_combination(current_combination, min_balance, max_balance):
                combinations.append(current_combination)  # 记录有效组合
                current_combination = []  # 重置当前组合
                current_balance = Decimal('0')  # 重置平衡

        # 检查是否有剩余的工序未组合
        if current_combination:
            combinations.append(current_combination)  # 将剩余工序作为组合添加

        # 验证组合数量是否等于type_count
        if len(combinations) == type_count:
            successful_combination = combinations  # 记录成功的组合
            break  # 找到有效组合，退出循环
        attempts += 1  # 增加尝试次数

    # 如果没有找到有效的组合，输出提示信息
    if not successful_combination:
        print("未能在 5 次尝试内找到有效的组合。")
    else:
        print("找到的有效组合：")  # 输出找到的组合
        for idx, combo in enumerate(successful_combination):
            print(f"组合 {idx + 1}: {combo}")  # 打印每个组合的内容


# 示例数据
tem_array = [(3, Decimal('0.8')), (4, Decimal('0.4')), (5, Decimal('0.6')), (8, Decimal('0.4')), (9, Decimal('0.4'))]
type_count = 3  # 需要组合的数量

combine_operations(tem_array, type_count)  # 调用组合函数
