# import matplotlib.pyplot as plt
# import pandas as pd
# import random
# import matplotlib
# import os
#
# # # 自己的电脑环境
# # os.environ['TCL_LIBRARY'] = r'D:\Users\tanin\AppData\Local\Programs\Python\Python310\tcl\tcl8.6'
# # os.environ['TK_LIBRARY'] = r'D:\Users\tanin\AppData\Local\Programs\Python\Python310\tcl\tk8.6'
#
# # 实验室电脑环境
# os.environ['TCL_LIBRARY'] = r'C:\Users\elegant_pigg\AppData\Local\Programs\Python\Python313\tcl\tcl8.6'
# os.environ['TK_LIBRARY'] = r'C:\Users\elegant_pigg\AppData\Local\Programs\Python\Python313\tcl\tk8.6'
#
# # import matplotlib.pyplot as plt
# matplotlib.use('TkAgg')  # 设置后端为 TkAgg，兼容大多数环境
#
# # 定义绘图函数
# def plot_gantt_chart(workstation_available_time):
#     # 准备数据
#     data = []
#     for workstation, details in workstation_available_time.items():
#         for job in details['assigned_jobs']:
#             data.append({
#                 'Workstation': workstation,
#                 'Batch': job['batch'],
#                 'Operation': job['operation'],
#                 'Start': job['start_time'],
#                 'End': job['end_time']
#             })
#
#     df = pd.DataFrame(data)
#
#     # 生成颜色映射，每个批次一种颜色
#     unique_batches = df['Batch'].unique()
#     colors = {batch: f'#{random.randint(0, 0xFFFFFF):06x}' for batch in unique_batches}
#
#     # 创建子图，自动计算需要的行列数
#     num_workstations = len(df['Workstation'].unique())
#     num_columns = 3  # 每行显示3个子图
#     num_rows = (num_workstations // num_columns) + (1 if num_workstations % num_columns != 0 else 0)
#
#     fig, axes = plt.subplots(num_rows, num_columns, figsize=(15, 5 * num_rows))
#
#     # 如果是单行或单列，axes的形状可能是1维数组，调整为2维数组处理
#     axes = axes.flatten()
#
#     # 按工作站分配不同的图表
#     for idx, workstation in enumerate(df['Workstation'].unique()):
#         ax = axes[idx]  # 获取当前工作站的子图
#         workstation_data = df[df['Workstation'] == workstation]
#
#         for _, row in workstation_data.iterrows():
#             batch = row['Batch']
#             operation = row['Operation']
#
#             # 提取工序编号的 y 部分（例如 'O1,1' 提取 '1'）
#             operation_y = operation.split(',')[1]  # 获取工序编号（'y' 部分）
#
#             color = colors[row['Batch']]
#             ax.barh(
#                 row['Workstation'],
#                 row['End'] - row['Start'],
#                 left=row['Start'],
#                 height=0.8,
#                 color=color,
#                 edgecolor='black'
#             )
#             # 在条形图中间标注工序编号
#             ax.text(
#                 x=(row['Start'] + row['End']) / 2,
#                 y=row['Workstation'],
#                 s=operation_y,
#                 ha='center',
#                 va='center',
#                 color='white',
#                 fontsize=9,
#                 fontweight='bold'
#             )
#
#         ax.set_xlabel('Time (in seconds)')
#         ax.set_ylabel('Workstation')
#         ax.set_title(f'Gantt Chart for {workstation}')
#
#     # 如果子图的数量不够，隐藏空的子图
#     for i in range(num_workstations, len(axes)):
#         axes[i].axis('off')
#
#     # 自动调整布局
#     plt.tight_layout()
#     plt.show()
#
# # 模拟的工作站和工序数据
# workstation_available_time = {
#     'L1': {'assigned_jobs': [{'batch': 1, 'operation': 'O1,1', 'start_time': 0, 'end_time': 10},
#                               {'batch': 2, 'operation': 'O2,1', 'start_time': 10, 'end_time': 20}]},
#     'L2': {'assigned_jobs': [{'batch': 1, 'operation': 'O1,2', 'start_time': 0, 'end_time': 15},
#                               {'batch': 2, 'operation': 'O2,2', 'start_time': 15, 'end_time': 25}]},
#     'L3': {'assigned_jobs': [{'batch': 1, 'operation': 'O1,3', 'start_time': 5, 'end_time': 20}]},
#     'L4': {'assigned_jobs': [{'batch': 2, 'operation': 'O2,4', 'start_time': 0, 'end_time': 12}]}
# }
#
# # 调用绘图函数
# # plot_gantt_chart(workstation_available_time)
