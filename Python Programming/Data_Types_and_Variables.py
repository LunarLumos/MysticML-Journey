#! /bin/python3
# 1. Primitive Data Types
x = 10           # Integer
y = 3.14         # Float
name = "Alice"   # String
is_active = True # Boolean

# Print Primitive Data Types
print("Primitive Data Types:")
print(f"x = {x}, type = {type(x)}")
print(f"y = {y}, type = {type(y)}")
print(f"name = {name}, type = {type(name)}")
print(f"is_active = {is_active}, type = {type(is_active)}\n")

# 2. Mutable and Immutable Data Types
# Immutable Example: Tuple
coordinates = (10, 20)
# Mutable Examples: List, Dictionary, Set
fruits = ["apple", "banana", "cherry"]  # List
person = {"name": "John", "age": 30}    # Dictionary
unique_numbers = {1, 2, 3 , 7, 5, 6}              # Set

# Print Mutable and Immutable Data Types
print("Mutable and Immutable Data Types:")
print(f"coordinates = {coordinates}, type = {type(coordinates)}")  # Immutable
print(f"fruits = {fruits}, type = {type(fruits)}")                  # Mutable
print(f"person = {person}, type = {type(person)}")                # Mutable
print(f"unique_numbers = {unique_numbers}, type = {type(unique_numbers)}\n")

# 3. Working with Lists (Mutable)
fruits.append("orange")  # Add item to list
fruits.remove("banana")  # Remove item from list
print("Working with Lists:")
print(f"Updated fruits list: {fruits}\n")

# 4. Working with Tuples
coordinates = coordinates + (30, 40)  # Creating a new tuple
print("Working with Tuples:")
print(f"Updated coordinates tuple: {coordinates}\n")

# 5. Working with Dictionaries
person["age"] = 35  # Modify value in dictionary
person["city"] = "New York"  # Add new key-value pair
print("Working with Dictionaries:")
print(f"Updated person dictionary: {person}\n")

# 6. Working with Sets 
unique_numbers.add(7)  # Add element to set
unique_numbers.remove(3)  # Remove element from set
print("Working with Sets:")
print(f"Updated unique_numbers set: {unique_numbers}\n")

# 7. Set Operations
print("Set Operations:")
print(f"Is 3 in unique_numbers? {3 in unique_numbers}")  # Check if 3 is in the set
print(f"Union of sets: {unique_numbers | {5, 6}}")  # Union of sets
print(f"Intersection of sets: {unique_numbers & {5, 7}}")  # common of sets
