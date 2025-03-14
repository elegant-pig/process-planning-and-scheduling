

def adjust_individual(individual):
    total_balance=0
    for num in individual['individual']['balance_code']:
        total_balance+=num
    print(total_balance)
    # if total_balance<23:
    #
    # else:
