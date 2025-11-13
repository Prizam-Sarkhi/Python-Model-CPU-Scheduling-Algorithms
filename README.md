# CPU Scheduling Algorithm Simulation (Python + Tableau)

This project simulates four classical CPU scheduling algorithms:

- First-Come First-Serve (FCFS)
- Shortest Job First (SJF)
- Priority Scheduling
- Round Robin (RR)

The program generates random workloads (Light, Mixed, Heavy) and evaluates:

- Turnaround Time (TAT)
- Waiting Time (WT)
- Response Time (RT)

Each algorithm runs 10 times per workload, results are averaged, exported to CSV, 
and visualized in Tableau.

## How to run

$ python main.py

## Output

- raw_results.csv
- averaged_results.csv

## Visualization

CSV output can be imported directly into Tableau to generate performance comparisons.
