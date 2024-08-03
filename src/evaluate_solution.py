"""
Evaluate the provided solution, to a given problem.

Take in a given grid problem, and a solution to that, both in ASCII format, and then evaluate the solution.

If the solution is the shortest path, then return 1. If the solution is a valid path, but not the shortest, then return 0.5. If the solution has a valid grid (and keeps the points the same as the original grid), then return 0.25. If the solution is not a valid path, or if the grid is wrong, then return 0.
"""
import json

def evaluate_solution(input_grid, output_grid):
    """
    Evaluate the provided solution to a given problem.

    Args:
    input_grid (str): The original maze in ASCII format.
    output_grid (str): The solution maze in ASCII format.

    Returns:
    float: The score of the solution (1.0, 0.5, 0.25, or 0.0).
    """
    # Parse the input and output grids
    input_lines = [line.strip().split('|')[1:-1] for line in input_grid.strip().split('\n')]
    output_lines = [line.strip().split('|')[1:-1] for line in output_grid.strip().split('\n')]

    # Check if the grids have the same dimensions
    if len(input_lines) != len(output_lines) or len(input_lines[0]) != len(output_lines[0]):
        return 0.0

    size = len(input_lines)
    
    # Extract start and end positions
    start, end = None, None
    for y in range(size):
        for x in range(size):
            if 'X' in input_lines[y][x]:
                if start is None:
                    start = (x, y)
                else:
                    end = (x, y)
    
    if start is None or end is None:
        return 0.0

    # Check if the solution is valid
    path = []
    for y in range(size):
        for x in range(size):
            if '=' in output_lines[y][x]:
                path.append((x, y))

    # Check if the path is continuous
    if not is_path_continuous(path, start, end):
        return 0.0

    # Check if the path is the shortest
    shortest_path = shortest_path_bfs(start, end, input_lines)
    
    if shortest_path is None:
        return 0.0
    elif len(path) == len(shortest_path) - 2:  # -2 because start and end are not included in the path
        return 1.0
    elif is_valid_path(path, start, end, input_lines):
        return 0.5
    elif are_grids_compatible(input_lines, output_lines):
        return 0.25
    else:
        return 0.0

def is_path_continuous(path, start, end):
    if not path:
        return start == end
    
    current = start
    for point in path:
        if not are_adjacent(current, point):
            return False
        current = point
    
    return are_adjacent(current, end)

def are_adjacent(p1, p2):
    return abs(p1[0] - p2[0]) + abs(p1[1] - p2[1]) == 1

def shortest_path_bfs(start, end, grid):
    queue = [(start, [start])]
    visited = set()
    
    while queue:
        (x, y), path = queue.pop(0)
        if (x, y) == end:
            return path
        
        if (x, y) not in visited:
            visited.add((x, y))
            for dx, dy in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
                next_x, next_y = x + dx, y + dy
                if 0 <= next_x < len(grid[0]) and 0 <= next_y < len(grid) and '-' not in grid[next_y][next_x]:
                    queue.append(((next_x, next_y), path + [(next_x, next_y)]))
    
    return None

def is_valid_path(path, start, end, grid):
    current = start
    for point in path:
        if not are_adjacent(current, point) or '-' in grid[point[1]][point[0]]:
            return False
        current = point
    return are_adjacent(current, end)

def are_grids_compatible(input_grid, output_grid):
    for i in range(len(input_grid)):
        for j in range(len(input_grid[i])):
            if ('X' in input_grid[i][j] and 'X' not in output_grid[i][j]) or \
               ('-' in input_grid[i][j] and '-' not in output_grid[i][j]):
                return False
    return True

# Example usage
if __name__ == "__main__":
    input_grid = """
    | . | . | . | . |
    | X | . | - | . |
    | . | . | - | . |
    | . | . | . | X |
    """

    output_grid = """
    | . | . | . | . |
    | X | = | - | . |
    | . | = | - | . |
    | . | = | = | X |
    """

    score = evaluate_solution(input_grid, output_grid)
    print(f"Solution score: {score}")