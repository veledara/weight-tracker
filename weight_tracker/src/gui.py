from sys import float_repr_style
import tkinter as tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from tkinter import ttk
from datetime import datetime
from graph import GraphMaker


class WeightTrackerGUI:
    graph: GraphMaker
    def __init__(self) -> None:
        self.root = tk.Tk()
        self.root.title("Weight Tracker")
        self.root.geometry("1024x512")
        # self.root.resizable(False, False)
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        self.graph = GraphMaker()

        self.main_window_show()

    def main_window_show(self):
        self.weight_change_graph_labelframe = tk.LabelFrame(self.root, bg="lightgray")
        self.weight_change_graph_labelframe.grid(
            column=0, row=0, sticky=(tk.N, tk.W, tk.E, tk.S), padx=20, pady=20
        )

        self.options_labelframe = tk.LabelFrame(self.root, text="Options")

        self.options_labelframe.grid(
            column=1, row=0, sticky=(tk.N, tk.W, tk.E, tk.S), padx=20, pady=20
        )

        self.add_frame = tk.Frame(self.options_labelframe)
        self.add_frame.grid(
            column=0, row=1, sticky=(tk.N, tk.W, tk.E, tk.S), padx=20, pady=10
        )
        self.date_label = ttk.Label(self.add_frame)
        self.update_label()
        self.date_label.grid(
            column=0, row=0, sticky=(tk.N, tk.W, tk.E, tk.S), padx=5, pady=5
        )

        self.weight_entry = ttk.Entry(self.add_frame, width=15)
        self.weight_entry.grid(
            column=0, row=1, sticky=(tk.N, tk.W, tk.E, tk.S), padx=5, pady=5
        )

        self.add_mark_button = ttk.Button(
            self.add_frame,
            text="add",
            command=lambda: self.add_mark_to_graph(self.weight_entry.get().split("|")[0]),
        )
        self.add_mark_button.grid(
            column=0, row=2, sticky=(tk.N, tk.W, tk.E, tk.S), padx=5, pady=5
        )

    def update_label(self):
        current_time = datetime.now().strftime(f"%d.%m.%y | %H:%M:%S")
        self.date_label.config(text=current_time)
        self.date_label.after(1000, self.update_label)

    def update_graph(self):
        for widgets in self.weight_change_graph_labelframe.winfo_children():
             widgets.destroy()
        self.graph.update_graph()
        canvas = FigureCanvasTkAgg(
            self.graph.fig, master=self.weight_change_graph_labelframe
        )
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

    def add_mark_to_graph(self, weight: float):
        self.weight_validation()
        self.graph.add_mark(self.date_label.cget("text"), weight)
        self.update_graph()

    def weight_validation(self):
        pass

    def run(self):
        self.root.mainloop()


if __name__ == "__main__":
    WeightTrackerGUI().run()
