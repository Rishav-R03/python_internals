# Exercise one 
import time 
from functools import wraps 
def log_execution(func):
    def wrapper(*args,**kwargs):
        print(f"[START] Executing {func.__name__}")
        func(*args,**kwargs)
        print("[COMPLETED]")
    return wrapper 

@log_execution
def greet(name:str):
    print(f"Hello {name}")

greet("rishav")


def time_it(func):
    def wrapper(*args,**kwargs):
        start = time.perf_counter()
        func(*args,**kwargs)
        end = time.perf_counter()
        elapsed = end - start 
        return elapsed 
    return wrapper


@time_it
def time_test_one(duration):
    time.sleep(duration)

@time_it
def time_test_two(duration):
    time.sleep(duration)

duration1 = time_test_one(3)
print(f"Function one took {duration1:.4f}s to execute")
duration2 = time_test_two(0.5)
print(f"Function two took {duration2:.4f}s to execute")


class Employee:
    name: str 
    role: str 

    def __init__(self,name,role):
        self.name = name 
        self.role = role 



def require_admin(func):
    @wraps(func) # preserves func name and docstring
    def wrapper(*args,**kwargs):
        user = args[0] if args else None 
        if getattr(user,'role',None) == "admin":
            print("Authorized")
            return func(*args,**kwargs)
        else:
            print("Unauthorized - Permision denied")
            return None 
    return wrapper 

@require_admin
def checkPerformance(e:Employee):
    print("Checking performance")


emp1 = Employee("rishav","admin")
checkPerformance(emp1)
emp2 = Employee("rishav","employee")
checkPerformance(emp2)
