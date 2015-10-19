import MapReduce
import sys


mr = MapReduce.MapReduce()


def mapper(entry):
    matrix_id = entry[0]
    value = entry[3]
    if matrix_id == "a":
        row = entry[1]
        order = entry[2]
        for col in range(5):
            mr.emit_intermediate((row, col), (order, value))
    else:
        col = entry[2]
        order = entry[1]
        for row in range(5):
            mr.emit_intermediate((row, col), (order, value))

def reducer(index, value_list):
    step_list = [[] for i in range(5)]
    
    for order, value in value_list:
        step_list[order].append(value)
    
    result = 0  ## initiate sum of products
    for step in step_list:
        if len(step) == 2:
            result += step[0] * step[1]
    if result != 0:   ## to preserve advantage of sparcity
        mr.emit((index[0], index[1], result))
        

inputdata = open(sys.argv[1])
mr.execute(inputdata, mapper, reducer)