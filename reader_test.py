import numpy as np

def _fetch_text_file_data(filename ,retun_int=False):
    with open(filename) as file:
        data = file.readlines()
    data_string_list = [item.replace("\n" ,"") for item in data]
    if retun_int == True:
        data_int_list = []
        for element in data_string_list:
            element = int(element) if element != "" else None
            data_int_list.append(element)
        return data_int_list
    return data_string_list

data = _fetch_text_file_data("test.txt", retun_int=True)
print(data)
