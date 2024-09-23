import numpy as np
from plant import Plant

def get_neighbor_coordinates(arr, i, j):
    # Define the range for rows and columns, ensuring the indices don't go out of bounds
    row_start = max(0, i-1)
    row_end = min(arr.shape[0], i+2)
    col_start = max(0, j-1)
    col_end = min(arr.shape[1], j+2)
    
    # Collect the neighboring coordinates
    neighbors = []
    for row in range(row_start, row_end):
        for col in range(col_start, col_end):
            # Exclude the center cell (i, j)
            if row == i and col == j:
                continue
            neighbors.append((row, col))
    
    return neighbors

# Example 2D array
arr = np.array([[1, 2, 3],
                [4, 5, 6],
                [7, 8, 9]])

# Get neighbor coordinates of the element at (1, 1)
neighbor_coords = get_neighbor_coordinates(arr, 1, 1)
print(neighbor_coords)


print(np.eye(10,Plant))