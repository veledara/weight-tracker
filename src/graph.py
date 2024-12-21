import json
from matplotlib.figure import Figure
from typing import List, Optional
from datetime import datetime
import matplotlib as mpl

# Можно применить стиль
mpl.rcParams['axes.facecolor'] = '#f7f7f7'
mpl.rcParams['figure.facecolor'] = '#eaeaea'
mpl.rcParams['axes.grid'] = True
mpl.rcParams['grid.color'] = 'gray'
mpl.rcParams['grid.linestyle'] = '--'
mpl.rcParams['grid.alpha'] = 0.5
mpl.rcParams['lines.linewidth'] = 2
mpl.rcParams['lines.markersize'] = 8
mpl.rcParams['lines.marker'] = 'o'
mpl.rcParams['lines.color'] = 'red'

class Mark:
    date: datetime
    weight: float

    def __init__(self, date: datetime, weight: float) -> None:
        self.date = date
        self.weight = float(weight)

    def __repr__(self) -> str:
        return f"Date: {self.date}, Weight: {self.weight}"


class GraphMaker:
    marks: List[Mark]
    fig: Figure
    target_weight: Optional[float]

    def __init__(self) -> None:
        self.marks = []
        self.target_weight = None
        self.fig = Figure(figsize=(8, 4), dpi=100)
        self.ax = self.fig.add_subplot(111)
        self.update_axes()

    def update_axes(self) -> None:
        self.ax.clear()
        self.ax.set_xlabel("Time")
        self.ax.set_ylabel("Weight")
        self.ax.set_title("Weight Graph")
        self.ax.grid(True)

        if self.marks:
            self.ax.plot(
                [mark.date for mark in self.marks],
                [mark.weight for mark in self.marks],
                color="red",
                marker="o",
                linewidth=2,
                markersize=6,
                label="Weight"
            )

        # Отображение целевого веса
        if self.target_weight is not None:
            self.ax.axhline(
                y=self.target_weight,
                color="blue",
                linestyle="--",
                label=f"Target Weight: {self.target_weight} kg"
            )

        # Если что-то есть на легенде, показываем её
        if self.marks or self.target_weight is not None:
            self.ax.legend()

    def set_target_weight(self, weight: float) -> None:
        self.target_weight = float(weight)

    def add_mark(self, date: datetime, weight: float) -> None:
        self.marks.append(Mark(date, weight))

    def remove_last_mark(self) -> None:
        if self.marks:
            self.marks.pop()

    def remove_all_marks(self) -> None:
        self.marks = []

    def get_weight_on_start(self) -> float:
        return self.marks[0].weight if self.marks else 0.0

    def get_current_weight(self) -> float:
        return self.marks[-1].weight if self.marks else 0.0

    def show_weight_change(self) -> float:
        if len(self.marks) > 1:
            return round(self.get_weight_on_start() - self.get_current_weight(), 1)
        return 0.0

    def to_json(self) -> str:
        data = {
            "marks": [
                (mark.date.strftime(f"%d.%m.%y\n%H:%M:%S"), mark.weight)
                for mark in self.marks
            ],
            "target_weight": self.target_weight
        }
        return json.dumps(data)

    @classmethod
    def from_json(cls, json_str: str) -> "GraphMaker":
        data = json.loads(json_str)
        graph = cls()
        for date_str, weight in data.get("marks", []):
            date = datetime.strptime(date_str, f"%d.%m.%y\n%H:%M:%S")
            graph.add_mark(date, weight)
        graph.target_weight = data.get("target_weight", None)
        return graph

    def __repr__(self) -> str:
        return f"Marks are {self.marks}, Target: {self.target_weight}"
