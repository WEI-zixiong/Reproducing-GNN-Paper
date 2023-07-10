import os
import re
import pandas as pd
def edge(file_order, input_file_path, output_file_path):
    # structure_file = r'E:\file\python-code\GNN\reshow\3-feed_GNN\structure00001.data'
    coord = []  # stores coordinates
    file_list = [] # stores the name of all structure.data
    data_file_po = [] # stores the name of the path of all structure.data
    file_column = [] # stores the name of every row
    data_path_format = input_file_path + '\{}'
    column_name = r'{}' # for pd DataFrame
    input_file_list = os.listdir(input_file_path)
    re_form = re.compile(r'structure+\d+\.+data$')
    for m in input_file_list:
        file_list += re_form.findall(m)
    for n in list(range(len(file_list))):
        data_file_po.append(data_path_format.format(file_list[n]))
    os.chdir(output_file_path)
    for o in list(range(len(data_file_po))):
        file_column.append(column_name.format('Data' + str(o + 1).zfill(5)))
    with open(data_file_po[file_order], 'r') as f:
        lines = f.readlines()
    # with open(structure_file, 'r') as stru:
    #     lines = stru.readlines()
        for a, line in enumerate(lines):
            if a > 16:
                coord.append(line)
    # stru.close()
    cut_off = 3.2
    distance_save = [] # stores all the distances
    row = [] # atom IDs of centered atom
    column = [] # atom IDs within cutoff radius
    for i in range(len(coord)):
        coord_split_i = coord[i].split()
        atom_i = coord_split_i[0]
        row.append(atom_i)
        for j in range(len(coord)):
            coord_split_j = coord[j].split()
            atom_j = coord_split_j[0]
            distance = ((float(coord_split_i[2]) - float(coord_split_j[2])) ** 2 +
                        (float(coord_split_i[3]) - float(coord_split_j[3])) ** 2 +
                        (float(coord_split_i[4]) - float(coord_split_j[4])) ** 2) ** 0.5
            # print(j)
            distance_save.append(distance)
            if 0 < distance <= cut_off:
                column.append(atom_j)
        column.append('\n')
    numbers = {} # store the atom IDs within cutoff
    current_list = [] # dynamic list for atom IDs
    for item in column:
        if item == '\n':
            # Create a new list for each '\n'
            if current_list:
                numbers[len(numbers) + 1] = current_list
                current_list = []
        else:
            # Extract the numbers and append to the current list
            if item.isdigit():
                current_list.append(item)
    # Add the last list to numbers if it exists
    if current_list:
        numbers[len(numbers) + 1] = current_list
    # print(numbers)
    # print(len(numbers.get(2)))
    #===========pd method=============# need further operations
    # df = pd.DataFrame.from_dict(numbers, orient='index')
    # df.columns = ['cutoff'] * len(df.columns)
    # # df.columns = [f'cutoff_{i}' for i in range(len(df.columns))]  # Assign unique column names
    # # for i in range(len(row)):
    # #     df.iloc[i] = df.iloc[i].dropna().reindex(df.columns)
    # # Concatenate all the rows into a single row
    # concat_row = pd.concat([df[col] for col in df.columns], axis= 0)
    # concat_df = pd.DataFrame([concat_row.values.tolist()], columns=[f'col_{i}' for i in range(len(concat_row))])
    # concat_df.to_csv('test.txt', sep='\t', index=True, header=False, mode='w')
    # # regex = re.compile('\d+')
    # # digit = []
    # # with open('test.txt', 'r+') as txt:
    # #     lines_txt = txt.readlines()
    # #     for j, line_j in enumerate(lines_txt):
    # #         txt_split = line_j.split()
    # #         print(txt_split[3])
    # #         digit.append(regex.findall(line_j))
    #==============old school way==============#
    cut_off_atoms = [] # stores atom IDs
    add_center = [] # repeat centered atom IDs
    for k in range(len(row)):
        element = numbers.get(k+1)
        if element is not None:
            cut_off_atoms.append(element)
        # print(len(numbers.get(k+1)))
            for l in range(len(numbers.get(k+1))):
                add_center.append(str(row[k]))
    # flat cut_off_atoms list
    flat_list = [item for sublist in cut_off_atoms for item in sublist]
    # put together add_center and cut_off_atoms
    two_rows = [list(row) for row in zip(add_center, flat_list)]
    df = pd.DataFrame(two_rows, columns=[file_column[file_order], file_column[file_order]])
    df = df.T
    output_file = os.path.join(output_file_path, 'test3.txt')
    df.to_csv(output_file, sep='\t', index=True, header=False, mode='a')
    f.close()
    return print('finished')

input_file_path = r'E:\file\python-code\GNN\reshow\3-feed_GNN\test_input_file'
output_file_path = r'E:\file\python-code\GNN\reshow\3-feed_GNN'
for b in range(10):
    edge(b, input_file_path, output_file_path)
