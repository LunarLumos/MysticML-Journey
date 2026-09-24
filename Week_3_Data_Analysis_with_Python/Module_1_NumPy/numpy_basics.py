import numpy as np

# 1️⃣ Creating NumPy Arrays
arr1 = np.array([1, 2, 3, 4, 5])  # 1D array
arr2 = np.array([[1, 2, 3], [4, 5, 6]])  # 2D array

# Special arrays
zeros = np.zeros((3, 3))  # 3x3 matrix of zeros
ones = np.ones((2, 4))  # 2x4 matrix of ones
identity = np.eye(3)  # Identity matrix
random_arr = np.random.rand(2, 3)  # 2x3 random values

# 2️⃣ Array Attributes
print("Shape:", arr2.shape)
print("Size:", arr2.size)
print("Data type:", arr2.dtype)
print("Number of dimensions:", arr2.ndim)

# 3️⃣ Indexing and Slicing
print(arr2[0, 1])  # Element at first row, second column
print(arr2[:, 1])  # All rows, second column
print(arr2[1, :])  # Second row, all columns
print(arr2[:2, :2])  # First two rows, first two columns

# 4️⃣ Mathematical Operations
arr = np.array([1, 2, 3, 4])
print("Add 2:", arr + 2)
print("Multiply by 3:", arr * 3)
print("Exponential:", np.exp(arr))
print("Square root:", np.sqrt(arr))
print("Mean:", np.mean(arr))
print("Sum:", np.sum(arr))

# 5️⃣ Reshaping Arrays
arr3 = np.arange(12)  # Array from 0 to 11
reshaped = arr3.reshape(3, 4)  # Reshape into 3x4 matrix
print("Reshaped Array:\n", reshaped)

# 6️⃣ Concatenation & Stacking
arr4 = np.array([[10, 20], [30, 40]])
arr5 = np.array([[50, 60], [70, 80]])

horizontal_stack = np.hstack((arr4, arr5))  # Horizontally stack
vertical_stack = np.vstack((arr4, arr5))  # Vertically stack
print("Horizontal Stack:\n", horizontal_stack)
print("Vertical Stack:\n", vertical_stack)

# 7️⃣ Statistical Functions
data = np.array([[5, 10, 15], [20, 25, 30]])
print("Max:", np.max(data))  # Maximum value
print("Min:", np.min(data))  # Minimum value
print("Sum along axis 0:", np.sum(data, axis=0))  # Sum of columns
print("Sum along axis 1:", np.sum(data, axis=1))  # Sum of rows
