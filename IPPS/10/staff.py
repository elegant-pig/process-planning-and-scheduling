import numpy as np


def generate_efficiency_matrices(n, s, y, low=0.5, high=1.5):
    """
    生成n个矩阵，每个矩阵表示每个员工对应s台机器在y个工序的效率。

    参数:
    n: 员工数量
    s: 机器数量
    y: 工序难度等级数量
    low: 效率值的下限
    high: 效率值的上限

    返回:
    efficiency_matrices: 包含n个矩阵的列表，每个矩阵的形状为(s, y)
    """
    efficiency_matrices = [np.random.uniform(low, high, (s, y)) for _ in range(n)]
    return efficiency_matrices


# 示例：生成3个员工，每个员工对应4台机器，针对5个工序的效率
n = 22  # 员工数量
s = 5  # 机器数量
y = 4  # 工序难度等级数量

efficiency_matrices = generate_efficiency_matrices(n, s, y)

# 打印结果
for i, matrix in enumerate(efficiency_matrices):
    print(f"员工 {i + 1} 的效率矩阵：\n{matrix}\n")
