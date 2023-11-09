import random
from queue import Queue
import colorama

colorama.init()  # Initialize colorama


def generate_maze(n, wall_percentage=25):
    maze = [['◌' for _ in range(n)] for _ in range(n)]

    # Set start and end points
    start, end = (0, 0), (n - 1, n - 1)
    maze[start[0]][start[1]] = 'S'
    maze[end[0]][end[1]] = 'E'

    # Add random walls
    num_walls = int((wall_percentage / 100) * (n * n))
    for _ in range(num_walls):
        x, y = random.randint(0, n - 1), random.randint(0, n - 1)
        while (x, y) == start or (x, y) == end or maze[x][y] == '▓':
            x, y = random.randint(0, n - 1), random.randint(0, n - 1)
        maze[x][y] = '▓'

    return maze


def print_colored_maze(maze):
    for row in maze:
        for cell in row:
            if cell == '▓':
                print(colorama.Fore.RED + cell, end=" ")  # Walls in red
            elif cell == '◌':
                print(colorama.Fore.BLUE + cell, end=" ")  # Open spaces in blue
            elif cell == '◍':
                print(colorama.Fore.GREEN + cell, end=" ")  # Path in green
            else:
                print(cell, end=" ")
        print()
    print()


def find_path(maze):
    start, end = (0, 0), (len(maze) - 1, len(maze[0]) - 1)
    visited = set()
    path = []

    def dfs(current):
        if current == end:
            path.append(current)
            return True

        visited.add(current)
        neighbors = get_neighbors(current, maze)

        for neighbor in neighbors:
            if neighbor not in visited:
                path.append(current)
                if dfs(neighbor):
                    return True
                path.pop()

        return False

    if dfs(start):
        return path
    else:
        return None


def get_neighbors(cell, maze):
    x, y = cell
    neighbors = []

    for i, j in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
        nx, ny = x + i, y + j
        if 0 <= nx < len(maze) and 0 <= ny < len(maze[0]) and maze[nx][ny] != '▓':
            neighbors.append((nx, ny))

    return neighbors


def mark_path_on_maze(maze, path):
    for i in range(len(maze)):
        for j in range(len(maze[0])):
            if maze[i][j] == '◌' and (i, j) not in path:
                maze[i][j] = '◌'
            elif (i, j) in path:
                maze[i][j] = '◍'


# Main program
if __name__ == "__main__":
    while True:
        print("Menu:")
        print("1. Print Path")
        print("2. Generate New Puzzle")
        print("3. Exit")

        choice = input("Enter your choice (1/2/3): ")

        if choice == '1':
            maze_size = int(input("Enter the size of the maze: "))
            maze = generate_maze(maze_size)
            print("Generated Maze:")
            print_colored_maze(maze)

            path = find_path(maze)

            if path:
                mark_path_on_maze(maze, path)
                print("Path Found:")
                print_colored_maze(maze)
            else:
                print("No path found.")

        elif choice == '2':
            continue  # The loop will generate a new puzzle in the next iteration

        elif choice == '3':
            print("Exiting the program. Goodbye!")
            break

        else:
            print("Invalid choice. Please enter 1, 2, or 3.")
