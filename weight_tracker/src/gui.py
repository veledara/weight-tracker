import tkinter as tk
from weight_tracker.src.graph import fig
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from tkinter import ttk


class WeightTrackerGUI:
    def __init__(self) -> None:
        self.root = tk.Tk()
        self.root.title("Weight Tracker")
        self.root.geometry("1024x768")
        #self.root.resizable(False, False)
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)

        self.main_window_show()

    def main_window_show(self):
        self.weight_change_graph_labelframe = tk.LabelFrame(
            self.root, bg='lightgray'
        )
        self.weight_change_graph_labelframe.grid(
            column=0, row=0, sticky=(tk.N, tk.W, tk.E, tk.S), padx=20, pady=20
        )

        canvas = FigureCanvasTkAgg(fig, master=self.weight_change_graph_labelframe)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

        self.options_labelframe = tk.LabelFrame(
            self.root, text="Options"
        )
        self.options_labelframe.grid(
            column=0, row=1, sticky=(tk.N, tk.W, tk.E, tk.S), padx=20, pady=20
        )

    def run(self):
        self.root.mainloop()


if __name__ == "__main__":
    WeightTrackerGUI().run()
