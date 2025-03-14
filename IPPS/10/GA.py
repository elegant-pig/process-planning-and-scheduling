import random
from data_solve import component_operation_mapping

population_size = 10 #种群大小

# 获取所有部件
components = list(component_operation_mapping.keys())

# 固定最后一个部件
last_component = components[-1]
# 除去最后一个部件
components_without_last = components[:-1]

# 生成遗传算法第一层个体（部件顺序）
def generate_individual_first_layer():
    # 将除最后一个部件的所有部件随机打乱顺序
    shuffled_components = random.sample(components_without_last, len(components_without_last))
    # 最后一个部件固定在最后
    shuffled_components.append(last_component)
    return shuffled_components

# 生成遗传算法第二层个体（工序顺序）
def generate_individual_second_layer(component_order):
    operation_sequence = []
    for component in component_order:
        # 从 component_operation_mapping 中获取该部件的工序列表，并按其顺序排列
        operations = component_operation_mapping[component]
        for op in operations:
            # 添加每个工序的细节到第二层序列
            operation_sequence.append({
                'component': component,
                'operation': op['operation'],
                'machine': op['machine'],
                'difficulty': op['difficulty']
            })
    return operation_sequence

# 生成包含两层编码的个体
def generate_individual():
    # 第一层：部件顺序
    first_layer = generate_individual_first_layer()
    # 第二层：基于第一层部件顺序的工序顺序
    second_layer = generate_individual_second_layer(first_layer)
    return first_layer, second_layer

# 生成初始种群
def generate_initial_population(population_size):
    population = []
    for _ in range(population_size):
        individual = generate_individual()
        population.append(individual)
    return population

initial_population = generate_initial_population(population_size)

# 打印生成的初始种群（第一层和第二层）
for i, (first_layer, second_layer) in enumerate(initial_population, 1):
    print(f"Individual {i} - First Layer (Component Order): {first_layer}")
    print(f"Individual {i} - Second Layer (Operation Sequence):")
    for operation in second_layer:
        print(f"  Component: {operation['component']}, "
              f"Operation: {operation['operation']}, "
              f"Machine: {operation['machine']}, "
              f"Difficulty: {operation['difficulty']}")