import numpy as np
import pandas as pd
import os
import re

input_file_path = r'E:\file_path\out-data-test'
output_file_path = r'E:\file_path\out-txt-test'
# os.mkdir(output_file_path)
input_file_list = os.listdir(input_file_path)

txt_path_format = r'E:\file_path\out-txt-test\{}'
txt_name_format = r'{}'
txt_path_name = []
txt_out_name = []
file_list = [] # 所有data名字合集
re_form = re.compile(r'structure+\d+\.+data$')
for i in input_file_list:
    file_list += re_form.findall(i)

data_file_po = [] # 所有data位置合集
data_path_format = r'E:\file_path\out-data-test\{}'
for j in list(range(len(file_list))):
    data_file_po.append(data_path_format.format(file_list[j]))
    txt_path_name.append(txt_path_format.format('structure' + str(j+1).zfill(5) + '.txt'))
    txt_out_name.append(txt_name_format.format('structure' + str(j+1).zfill(5) + '.txt'))

os.chdir(output_file_path)
column = []
column_name = r'{}'
for n in list(range(len(data_file_po))):
    column.append(column_name.format('Data' + str(n+1).zfill(5)))
length = []
coord = []
coord_np = []
coord_del = []
coord_del_list = []
coord_del_list_new = []
coord_del_list_np = []
coord_del_list_np_shape = []
coord_del_list_np_shape_del = []
coord_del_list_np_shape_del_shape = []
# for k in list(range(len(file_list))): # 最后再去掉注释
#     length.append(len(open(data_file_po[k]).readlines()))
with open(data_file_po[5]) as f: # 最后改0为i
    lines = f.readlines()
    for line in lines:
        coord.append(re.split(r'\s+', line))
    # print(coord)
    coord_np = np.array(coord, dtype=object)
    coord_del = np.delete(coord_np, slice(0, 17))  # 只留坐标，一行则[]指定要删的列指标；slice更便利

    # #== method 1 ==#
    # coord_del_list = coord_del.tolist()  # 转为list来删除前两列
    # for l in list(range(len(coord_del_list))):
    #     del coord_del_list[l][0:2]
    #     del coord_del_list[l][3]
    # coord_del_list_np = np.array(coord_del_list)
    # coord_pd = pd.DataFrame(
    #     # data=coord_del_list_np_shape_del_shape,
    #     data=coord_del_list_np,
    #     columns=[column[5], column[5], column[5]])  # 最后改为i
    # coord_pd_T = coord_pd.T  # 变为txt里边内容的形式
    # coord_pd_T.to_csv('test1.txt', sep='\t', index=True, header=False, mode='a')  # index行索引，header列索引
    # #==============#

    #== method 2 ==#
    coord_del_list = coord_del.tolist()
    # coord_del_list = coord_del.reshape(-1, 1)  # 一行变为一列
    coord_del_list_np = np.delete(coord_del_list, slice(0,2), axis=1)
    coord_del_list_new = np.delete(coord_del_list_np, 3, axis=1)
    coord_pd = pd.DataFrame(
        data=coord_del_list_new,
        columns=[column[5], column[5], column[5]])  # 最后改为i
    coord_pd_T = coord_pd.T  # 变为txt里边内容的形式
    coord_pd_T.to_csv('test2.txt', sep='\t', index=True, header=False, mode='a')  # index行索引，header列索引
    #==============#

    # #== method 3 ==#
    # coord_del_list = coord_del.tolist()
    # coord_del_list_new = np.delete(coord_del_list, slice(0, 2), axis=1)
    # coord_del_list_np_shape = coord_del_list_new.reshape(len(coord_del_list_new), 4)
    # coord_del_list_np_shape_del = np.delete(coord_del_list_np_shape, -1, axis=1)
    # coord_del_list_np_shape_del_shape = coord_del_list_np_shape_del.reshape(len(coord_del_list_new), 3)
    # coord_pd = pd.DataFrame(
    #     data=coord_del_list_np_shape_del_shape,
    #     columns=[column[5], column[5], column[5]])  # 最后改为i
    # coord_pd_T = coord_pd.T  # 变为txt里边内容的形式
    # coord_pd_T.to_csv('test3.txt', sep='\t', index=True, header=False, mode='a')  # index行索引，header列索引
    # #==============#

    # #== method 4 ==#
    # indices_to_remove = [0,1,5]
    # coord_del_list_new = np.array([np.delete(col, indices_to_remove) for col in coord_del.T]).T
    # coord_del_list_new_T = coord_del_list_new.T
    # coord_pd = pd.DataFrame(
    #     data=coord_del_list_new_T,
    #     columns=[column[5], column[5], column[5]])  # 最后改为i
    # coord_pd_T = coord_pd.T  # 变为txt里边内容的形式
    # coord_pd_T.to_csv('test4.txt', sep='\t', index=True, header=False, mode='a')  # index行索引，header列索引
    # #==============#

f.close()
