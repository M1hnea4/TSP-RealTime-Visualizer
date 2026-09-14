import math
import random
import time
import matplotlib.pyplot as plt

plt.rcParams['toolbar'] = 'None'

class TSPSolver:
    def __init__(self, file_name):
        self.coordinates = self.read_coordinates(file_name)
        self.cities = list(self.coordinates.keys())
        self.dist_matrix = self.create_distance_matrix()
        
        self.fig, self.ax = plt.subplots(figsize=(9, 7))
        self.fig.canvas.manager.set_window_title('TSP Real-Time Optimizer')
        plt.ion() 

    def read_coordinates(self, file_name):
        coords = {}
        try:
            with open(file_name, 'r') as f:
                for line in f:
                    parts = line.strip().split()
                    if len(parts) == 3:
                        coords[int(parts[0])] = (float(parts[1]), float(parts[2]))
        except FileNotFoundError:
            print(f"Error: {file_name} not found. Ensure the file is in the same folder.")
        return coords

    def create_distance_matrix(self):
        matrix = {}
        for id1, p1 in self.coordinates.items():
            matrix[id1] = {id2: math.sqrt((p1[0]-p2[0])**2 + (p1[1]-p2[1])**2) 
                           for id2, p2 in self.coordinates.items()}
        return matrix

    def get_fitness(self, route):
        return sum(self.dist_matrix[route[i]][route[(i+1) % len(route)]] for i in range(len(route)))

    def update_plot(self, route, cost, info):
        self.ax.clear()
        
        x = [self.coordinates[c][0] for c in route] + [self.coordinates[route[0]][0]]
        y = [self.coordinates[c][1] for c in route] + [self.coordinates[route[0]][1]]
        
        self.ax.plot(x, y, color='#2c3e50', linewidth=1.5, marker='o', 
                     markerfacecolor='#e74c3c', markersize=5, alpha=0.9)
        
        self.ax.set_xticks([])
        self.ax.set_yticks([])
        for spine in self.ax.spines.values():
            spine.set_visible(False)
            
        self.ax.set_title(f"{info}\nTotal Distance: {cost:.2f}", fontsize=12, color='#34495e')
        plt.pause(0.005)

    # --- 1. HILL CLIMBING ---
    def hill_climbing(self, child_id):
        current_route = self.cities[:]
        random.shuffle(current_route)
        current_cost = self.get_fitness(current_route)
        improved = True
        while improved:
            improved = False
            for i in range(1, len(current_route) - 2):
                for j in range(i + 1, len(current_route)):
                    new_route = current_route[:]
                    new_route[i:j] = current_route[i:j][::-1] 
                    new_cost = self.get_fitness(new_route)
                    if new_cost < current_cost:
                        current_cost = new_cost
                        current_route = new_route
                        improved = True
                        self.update_plot(current_route, current_cost, f"Child {child_id} | Hill Climbing")
                        break
                if improved: break
        return current_route, current_cost

    # --- 2. SIMULATED ANNEALING ---
    def simulated_annealing(self, child_id):
        current_route = self.cities[:]
        random.shuffle(current_route)
        current_cost = self.get_fitness(current_route)
        temp, cooling_rate = 1000, 0.995
        
        while temp > 1:
            i, j = sorted(random.sample(range(len(current_route)), 2))
            new_route = current_route[:]
            new_route[i:j] = current_route[i:j][::-1]
            new_cost = self.get_fitness(new_route)
            
            if new_cost < current_cost or random.random() < math.exp((current_cost - new_cost) / temp):
                current_cost = new_cost
                current_route = new_route
                if random.random() > 0.97: 
                    self.update_plot(current_route, current_cost, f"Child {child_id} | SA (Temp: {int(temp)})")
            temp *= cooling_rate
        return current_route, current_cost

    # --- 3. TABU SEARCH ---
    def tabu_search(self, child_id):
        current_route = self.cities[:]
        random.shuffle(current_route)
        best_child_route, best_child_cost = current_route[:], self.get_fitness(current_route)
        tabu_list, iterations = [], 100
        
        for _ in range(iterations):
            best_neighbor, best_neighbor_cost, move = None, float('inf'), None
            for _ in range(40): 
                i, j = sorted(random.sample(range(len(self.cities)), 2))
                m = (current_route[i], current_route[j])

                new_route = current_route[:]
                new_route[i:j] = current_route[i:j][::-1]
                new_cost = self.get_fitness(new_route)

                if m not in tabu_list or new_cost < best_child_cost:
                    if new_cost < best_neighbor_cost:
                        best_neighbor_cost, best_neighbor, move = new_cost, new_route, m
            
            if best_neighbor:
                current_route = best_neighbor
                tabu_list.append(move)
                if len(tabu_list) > 20: tabu_list.pop(0)
                if best_neighbor_cost < best_child_cost:
                    best_child_cost, best_child_route = best_neighbor_cost, best_neighbor
                    self.update_plot(best_child_route, best_child_cost, f"Child {child_id} | Tabu Search")
        return best_child_route, best_child_cost

def main():
    solver = TSPSolver('berlin52.txt')
    if not solver.coordinates: return

    print("1. Hill Climbing (2-Opt)")
    print("2. Simulated Annealing")
    print("3. Tabu Search")
    
    choice = input("\nSelect Method (1-3): ")
    try:
        num_children = int(input("How many children (instances) to run?: ") or 1)
    except ValueError:
        num_children = 1

    best_global_route, best_global_cost = None, float('inf')

    for i in range(1, num_children + 1):
        if choice == '1': 
            route, cost = solver.hill_climbing(i)
        elif choice == '2': 
            route, cost = solver.simulated_annealing(i)
        elif choice == '3': 
            route, cost = solver.tabu_search(i)
        else: 
            print("Invalid choice!"); return

        if cost < best_global_cost:
            best_global_cost, best_global_route = cost, route
            print(f" >>> Global Record! Child {i}: {best_global_cost:.2f}")


    plt.ioff()
    solver.update_plot(best_global_route, best_global_cost, f"FINAL BEST (of {num_children} children)")
    print(f"\nOptimization Finished.")
    print(f"Shortest Distance Found: {best_global_cost:.2f}")
    plt.show()

if __name__ == "__main__":
    main()