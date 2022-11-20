def missing_value():
    test_list = [1, 3, 5, 6, 3, 5, 6, 1]
    res = []
    [res.append(x) for x in test_list if x not in res]
    return str(res)

def map_status_and_stage(n):
    return n.status()

def map_data_types(): 

updated_list = map(mapStatusAndStage, companies)
print(updated_list)
print(list(updated_list))
