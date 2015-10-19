import MapReduce
import sys

# Part 1: create MapReduce object
mr = MapReduce.MapReduce()

# Part 2: 
def mapper(name):
    # key: name
    # value: friend name
    mr.emit_intermediate(name[0], name[1])

# Part 3: calculate friend count
def reducer(person, friend_list):
    mr.emit((person, len(friend_list)))


# Part 4
inputdata = open(sys.argv[1])
mr.execute(inputdata, mapper, reducer)