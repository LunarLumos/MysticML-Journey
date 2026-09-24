#! /bin/python3
import os

#Taking Input File name
def file_handling_example():
    filename = input("Enter the file name: ")

    # Writing to a file
    with open(filename, "w") as file:
        file.write("Hello, Python!\n")
        file.write("This is a sample file.\n")

    # Reading the file
    with open(filename, "r") as file:
        print("File Content:")
        print(file.read())

    # Modifying the file
    with open(filename, "a") as file:
        file.write("Appending new content.\n")

    # Read modified file
    with open(filename, "r") as file:
        print("Modified File Content:")
        print(file.read())

    # Deleting the file
    os.remove(filename)
    print(f"{filename} has been deleted.\n")

# List Comprehension
def list_comprehension_example():
    numbers = [1, 2, 3, 4, 5]
    squared_numbers = [x**2 for x in numbers]
    print(f"Squared numbers: {squared_numbers}")

# Set
def set_comprehension_example():
    numbers = [1, 2, 3, 4, 5, 5, 6]
    unique_squared_numbers = {x**2 for x in numbers}
    print(f"Unique squared numbers: {unique_squared_numbers}")

# Lambda Function
def lambda_example():
    add = lambda x, y: x + y
    multiply = lambda x, y: x * y

    print(f"Sum of 5 and 3 using lambda: {add(5, 3)}")
    print(f"Product of 5 and 3 using lambda: {multiply(5, 3)}")

# Main function to call all examples
def main():
    file_handling_example()
    list_comprehension_example()
    set_comprehension_example()
    lambda_example()

if __name__ == "__main__":
    main()
