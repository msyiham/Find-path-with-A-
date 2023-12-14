import tkinter as tk
from queue import PriorityQueue

class Node:
    def __init__(self, row, col, is_obstacle=False):
        self.row = row
        self.col = col
        self.is_obstacle = is_obstacle
        self.neighbors = []
        self.parent = None
        self.g_cost = float('inf')
        self.h_cost = 0

    def __lt__(self, other):
        return (self.g_cost + self.h_cost) < (other.g_cost + other.h_cost)

class AStarApp:
    def __init__(self, master, rows, cols):
        self.master = master
        self.master.title("A* Pathfinding App")
        self.rows = rows
        self.cols = cols
        self.grid = [[Node(row, col) for col in range(cols)] for row in range(rows)]
        self.start_node = None
        self.end_node = None
        self.obstacle_nodes = set()
        self.canvas = tk.Canvas(master, width=cols*30, height=rows*30)
        self.canvas.pack()
        self.canvas.bind("<Button-1>", self.on_canvas_click)
        self.create_grid()
        self.find_path_button = tk.Button(master, text="Find Path", command=self.find_path)
        self.find_path_button.pack(side=tk.LEFT)
        self.reset_button = tk.Button(master, text="Reset", command=self.reset_grid)
        self.reset_button.pack(side=tk.LEFT)

    def create_grid(self):
        for row in range(self.rows):
            for col in range(self.cols):
                node = self.grid[row][col]
                color = "white"
                if node.is_obstacle:
                    color = "black"
                self.canvas.create_rectangle(col*30, row*30, (col+1)*30, (row+1)*30, fill=color)

    def on_canvas_click(self, event):
        col = event.x // 30
        row = event.y // 30
        clicked_node = self.grid[row][col]
        if not self.start_node:
            self.start_node = clicked_node
            self.color_node(self.start_node, "green")
        elif not self.end_node:
            self.end_node = clicked_node
            self.color_node(self.end_node, "red")
        else:
            if clicked_node != self.start_node and clicked_node != self.end_node:
                clicked_node.is_obstacle = not clicked_node.is_obstacle
                if clicked_node.is_obstacle:
                    self.obstacle_nodes.add(clicked_node)
                    self.color_node(clicked_node, "black")
                else:
                    self.obstacle_nodes.remove(clicked_node)
                    self.color_node(clicked_node, "white")

    def initialize_neighbors(self):
        for row in range(self.rows):
            for col in range(self.cols):
                current_node = self.grid[row][col]
                neighbors = []

                directions = [(0, -1), (-1, 0), (0, 1), (1, 0)]
                for i, j in directions:
                    new_row, new_col = row + i, col + j
                    if 0 <= new_row < self.rows and 0 <= new_col < self.cols:
                        neighbors.append(self.grid[new_row][new_col])

                current_node.neighbors = neighbors

    def color_node(self, node, color):
        self.canvas.create_rectangle(node.col*30, node.row*30, (node.col+1)*30, (node.row+1)*30, fill=color)

    def find_path(self):
        if not self.start_node or not self.end_node:
            return

        self.initialize_neighbors()

        open_set = PriorityQueue()
        open_set.put(self.start_node)
        self.start_node.g_cost = 0
        self.start_node.h_cost = self.calculate_heuristic(self.start_node, self.end_node)

        while not open_set.empty():
            current_node = open_set.get()

            if current_node == self.end_node:
                self.draw_path()
                return

            for neighbor in current_node.neighbors:
                tentative_g_cost = current_node.g_cost + 1

                if tentative_g_cost < neighbor.g_cost and neighbor not in self.obstacle_nodes:
                    neighbor.parent = current_node
                    neighbor.g_cost = tentative_g_cost
                    neighbor.h_cost = self.calculate_heuristic(neighbor, self.end_node)
                    open_set.put(neighbor)

                self.color_node(current_node, "blue")
                self.master.update()

    def draw_path(self):
        current_node = self.end_node
        while current_node:
            self.color_node(current_node, "yellow")
            current_node = current_node.parent
            self.master.update()

    def reset_grid(self):
        self.start_node = None
        self.end_node = None
        self.obstacle_nodes.clear()

        self.canvas.delete("all")

        # Buat grid baru dan atur ulang nilai is_obstacle
        self.grid = [[Node(row, col) for col in range(self.cols)] for row in range(self.rows)]
        self.create_grid()

    def calculate_heuristic(self, node, target_node):
        return abs(node.row - target_node.row) + abs(node.col - target_node.col)

if __name__ == "__main__":
    rows = 10
    cols = 15
    root = tk.Tk()
    app = AStarApp(root, rows, cols)
    root.mainloop()