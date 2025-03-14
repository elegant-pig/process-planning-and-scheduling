import math

import pandas as pd
from gurobipy import Model, GRB,quicksum
# 读取 Excel 文件
file_path = '../data/data.xlsx'  # 请替换为你的 Excel 文件路径
df = pd.read_excel(file_path)

# 显示读取的数据
# print(df)

# 初始化 Gurobi 模型
model = Model('ProductionScheduling')
# 提取关键信息
batch_size=10 #每批次工件数
produceNum=123 #生产总数
components = df['部件'].unique()  # 部件列表
operations = df['工序'].unique()   # 工序列表
machines = df['机器'].unique()
workstations=22
employees =22  # 假设有 4 名员工，依据实际情况调整
# 创建批次列表
# 计算总批次数
num_batches = (produceNum + batch_size - 1) // batch_size
batches = [batch_size] * (num_batches - 1) + [produceNum % batch_size or batch_size]

# 创建变量
# 定义变量
# X[b, s , w, p]：批次 b 的部件 p 上的工序 s 被分配给工作站 w
X = model.addVars(batches, operations, workstations, components, vtype=GRB.BINARY, name='X')

# N[b, s , w, p]：批次 b 的部件 p 上的工序 s 的下一工序被分配到邻近工作站
N = model.addVars(batches, operations, workstations, components, vtype=GRB.BINARY, name='N')

# Y[e, w]：员工 e 分配到工作站 w
Y = model.addVars(employees, workstations, vtype=GRB.BINARY, name='Y')

# Z[m, w]：机器 m 分配到工作站 w
Z = model.addVars(machines, workstations, vtype=GRB.BINARY, name='Z')



# D[s, p]：部件 p 的工序 s 的难易程度
D = model.addVars(operations, components, vtype=GRB.CONTINUOUS, name='D')

# E[e, m, s]：员工 e 在机器 m 上操作工序 s 的效率
E = model.addVars(employees, machines, operations, vtype=GRB.CONTINUOUS, lb=0.1, ub=1.5, name='E')

# ST[b, sp]：批次 b 的部件 p 的工序 s 的开始时间
ST = model.addVars(batches, operations, components, vtype=GRB.CONTINUOUS, name='ST')

# CT[b, s , p]：批次 b 的部件 p 的工序 s 的完工时间
CT = model.addVars(batches, operations, components, vtype=GRB.CONTINUOUS, name='CT')

# Process[b, s , p]：批次 b 的部件 p 的工序 s 的加工时间
Process = model.addVars(batches, operations, components, vtype=GRB.CONTINUOUS, name='Process')

# SAM[s]：工序 s 的标准时间
SAM = model.addVars(operations, vtype=GRB.CONTINUOUS, name='SAM')

# 约束 1: 一个工作站只能分配一台机器和一名员工
for w in range(1, NW + 1):
    model.addConstr(quicksum(Z[m, w] for m in machines) == 1, name=f'Machine_Constraint_Workstation_{w}')
    model.addConstr(quicksum(Y[e, w] for e in employees) == 1, name=f'Employee_Constraint_Workstation_{w}')

# 约束 2: 一个加工批次只能被加工一次
for b in range(batches):
    for p in components:
        model.addConstr(quicksum(X[b, s, w, p] for w in range(1, NW + 1) for s in operations) == 1, name=f'Batch_Processing_Once_{b}_{p}')

# 约束 3: 同一工作站上，一个加工批次的部件的工序在另一个批次开始前完成
for b in range(batches):
    for b_prime in range(batches):
        for p in components:
            for s in operations:
                for s_prime in operations:
                    model.addConstr(CT[b, s, p] <= ST[b_prime, s_prime, p], name=f'Batch_Completion_Precedence_{b}_{s}_{p}_{b_prime}_{s_prime}')

# 约束 4: 同一加工批次中的工序i如果要在工序j之前完成
for b in range(batches):
    for p in components:
        for s_i in operations:
            for s_j in operations:
                if s_i < s_j:  # 假设工序的顺序有一定关系
                    model.addConstr(CT[b, s_i, p] <= ST[b, s_j, p], name=f'Sequence_Precedence_{b}_{s_i}_{p}_{s_j}')

# 约束 5: 同一时刻，一个工作站的员工和机器只能执行一道工序
for w in range(1, NW + 1):
    for e in employees:
        for m in machines:
            model.addConstr(
                quicksum(X[b, s, w, p] * Y[e, w] * Z[m, w]
                         for b in range(batches)
                         for p in components
                         for s in operations) <= 1,
                name=f'Workstation_Employee_Machine_Constraint_{w}_{e}_{m}'
            )

# 模型求解
model.optimize()

# 输出结果
if model.status == GRB.OPTIMAL:
    for b in range(batches):
        for p in components:
            for w in range(1, NW + 1):
                for s in operations:
                    if X[b, s, w, p].X > 0.5:  # 如果变量的值为1
                        print(f'批次 {b} 的部件 {p} 的工序 {s} 被分配给工作站 {w}')