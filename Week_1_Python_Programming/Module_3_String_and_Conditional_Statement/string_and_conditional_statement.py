#! /bin/python3
my_string = "  Hello, Python World!   "
print("Original String:", my_string)

# Strip leading and trailing whitespaces
cleaned_string = my_string.strip()
print("After strip:", cleaned_string)

# Convert to uppercase
upper_string = cleaned_string.upper()
print("Uppercase:", upper_string)

# Convert to lowercase
lower_string = cleaned_string.lower()
print("Lowercase:", lower_string)

# Replace "Python" with "Programming"
replaced_string = cleaned_string.replace("Python", "Programming")
print("Replaced String:", replaced_string)

# Split the string into a list of words
words = cleaned_string.split(" ")
print("Split String:", words)

# String formatting using the format() function
name = "Alice"
age = 30
formatted_string = "My name is {} and I am {} years old.".format(name, age)
print("Formatted String:", formatted_string)

# if-else
x = 10
if x > 5:
    print(f"x = {x} is greater than 5.")
else:
    print(f"x = {x} is not greater than 5.")

# Using elif 
if x < 5:
    print(f"x = {x} is less than 5.")
elif x == 5:
    print(f"x = {x} is equal to 5.")
else:
    print(f"x = {x} is greater than 5.")

#ternary operator
y = 7
result = "Positive" if y > 0 else "Non-positive"
print(f"y = {y} is {result}.")

# Personalized greeting based on user input
user_name = input("Enter your name: ")

if user_name == "Alice":
    print("Hello Alice! Welcome back!")
elif user_name == "Bob":
    print("Hey Bob! How's it going?")
else:
    print(f"Hello {user_name}, nice to meet you!")


# Extract part of the string using slicing
for i in range(len(cleaned_string)):
    print(f"Character at index {i} is {cleaned_string[i]}")

substring = my_string[0:5]
print("Substring (0:5):", substring)

substring1 = my_string[:5]
print("Substring (:5):", substring1) 

substring2 = my_string[7:]  
print("Substring (7:):", substring2) 


substring3 = my_string[-6:]  
print("Substring (-6:):", substring3)

substring4 = my_string[0:12:2] 
print("Substring (0:12:2):", substring4)
