from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np

# Generate sample data
days = np.arange(1, 11)  # Example: 10 days
weight = [
    70,
    69.5,
    69,
    68.8,
    68.2,
    67.7,
    68,
    68.5,
    68.2,
    68.7,
]  # Example: Weight data for each day

# Create a Matplotlib figure
fig = Figure(figsize=(6, 4), dpi=100, facecolor="lightgray")
ax = fig.add_subplot(111)
ax.plot(days, weight, color="red", marker="o")
ax.set_xlabel("Days")
ax.set_ylabel("Weight")
ax.set_title("Weight Statistics")
ax.grid(True)
