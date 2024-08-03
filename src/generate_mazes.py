import random
import math
import json
from collections import deque
from tqdm import tqdm

# Global variables
GRID_SIZES = [4, 8, 16, 32]
OUTPUT_FILE_TEMPLATE = 'data/grid_problems_{size}x{size}.jsonl'
NUM_PROBLEMS_PER_SIZE = 25000

def distance(x1, y1, x2, y2):
    return math.sqrt((x2 - x1)**2 + (y2 - y1)**2)

def create_grid(size):
    return [[' . ' for _ in range(size)] for _ in range(size)]

def draw_obstacle(grid, size):
    min_obstacle_size = max(1, size // 8)
    max_obstacle_size = max(2, size // 4)
    obstacle_size = random.randint(min_obstacle_size, max_obstacle_size)
    is_vertical = random.choice([True, False])
    
    if is_vertical:
        x = random.randint(0, size - 1)
        y = random.randint(0, size - obstacle_size)
        for i in range(obstacle_size):
            grid[y + i][x] = ' - '
    else:
        x = random.randint(0, size - obstacle_size)
        y = random.randint(0, size - 1)
        for i in range(obstacle_size):
            grid[y][x + i] = ' - '

def shortest_path_bfs(start, end, grid, size):
    queue = deque([(start, [])])
    visited = set()
    shortest_path = None
    shortest_length = float('inf')
    
    while queue:
        (x, y), path = queue.popleft()
        
        if len(path) >= shortest_length:
            continue
        if (x, y) == end:
            if len(path) < shortest_length:
                shortest_path = path + [(x, y)]
                shortest_length = len(shortest_path)
            continue
        if (x, y) not in visited:
            visited.add((x, y))
            for dx, dy in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
                next_x, next_y = x + dx, y + dy
                if 0 <= next_x < size and 0 <= next_y < size and grid[next_y][next_x] != ' - ':
                    queue.append(((next_x, next_y), path + [(x, y)]))
    
    return shortest_path

def grid_to_string(grid):
    return '\n'.join(['|' + '|'.join(row) + '|' for row in grid])

def generate_problem(size):
    grid = create_grid(size)
    
    start_x, start_y = random.randint(0, size - 1), random.randint(0, size - 1)
    grid[start_y][start_x] = ' X '
    
    min_start_end_distance = max(2, size // 4)
    while True:
        end_x, end_y = random.randint(0, size - 1), random.randint(0, size - 1)
        if distance(start_x, start_y, end_x, end_y) >= min_start_end_distance:
            grid[end_y][end_x] = ' X '
            break
    
    min_obstacles = max(1, size // 4)
    max_obstacles = max(2, size // 2)
    num_obstacles = random.randint(min_obstacles, max_obstacles)
    for _ in range(num_obstacles):
        draw_obstacle(grid, size)
    
    input_grid = grid_to_string(grid)
    
    path = shortest_path_bfs((start_x, start_y), (end_x, end_y), grid, size)
    
    if path:
        solution_grid = [row[:] for row in grid]
        for x, y in path:
            if (x, y) != (start_x, start_y) and (x, y) != (end_x, end_y):
                solution_grid[y][x] = ' = '
        output_grid = grid_to_string(solution_grid)
    else:
        output_grid = "No path found"
    
    # New role: system
    system_representation = {
        "grid_size": size,
        "start": [start_x, start_y],
        "end": [end_x, end_y],
        "obstacles": [[y, x] for y in range(size) for x in range(size) if grid[y][x] == ' - '],
        "solution": path if path else None
    }
    
    return [
        {
            "role": "system",
            "content": json.dumps(system_representation)
        },
        {
            "role": "user",
            "content": input_grid
        },
        {
            "role": "assistant",
            "content": output_grid
        }
    ]

def generate_problems(num_problems, size, output_file):
    with open(output_file, 'w') as f:
        for _ in tqdm(range(num_problems)):
            problem = generate_problem(size)
            json.dump(problem, f)
            f.write('\n')

# Generate problems for each grid size and save to separate JSONL files
for size in GRID_SIZES:
    output_file = OUTPUT_FILE_TEMPLATE.format(size=size)
    generate_problems(NUM_PROBLEMS_PER_SIZE, size, output_file)
    print(f"{NUM_PROBLEMS_PER_SIZE} problems generated for {size}x{size} grid and saved to {output_file}")