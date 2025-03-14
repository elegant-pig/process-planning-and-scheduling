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
# workstations=22 #假设有22个工作站
# employees =22  # 假设有 22 名员工
employees=(['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o'])
workstations=['w1','w2','w3','w4','w5','w6','w7','w8','w9','w10','w11','w12','w13','w14','w15']
# 创建批次列表
# 计算总批次数
num_batches = (produceNum + batch_size - 1) // batch_size
batches = [batch_size] * (num_batches - 1) + [produceNum % batch_size or batch_size]
batch=list(range(num_batches))
print(components)
print(operations)
print(machines)
# print(list(range(workstations)))
# print(list(range(employees)))
print(batch)
print(batches)

# 创建变量
# 定义变量
# X[b, s , w, p]：批次 b 的部件 p 上的工序 s 被分配给工作站 w
X = model.addVars(batch, operations, workstations, components, vtype=GRB.BINARY, name='X')

# N[b, s , w, p]：批次 b 的部件 p 上的工序 s 的下一工序被分配到邻近工作站
N = model.addVars(batch, operations, workstations, components, vtype=GRB.BINARY, name='N')

# Y[e, w]：员工 e 分配到工作站 w
Y = model.addVars(employees, workstations, vtype=GRB.BINARY, name='Y')

# Z[m, w]：机器 m 分配到工作站 w
Z = model.addVars(machines, workstations, vtype=GRB.BINARY, name='Z')

# D[s, p]：部件 p 的工序 s 的难易程度
D = model.addVars(operations, components, vtype=GRB.CONTINUOUS, name='D')

# E[e, m, s]：员工 e 在机器 m 上操作工序 s 的效率
E = model.addVars(employees, machines, operations, vtype=GRB.CONTINUOUS, lb=0.1, ub=1.5, name='E')

# ST[b, sp]：批次 b 的部件 p 的工序 s 的开始时间
ST = model.addVars(batch, operations, components, vtype=GRB.CONTINUOUS, name='ST')

# CT[b, s , p]：批次 b 的部件 p 的工序 s 的完工时间
CT = model.addVars(batch, operations, components, vtype=GRB.CONTINUOUS, name='CT')

I = model.addVars(batch, operations, workstations, components, employees, machines, vtype=GRB.BINARY, name='I')


# Process[b, s , p]：批次 b 的部件 p 的工序 s 的加工时间
Process = model.addVars(batch, operations, components, vtype=GRB.CONTINUOUS, name='Process')

# SAM[s]：工序 s 的标准时间
SAM = model.addVars(operations, vtype=GRB.CONTINUOUS, name='SAM')

# 约束 1：一个工作站只能分配一台机器
model.addConstrs((quicksum(Z[m, w] for m in machines) == 1 for w in workstations), name="OneMachinePerStation")

# 约束 2：一个工作站只能分配一名员工
model.addConstrs((quicksum(Y[e, w] for e in employees) == 1 for w in workstations), name="OneEmployeePerStation")

# 约束 3：一个加工批次只能被加工一次
model.addConstrs((quicksum(X[b, s, w, p] for w in workstations) == 1 for b in batch for s in operations for p in components), name="OneProcessingPerBatch")

# 约束 4：当前批次的工序完成后才能开始下一个批次的相同工序
model.addConstrs((CT[b, s, p] <= ST[b_prime, s, p]
                 for b in batch for s in operations for p in components
                 for b_prime in batch if b != b_prime), name="ProcessingOrder")

# 约束 5：工序 i 必须在工序 j 之前完成
model.addConstrs((CT[b, s_i, p] <= ST[b, s_j, p]
                 for b in batch for p in components
                 for s_i, s_j in zip(operations[:-1], operations[1:])), name="OperationOrder")


# 约束 6：线性化约束
# 将变量 X、Y 和 Z 之间的乘积转化为新的二进制变量 I，并添加约束来确保它的线性化逻辑
model.addConstrs((I[b, s, w, p, e, m] <= X[b, s, w, p] for b in batch for s in operations for w in workstations for p in components for e in employees for m in machines), name="Lin1")
model.addConstrs((I[b, s, w, p, e, m] <= Y[e, w] for b in batch for s in operations for w in workstations for p in components for e in employees for m in machines), name="Lin2")
model.addConstrs((I[b, s, w, p, e, m] <= Z[m, w] for b in batch for s in operations for w in workstations for p in components for e in employees for m in machines), name="Lin3")
model.addConstrs((I[b, s, w, p, e, m] >= X[b, s, w, p] + Y[e, w] + Z[m, w] - 2
                 for b in batch for s in operations for w in workstations for p in components for e in employees for m in machines), name="Lin4")

# 约束 7：同一时刻一个工作站只能执行一道工序
model.addConstrs((quicksum(I[b, s, w, p, e, m] for b in batch for p in components for s in operations for e in employees for m in machines) <= 1
                 for w in workstations), name="OneOperationPerStationAtATime")

# 添加一个简单的目标函数，例如最小化最大完工时间
makespan = model.addVar(vtype=GRB.CONTINUOUS, name='makespan')

# 确保 makespan 是所有工序完工时间的最大值
model.addConstrs((makespan >= CT[b, s, p] for b in batch for s in operations for p in components), name="MaxCompletionTime")

# 设定目标函数，最小化最大完工时间
model.setObjective(makespan, GRB.MINIMIZE)

# 优化模型
model.optimize()

# 输出结果
if model.status == GRB.OPTIMAL:
    print("Optimal solution found.")
    for v in model.getVars():
        print(f'{v.varName}: {v.x}')
else:
    print("No optimal solution found.")