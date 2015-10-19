import MapReduce
import sys

# Part 1
mr = MapReduce.MapReduce()

# Part 2
def mapper(record):
    # key: document identifier
    # value: document contents
    key = record[0]
    value = record[1]
    words = set(value.split())
    for w in words:
      mr.emit_intermediate(w, key)

# Part 3
def reducer(key, list_of_doc):
    # key: word
    # value: list of occurrence counts
    list_of_doc = list(set(list_of_doc))
    mr.emit((key, list_of_doc))

# Part 4
inputdata = open(sys.argv[1])
mr.execute(inputdata, mapper, reducer)

