import pandas as pd
import string


# 读取 Excel 数据
file_path = '../data/operation_data.xlsx'
operation_data = pd.read_excel(file_path, sheet_name='use')

# def generate_operation_codes():
#     opration_codes=[]
#     tem_data=operation_data[['部件','工序','前继工序']]
#     print(tem_data)
#     for index,row in tem_data.iterrows():
#         part=row['部件']
#         op=row['工序']
#         # before=row['前继工序'].apply(lambda x:len(x.split('、')))
#         before=row['前继工序']
#         # print(type(before))
#         i=part[1:]
#         j=op
#         if pd.isna(before):
#             before=0
#         elif type(before)==int:
#             before=1
#         else:
#             before=len(before.split('、'))
#         # print(before)
#         # operation_code=f"O{i},{j}->{before}"
#         operation_code=f"O{i},{j}->{before}"
#         opration_codes.append(operation_code)
#     # print(opration_codes)
#     return opration_codes

def generate_operation_codes():
    opration_codes=[]
    tem_data=operation_data[['部件','工序']]
    # print(tem_data)
    for index,row in tem_data.iterrows():
        part=row['部件']
        op=row['工序']
        i=part[1:]
        j=op
        # print(before)
        # operation_code=f"O{i},{j}->{before}"
        operation_code=f"O{i},{j}"
        opration_codes.append(operation_code)
    # print(opration_codes)
    return opration_codes

# generate_operation_codes()
