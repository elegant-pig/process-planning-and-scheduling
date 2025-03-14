import pandas as pd

# 读取 Excel 文件，加入异常处理
file_path = '../data/data.xlsx'  # 请替换为你的 Excel 文件路径
try:
    df = pd.read_excel(file_path)
except FileNotFoundError:
    print(f"Error: 文件 {file_path} 未找到。请检查路径是否正确。")
    exit()
except Exception as e:
    print(f"Error: 读取文件时出错 - {e}")
    exit()

# 检查文件内容是否按预期读取
if df.empty:
    print("Error: 读取的 Excel 文件为空。")
    exit()

# 初始化计数器用于重命名
component_counter = 1
operation_counter = 1
machine_counter = 1
difficulty_counter = 1

# 用于保存重命名的映射
component_rename_mapping = {}
operation_rename_mapping = {}
machine_rename_mapping = {}
difficulty_rename_mapping = {}

# 提取部件、工序、机器、难易度和标准工时的关系
# 构建字典，表示部件与其工序的关系
component_operation_mapping = {}

# 遍历每一行，构建部件与工序-机器-难易度-标准工时的关系
for _, row in df.iterrows():
    component = row['部件']
    operation = row['工序']
    machine = row['机器']
    difficulty = row['难易度']
    standard_time = row['标准工时']  # 读取标准工时

    # 跳过有缺失数据的行
    if pd.isna(component) or pd.isna(operation) or pd.isna(machine) or pd.isna(difficulty) or pd.isna(standard_time):
        print(f"Warning: 跳过了有缺失数据的行: {row}")
        continue

    # 对部件进行重命名
    if component not in component_rename_mapping:
        component_rename_mapping[component] = f"{component_counter}"
        component_counter += 1
    renamed_component = component_rename_mapping[component]

    # 对工序进行重命名
    if operation not in operation_rename_mapping:
        operation_rename_mapping[operation] = f"{operation_counter}"
        operation_counter += 1
    renamed_operation = operation_rename_mapping[operation]

    # 对机器进行重命名
    if machine not in machine_rename_mapping:
        machine_rename_mapping[machine] = f"{machine_counter}"
        machine_counter += 1
    renamed_machine = machine_rename_mapping[machine]

    # 对难易度进行重命名
    if difficulty not in difficulty_rename_mapping:
        difficulty_rename_mapping[difficulty] = f"{difficulty_counter}"
        difficulty_counter += 1
    renamed_difficulty = difficulty_rename_mapping[difficulty]

    # 如果字典中还没有该部件，则创建一个新条目
    if renamed_component not in component_operation_mapping:
        component_operation_mapping[renamed_component] = []

    # 将工序、机器、难易度和标准工时的重命名后的字典添加到该部件的列表中
    component_operation_mapping[renamed_component].append({
        'operation': renamed_operation,
        'machine': renamed_machine,
        'difficulty': renamed_difficulty,
        'standard_time': standard_time  # 加入标准工时
    })

# 打印出构建好的部件关系，并将所有信息放在一行中
for component, operations in component_operation_mapping.items():
    operations_info = ", ".join(
        [f"O{op['operation']} - M{op['machine']} - D{op['difficulty']} - T{op['standard_time']}" for op in operations]
    )
    print(f" P{component}: {operations_info}")
