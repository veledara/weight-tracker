import tkinter as tk
from tkinter import ttk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
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
        self.file_path = "data.json"

        self.main_window_show()

    def __del__(self):
        self.save_data()

    def main_window_show(self):
        self.weight_change_graph_labelframe = tk.LabelFrame(self.root, bg="lightgray")
        self.weight_change_graph_labelframe.grid(
            column=0, row=0, sticky=(tk.N, tk.W, tk.E, tk.S), padx=20, pady=20
        )

        self.options_labelframe = tk.LabelFrame(self.root, text="Options")

        self.options_labelframe.grid(
            column=1, row=0, sticky=(tk.N, tk.W, tk.E, tk.S), padx=20, pady=20
        )

        self.options_labelframe.columnconfigure(0, weight=1)
        self.options_labelframe.rowconfigure(0, weight=1)

        self.add_frame = tk.Frame(self.options_labelframe)
        self.add_frame.grid(
            column=0, row=0, sticky=(tk.N, tk.W, tk.E, tk.S), padx=20, pady=10
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
            command=lambda: self.add_mark(self.weight_entry.get()),
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
        self.clear_all_button = ttk.Button(
            self.add_frame,
            text="Clear all",
            command=lambda: self.show_clear_all_window(),
        )
        self.clear_all_button.grid(
            column=0, row=4, sticky=(tk.N, tk.W, tk.E, tk.S), padx=5, pady=5
        )
        self.statistics_button = ttk.Button(
            self.options_labelframe,
            text="Statistics",
            command=lambda: self.show_statistics_window(),
        )
        self.statistics_button.grid(column=0, row=1, sticky=tk.S, padx=5, pady=5)

        self.load_data()

    def update_graph(self):
        for widgets in self.weight_change_graph_labelframe.winfo_children():
            widgets.destroy()
        self.graph.update_axes()
        canvas = FigureCanvasTkAgg(
            self.graph.fig, master=self.weight_change_graph_labelframe
        )
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

    def update_date_label(self):
        current_time = datetime.now().strftime(f"%d.%m.%y\n%H:%M:%S")
        self.date_label.config(text=current_time)
        self.date_label.after(1000, self.update_date_label)

    def update_weight_change_label(self):
        if len(self.graph.marks) > 1:
            current_weight_change = self.graph.show_weight_change()
            start_weight_text = (
                f"Your starting weight: {self.graph.get_weight_on_start()} kg.\n"
            )
            current_weight_text = (
                f"Your current weight: {self.graph.get_current_weight()} kg.\n"
            )
            weight_change_text = (
                f"You have gained {-current_weight_change} kg."
                if current_weight_change < 0
                else f"You have lost {current_weight_change} kg!"
            )
            label_text = start_weight_text + current_weight_text + weight_change_text
        else:
            label_text = f"Your weight hasn't changed."
        self.weight_change_label.config(text=label_text)

    def show_statistics_window(self):
        self.statistics_window = tk.Toplevel(self.root)
        self.statistics_window.grab_set()
        self.statistics_window.title("Statistics")
        self.statistics_window.resizable(False, False)

        self.statistics_window.update()
        x = (
            self.root.winfo_x()
            + (self.root.winfo_width() - self.statistics_window.winfo_width()) // 2
        )
        y = (
            self.root.winfo_y()
            + (self.root.winfo_height() - self.statistics_window.winfo_height()) // 2
        )
        self.statistics_window.geometry(f"+{x}+{y}")

        self.statistics_frame = tk.Frame(self.statistics_window)
        self.statistics_frame.grid(
            column=0, row=0, sticky=(tk.N, tk.W, tk.E, tk.S), padx=20, pady=10
        )
        self.weight_change_label = ttk.Label(self.statistics_frame, font=("Arial", 12))
        self.weight_change_label.grid(
            column=0, row=0, sticky=(tk.N, tk.S), padx=5, pady=5
        )
        self.update_weight_change_label()

    def add_mark(self, weight: float):
        if self.weight_validation(weight):
            self.graph.add_mark(
                datetime.strptime(self.date_label.cget("text"), f"%d.%m.%y\n%H:%M:%S"),
                weight,
            )
            self.update_graph()

    def remove_last_mark(self):
        if len(self.graph.marks) != 0:
            self.graph.remove_last_mark()
            self.update_graph()

    def show_clear_all_window(self):
        self.clear_window = tk.Toplevel(self.root)
        self.clear_window.grab_set()
        self.clear_window.title("Сlearing the graph")
        self.clear_window.resizable(False, False)
        self.clear_window.update()
        x = (
            self.root.winfo_x()
            + (self.root.winfo_width() - self.clear_window.winfo_width()) // 2
        )
        y = (
            self.root.winfo_y()
            + (self.root.winfo_height() - self.clear_window.winfo_height()) // 2
        )
        self.clear_window.geometry(f"+{x}+{y}")

        self.clear_window_frame = tk.Frame(self.clear_window)
        self.clear_window_frame.grid(
            column=0, row=0, sticky=(tk.N, tk.W, tk.E, tk.S), padx=20, pady=10
        )
        self.are_you_sure_label = ttk.Label(
            self.clear_window_frame, font=("Arial", 12), text="Are you sure?"
        )
        self.are_you_sure_label.grid(
            column=0, row=0, sticky=(tk.N, tk.S), padx=5, pady=5, columnspan=2
        )
        self.yes_button = ttk.Button(
            self.clear_window_frame,
            text="Yes",
            command=lambda: self.clear_all(),
        )
        self.yes_button.grid(column=0, row=1, sticky=(tk.N, tk.S), padx=5, pady=5)
        self.no_button = ttk.Button(
            self.clear_window_frame,
            text="No",
            command=lambda: self.clear_window.destroy(),
        )
        self.no_button.grid(
            column=1, row=1, sticky=(tk.N, tk.W, tk.E, tk.S), padx=5, pady=5
        )

    def clear_all(self):
        self.graph.remove_all_marks()
        self.update_graph()
        self.clear_window.destroy()

    def weight_validation(self, weight):
        try:
            float_value = float(weight)
            return float_value > 0
        except (ValueError, TypeError):
            return False

    def save_data(self):
        json_data = self.graph.to_json()
        with open(self.file_path, "w") as file:
            file.write(json_data)

    def load_data(self):
        try:
            with open(self.file_path, "r") as file:
                json_data = file.read()
            self.graph = GraphMaker.from_json(json_data)
            self.update_graph()
        except FileNotFoundError:
            self.update_graph()

    def run(self):
        self.root.mainloop()


if __name__ == "__main__":
    WeightTrackerGUI().run()
