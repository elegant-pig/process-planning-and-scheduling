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


# 提取部件、工序、机器和难易度的关系
# 构建字典，表示部件与其工序的关系
component_operation_mapping = {}

# 遍历每一行，构建部件与工序-机器-难易度的关系
for _, row in df.iterrows():
    component = row['部件']
    operation = row['工序']
    machine = row['机器']
    difficulty = row['难易度']

    # 跳过有缺失数据的行
    if pd.isna(component) or pd.isna(operation) or pd.isna(machine) or pd.isna(difficulty):
        print(f"Warning: 跳过了有缺失数据的行: {row}")
        continue

    # 如果字典中还没有该部件，则创建一个新条目
    if component not in component_operation_mapping:
        component_operation_mapping[component] = []

    # 将工序、机器和难易度作为一个字典添加到该部件的列表中
    component_operation_mapping[component].append({
        'operation': operation,
        'machine': machine,
        'difficulty': difficulty
    })

# 打印出构建好的部件关系
for component, operations in component_operation_mapping.items():
    print(f"Component {component}:")
    for op in operations:
        print(f"  Operation {op['operation']} - Machine {op['machine']} - Difficulty {op['difficulty']}")
