s = "gfg"

it = iter(s)

print(next(it))
print(next(it))
print(next(it))

# custom iterator 

class EvenNumbers:
    def __init__(self,limit):
        self.limit= limit 
        self.n = 2 

    def __iter__(self):
        return self 

    def __next__(self):
        if self.n > self.limit:
            raise StopIteration
        x = self.n 
        self.n += 2 
        return x 

even = EvenNumbers(10)

for n in even:
    print(n)

