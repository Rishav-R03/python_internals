def decorator_one(func):
    def wrapper():
        print("Before main\n")
        func()
        print("After main\n")
    return wrapper

# decorator 2 with parameters 

def decorator_with_param(func):
    def wrapper(*args,**kwargs):
        print("Before execution")
        result = func(*args,**kwargs)
        print("After execution")
        return result 
    return wrapper

@decorator_one
def main_func():
    print("Hello\n")

@decorator_with_param
def add(a,b):
    return a + b 


main_func()
result = add(5,6)
print(result)

#_____Functions as first class objects____ 
# assigning func to a variable
def greet(name:str)->str:
    return f"Hello {name}"

message = greet("rishav")
print(message) 

# passing function as a parameter
def apply(f, v:str)->str:
    return f(v)

new_message = apply(greet,"rishav")
print(new_message)

# returning function from another function 
def make_multi(f):
    def wrapper(x):
        return x * f 
    return wrapper

dbl = make_multi(2)
print(type(dbl))
print(dbl(5))


# Higher order functions 
def func(f,x):
    return f(x)

def square(x):
    return x * x 

print(func(square,4))


def method_decorator(func):
    def wrapper(self,*args,**kwargs):
        print("Before method execution")
        res = func(self,*args,**kwargs)
        print("After method execution")
        return res 
    return wrapper

class Solution:
    @method_decorator
    def say_hello(self):
        print("Hello")

ob = Solution()
ob.say_hello()


def even_decorator(func):
    def wrapper(*args,**kwargs):
        res = func(*args,**kwargs)
        if res % 2 == 0:
            return res
        return res + 1
    return wrapper 

@even_decorator
def user_input(num:int)->int:
    return num

res = user_input(6)
print(res) 


# Class decorator 
def func(cls):
    cls.class_name = cls.__name__
    return cls 

@func 
class Person:
    pass 
print(Person.class_name)

# built in decorators 

class MathOperations:
    @staticmethod 
    def add(x,y):
        return x + y

res = MathOperations.add(5,4)
print(res)

class Employee:
    raise_amount_percent = 10
    def __init__(self,name,salary):
        self.name = name 
        self.salary = salary 

    @classmethod 
    def set_raise_amount(cls,amount):
        cls.raise_amount_percent = amount 

Employee.set_raise_amount(11)
print(Employee.raise_amount_percent)

# property 

class Circle:
    def __init__(self,radius):
        self._radius = radius 
    @property 
    def radius(self):
        return self._radius 

    @radius.setter 
    def radius(self,value):
        if value >= 0:
            self._radisu = value 
        else:
            raise ValueError("Radius cannot be negative")

    @property
    def area(self):
        return 3.14 * (self._radius**2)

c = Circle(5)
print(c.radius)
print(c.area)
