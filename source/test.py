def bad(the_list=[]):
    the_list.append(10)
    return the_list


r1 = bad()
print(r1)
r2 = bad()
print(r1)
print(r2)
print(r1 is r2)
