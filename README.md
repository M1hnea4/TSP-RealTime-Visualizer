# 🌍 TSP Berlin52 Real-Time Optimizer

A real-time visualization tool that solves the Traveling Salesperson Problem (TSP) for the classic `berlin52` dataset. Watch the algorithms "untangle" the routes live on your screen!!

## 🚀 Features
* **Live Matplotlib Visualization:** See the route distance decrease in real-time as the algorithms optimize the path.
* **Three Heuristic Algorithms:**
  1. **Hill Climbing (2-Opt):** Rapidly untangles crossed paths to find local optimums.
  2. **Simulated Annealing:** Uses a cooling schedule to probabilistically escape local minimums.
  3. **Tabu Search:** Uses a memory structure (Tabu List) to avoid cycling back to recently visited routes.
* **Multi-Start Approach (Children):** Run multiple independent instances ("children") to find the best global route among different random starting configurations.

## 🛠️ Prerequisites
* Python 3.x
* `matplotlib`

Install the required library using:
\`\`\`bash
pip install matplotlib
\`\`\`

## 🎮 How to Use
1. Run the script: `python "tsp berlin52.py"`
2. Select the algorithm you want to use (1, 2, or 3).
3. Input the number of "children" (restarts) you want to run.
4. Watch the real-time plotting as the algorithms find the shortest path between the 52 locations in Berlin!

## 📊 Dataset
This project uses the classic `berlin52.txt` dataset from the TSPLIB library, containing 52 locations in Berlin.
