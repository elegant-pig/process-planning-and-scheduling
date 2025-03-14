import math

import pandas as pd

import Crossover
import Mutation
import calculate
import init
import selection
from goal_chart import plot_results

# from goal_chart import plot_makespan_over_iterations, plot_all_metrics_over_iterations

population_size=4 #种群大小
num_workstations=23
piece_num=20 #一共生产多少件
batch=10 #一批次生产多少件
Pr=0.8 #个体选择数
Px=0.4  #变异率
elite_size = round(population_size * Pr / 2) * 2  #确保选择的个体数都是偶数值
file_path = 'data/operation_data.xlsx'
operation_data = pd.read_excel(file_path, sheet_name='final')
data=operation_data.copy()
batch_time = math.ceil(piece_num / batch)  # 一共生产多少批次
max_iterations=3 #迭代次数

def main():
    global_best_solution = None  # 存储全局最佳解
    best_fitness = float('-inf')  # 或使用负无穷来初始化最差的适应度
    each_best_result=[] #记录每代的最有个体的适应度
    global_best_values = []  # 记录全局最优适应度变化
    each_solution=None
    each_current_best_solution=None
    # 初始化种群
    #返回：population,result_constraint
    population,_=init.initialize_population(data,population_size,num_workstations)

    # 计算初始化种群的适应度，并记录最优个体
    solution, current_best_solution = calculate.calculate(population, batch_time, num_workstations)
    each_best_result.append(current_best_solution['fitness'])

    # 设置全局最优解
    global_best_solution = current_best_solution
    global_best_values.append(global_best_solution['fitness'])


    tem=[]
    for generation in range(max_iterations):
        print(f"flagflag")
        print(f"第{generation+1}次迭代")
        solution, current_best_solution = calculate.calculate(population, batch_time, num_workstations)
        each_best_result.append(current_best_solution)

        # 更新全局最优解
        if current_best_solution['fitness'] > global_best_solution['fitness']:
            global_best_solution = current_best_solution

        # if global_best_solution is None or global_best_solution['fitness']<current_best_solution['fitness']:
        #     # 更新全局最佳解
        #     global_best_solution = current_best_solution

        global_best_values.append(global_best_solution)

        # 选择进入迭代的父代，选择的都是偶数
        parents=selection.elitism_selection(solution,elite_size)

        # 进行交叉
        Child,old_best=Crossover.crossover_choose_parent(parents)

        # 进行变异
        mutation_child=Mutation.mutate(Child,Px)

        # **更新种群**：加入变异后的个体 + 之前的全局最优个体
        population = mutation_child

        # 确保全局最优解不丢失
        if global_best_solution['individual'] not in population:
            population.append(global_best_solution['individual'])

        # # **保持种群大小一致**，如果超出 `population_size`，移除适应度最低的个体
        # if len(population) > population_size:
        #     population = sorted(population, key=lambda x: x['fitness'], reverse=True)[:population_size]

        # 判断停止条件
        if generation >= max_iterations:
            print("达到了最大迭代次数，停止算法")
            break

        # === 提取用于绘图的数据 ===
    makespan_values = [x['makespan'] for x in each_best_result]
    workload_values = [x['workload'] for x in each_best_result]
    total_free_time_values = [x['total_free_time'] for x in each_best_result]

    # === 调用绘图函数 ===
    plot_results(makespan_values, workload_values, total_free_time_values)


# 只有当脚本作为主程序运行时，才会执行以下代码
if __name__ == "__main__":
    main()