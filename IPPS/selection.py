import random

import calculate
import init


# def selection_()

def elitism_selection(solution,elite_size):
    """
    使用精英策略选择最优个体并返回。

    参数:
    - solution: 个体的适应度值列表
    - elite_size: 保留的最优个体数量

    返回:
    - elite_individuals: 保留的最优个体
    """
    elite_individuals = solution[:elite_size]

    # print(elite_individuals)
    # print(len(elite_individuals))
    return elite_individuals



import random

def roulette_wheel_selection(population, elite_size):
    """
    使用归一化方法的轮盘赌选择算法，并将 max_fitness 设置为最大适应度值的两倍。
    :param population: 所有个体的列表
    :param elite_size: 选择的个体数量
    :return: 选择的个体
    """
    selected_individuals = []

    for _ in range(elite_size):
        # 1. 计算适应度，distance 越小适应度越高
        fitness_values = []
        valid_distances = [individual['fitness'] for individual in population if individual['fitness'] > 0]

        # 确保最小距离不是 0
        min_distance = min(valid_distances) if valid_distances else 1

        for individual in population:
            distance = individual['fitness']
            if distance == 0:
                # 如果 distance 为 0，适应度设置为最大适应度的两倍
                fitness_values.append(round((1 / min_distance) * 2, 4) if min_distance != 0 else 1)
            else:
                # 计算适应度
                fitness_values.append(round(1 / distance, 4))

        # 2. 归一化适应度
        total_fitness = sum(fitness_values)

        # 归一化过程：将适应度缩放到 [0, 1] 区间
        normalized_fitness_values = [fitness / total_fitness for fitness in fitness_values]

        # 3. 轮盘赌选择
        random_choice = random.random()  # 随机选择一个 [0, 1) 之间的数
        cumulative_probability = 0.0
        selected_idx = None
        for i, prob in enumerate(normalized_fitness_values):
            cumulative_probability += prob
            if random_choice <= cumulative_probability:
                selected_idx = i
                break

        # 如果没有选中任何个体，则处理错误
        if selected_idx is None:
            selected_idx=0

        # 将选择的个体添加到 selected_individuals 中
        selected_individuals.append(population[selected_idx])

        # 4. 从 population 中移除已选择的个体
        population.pop(selected_idx)

    return selected_individuals


# def roulette_wheel_selection(population, elite_size):
#     """
#     使用归一化方法的轮盘赌选择算法，并将 max_fitness 设置为最大适应度值的两倍。
#     :param population: 所有个体的列表
#     :param distances: 对应的个体的距离（即 distance 越小越好）
#     :return: 选择的个体
#     """
#     # 1. 计算适应度，distance 越小适应度越高
#     fitness_values = []
#     valid_distances = [individual['fitness'] for individual in population if individual['fitness'] > 0]
#
#     # 确保最小距离不是 0
#     # min_distance = min(individual['individuals']['distance'] for individual in population)
#     # 如果所有个体的 distance 都为 0，默认设置为 1
#     min_distance = min(valid_distances) if valid_distances else 1
#     # max_distance = max(individual['individuals']['distance'] for individual in population)
#
#     for individual in population:
#         distance = individual['fitness']
#         if distance == 0:
#             # 如果 distance 为 0，适应度设置为最大适应度的两倍
#             fitness_values.append(round((1 / min_distance)*2,4) if min_distance != 0 else 1)
#         else:
#             # 计算适应度
#             fitness_values.append(round(1 / distance,4))
#
#     # 2. 归一化适应度
#     # 获取所有适应度的最大值
#     total_fitness = sum(fitness_values)
#
#     # 归一化过程：将适应度缩放到 [0, 1] 区间
#     # 计算每个个体的选择概率
#     normalized_fitness_values = [fitness / total_fitness for fitness in fitness_values]
#
#     # 5. 轮盘赌选择
#     selected_individuals = []
#     # 5. 轮盘赌选择
#     for _ in range(elite_size):
#         random_choice = random.random()  # 随机选择一个 [0, 1) 之间的数
#         cumulative_probability = 0.0
#         for i, prob in enumerate(normalized_fitness_values):
#             cumulative_probability += prob
#             if random_choice <= cumulative_probability:
#                 selected_individuals.append(population[i])
#                 break
#
#     return selected_individuals
# elitism_selection(calculate.calculate(main.population),main.elite_size)
# roulette_wheel_selection(calculate.calculate(main.population),main.elite_size )
