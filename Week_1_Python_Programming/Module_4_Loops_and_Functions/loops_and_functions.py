#! /bin/python3
#While Loop
def while_loop():
    print("While Loop Example:")
    i = 1
    while i <= 5:
        print(i)
        i = i + 1
    print()
#For Loop
def for_loop():
    print("For Loop Example:")
    for i in range(1, 6):
        print(i)
    print()
    fruits = ["apple", "banana", "cherry"]
    print("Fruits List:")
    for fruit in fruits:
        print(fruit)
    print()
#Greet Someone
def greet(name="Guest"):
    print(f"Hello, {name}!")
    print()

def add(a, b):
    return a + b

def calculate(a, b):
    sum_result = a + b
    diff_result = a - b
    return sum_result, diff_result

def print_numbers(n):
    print(f"Printing numbers from 1 to {n}:")
    for i in range(1, n+1):
        print(i)
    print()

def greet_default(name="World"):
    print(f"Hello, {name}!")
    print()

def sum_and_difference(a, b):
    return a + b, a - b
# Main Function
def main():
    while_loop()
    for_loop()
    greet_default("Alice")
    greet_default()
    result = add(5, 7)
    print(f"Addition Result: {result}")
    print()
    sum_val, diff_val = calculate(10, 3)
    print(f"Sum: {sum_val}, Difference: {diff_val}")
    print()
    print_numbers(5)
    greet_default("Bob")
    greet_default()
    sum_result, diff_result = sum_and_difference(15, 5)
    print(f"Sum: {sum_result}, Difference: {diff_result}")
    print()

if __name__ == "__main__":
    main()

