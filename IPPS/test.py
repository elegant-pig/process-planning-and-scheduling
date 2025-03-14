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

        # 将选择的个体添加到 selected_individuals 中
        selected_individuals.append(population[selected_idx])

        # 4. 从 population 中移除已选择的个体
        population.pop(selected_idx)

    return selected_individuals
