import MapReduce
import sys

# Part 1: create MapReduce object
mr = MapReduce.MapReduce()

# Part 2: emit word:document_id pairs avoiding duplicates
def mapper(order):
    # key: table identifier (line_item/order), not explicitly used
    # order_id: record id (for matching)
    order_id = order[1]
    mr.emit_intermediate(order_id, order)

# Part 3: remove duplicates from list_of_ids and emit it
def reducer(order_id, record_list):
    # order_id: record id
    # value: list of records (lists)

    # remove order table
    for record in record_list:
        if record[0] == "order":
            order_record = record
            break
    record_list.remove(order_record)

    # emit order_record + other record for each record remaining 
    for record in record_list:
        mr.emit(order_record + record)

# Part 4
inputdata = open(sys.argv[1])
mr.execute(inputdata, mapper, reducer)