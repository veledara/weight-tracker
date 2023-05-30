from asyncio.windows_events import NULL
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
        self.date_label = ttk.Label(self.add_frame, font=("Arial", 16))
        self.date_label.grid(column=0, row=0, sticky=(tk.N, tk.S), padx=5, pady=5)
        self.update_date_label()

        self.weight_entry = ttk.Entry(self.add_frame, width=15)
        self.weight_entry.grid(
            column=0, row=1, sticky=(tk.N, tk.W, tk.E, tk.S), padx=5, pady=5
        )

        self.add_mark_button = ttk.Button(
            self.add_frame,
            text="Add",
            command=lambda: self.add_mark(self.weight_entry.get().split("|")[0]),
        )
        self.add_mark_button.grid(
            column=0, row=2, sticky=(tk.N, tk.W, tk.E, tk.S), padx=5, pady=5
        )

        self.remove_last_mark_button = ttk.Button(
            self.add_frame,
            text="Remove last",
            command=lambda: self.remove_last_mark(),
        )
        self.remove_last_mark_button.grid(
            column=0, row=3, sticky=(tk.N, tk.W, tk.E, tk.S), padx=5, pady=5
        )
        self.weight_change_label = ttk.Label(self.add_frame, font=("Arial", 12))
        self.weight_change_label.grid(
            column=0, row=4, sticky=(tk.N, tk.S), padx=5, pady=5
        )
        self.update_weight_change_label()

    def update_weight_change_label(self):
        if len(self.graph.marks) > 1:
            current_weight_change = self.graph.show_weight_change()
            start_weight_text = (
                f"Ваш начальный вес: {self.graph.get_weight_on_start()} кг.\n"
            )
            current_weight_text = (
                f"Ваш текущий вес: {self.graph.get_current_weight()} кг.\n"
            )
            weight_change_text = (
                f"Вы набрали {-current_weight_change} кг."
                if current_weight_change < 0
                else f"Вы сбросили {current_weight_change} кг!"
            )
            label_text = start_weight_text + current_weight_text + weight_change_text
        else:
            label_text = f"Ваш вес не изменился."
        self.weight_change_label.config(text=label_text)

    def update_date_label(self):
        current_time = datetime.now().strftime(f"%d.%m.%y\n%H:%M:%S")
        self.date_label.config(text=current_time)
        self.date_label.after(1000, self.update_date_label)

    def update_graph(self):
        for widgets in self.weight_change_graph_labelframe.winfo_children():
            widgets.destroy()
        self.graph.update_axes()
        self.update_weight_change_label()
        canvas = FigureCanvasTkAgg(
            self.graph.fig, master=self.weight_change_graph_labelframe
        )
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

    def add_mark(self, weight: float):
        if self.weight_validation(weight):
            self.graph.add_mark(self.date_label.cget("text"), weight)
            self.update_graph()

    def remove_last_mark(self):
        if len(self.graph.marks) != 0:
            self.graph.remove_last_mark()
            self.update_graph()

    def weight_validation(self, weight):
        try:
            float_value = float(weight)
            return float_value > 0
        except (ValueError, TypeError):
            return False

    def run(self):
        self.root.mainloop()


if __name__ == "__main__":
    WeightTrackerGUI().run()
