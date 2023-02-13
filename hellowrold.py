import random

# used to randomize lists.

"""
age1 = 2-11
age2 = 12-17
age3 = 18-34
age4 = 35-49
age5 = 50-64
age6 = 65+
"""

# Each list contains the number hours hours in a week, rounded up,
# that a person in this age group spends on certain internet activities
# The activities follow the list in D4
age1 = [12, 3, 8, 0, 0, 0, 0, 0, 0, 0, 0]
age2 = [8, 5, 5, 0, 0, 0, 0, 0, 0, 0, 0]
age3 = [12, 4, 7, 4, 2, 30, 3, 2, 6, 1, 1]
age4 = [24, 2, 7, 5, 2, 31, 3, 1, 8, 2, 1]
age5 = [41, 1, 5, 6, 2, 26, 2, 1, 8, 1, 1]
age6 = [51, 1, 4, 4, 1, 20, 1, 1, 8, 1, 1]

# This list contains the bandwidth required for the activities in the above list.
# Each number corresponds to the activity represented in the above lists.
bandwidth = [0, 3, 25, 1, 5, 1, 5, 1, 1, 5, 1]


# This function takes a list and returns a new list with all the same elements,
# but in a random order.
def randomize(list1):
    l = []
    while len(list1) > 0:
        l.append(list1.pop(random.randint(0, len(list1) - 1)))
    return l


# This function inputs an arbitrary number of lists of the same length and
# returns a new list in which each element is the sum of the corresponding
# elements in the input lists.
def add_hours(*argv):
    l = []
    a = 0
    for i in range(len(argv[0])):
        for n in range(len(argv)):
            a += argv[n][i]
        l.append(a)
        a \
            = 0
    return l


# This function generates a list of size 126 with that follows the frequencies
# of different activities.
def gen_age(age):
    global bandwidth
    l = []
    for i in range(len(age)):
        for n in range(age[i]):
            l.append(bandwidth[i])
    while len(l) < 126:
        l.append(0)
    return l


# This function calls both the gen_age function and randomize function and
# returns the result.
def generator(age):
    l = gen_age(age)
    r = randomize(l)
    return r

def main():

   print(add_hours(age1, age2))

main()
