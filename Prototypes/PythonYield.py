#ITERABLES (values stored in memory)
myList = [1,2,3]
for i in myList:
    print(i)
print('-----------------------------')

#GENERATORS (values on the fly)
myGenerator = (x*x for x in range(3))
for i in myGenerator:
    print(i)
print('-----------------------------')

#YIELD (like return except returns a generator)
def create_generator():
    myList = range(3)
    for i in myList:
        yield i*i

mygenerator = create_generator()
print(mygenerator)
for i in mygenerator:
    print(i)

#handy when the function will return a huge set of values that will only be read once
print('-----------------------------')
