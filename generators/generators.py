def fun(max):
    cnt = 1 
    while cnt <= max:
        yield cnt 
        cnt += 1
ctr = fun(5)
for n in ctr:
    print(n)


sqrs = (x * x for x in range(4))
for sq in list(sqrs):
    print(sq)