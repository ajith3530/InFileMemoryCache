import itertools
# with open("test.txt" ,'r') as write_file:
#     skipped = itertools.islice(write_file ,100 ,None)  # Skip 10 lines, i.e. start at index 10
#     for line in skipped:
#         print("1 - {}".format(line))


# import pickle
# list_1 = [1,2,4,None,5]
# # list_1 = [str(integer) for integer in list_1]
# with open('test.txt', 'wb') as fp:
#     pickle.dump(list_1, fp)
#
# with open ('test.txt', 'rb') as fp:
#     itemlist = pickle.load(fp)
#     pass

list_1 = [1, 2, None,3,4,5]
with open('test.txt', 'w+') as file:
    for item in list_1:
        if item == None:
            item = ""
        file.write("{}\n".format(str(item)))
