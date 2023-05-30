from matplotlib.figure import Figure
from typing import List
from datetime import datetime


class Mark:
    date: datetime
    weight: float

    def __init__(self, date: datetime, weight: float) -> None:
        self.date = datetime.strptime(date, f"%d.%m.%y\n%H:%M:%S")
        self.weight = float(weight)

    def __repr__(self) -> str:
        return f"Date: {self.date}, Weight: {self.weight}"


class GraphMaker:
    marks: List[Mark]
    fig: Figure

    def __init__(self) -> None:
        self.marks = []
        self.fig = Figure(figsize=(8, 4), dpi=100, facecolor="lightgray")
        self.ax = self.fig.add_subplot(111)

        self.update_axes()

    def update_axes(self) -> None:
        self.ax.clear()
        self.ax.set_xlabel("Days")
        self.ax.set_ylabel("Weight")
        self.ax.set_title("Weight Statistics")
        self.ax.grid(True)
        self.ax.plot(
            [mark.date for mark in self.marks],
            [mark.weight for mark in self.marks],
            color="red",
            marker="o",
        )

    def add_mark(self, date: datetime, weight: float) -> None:
        self.marks.append(Mark(date, weight))

    def remove_last_mark(self) -> None:
        self.marks.pop()

    def get_weight_on_start(self) -> None:
        return self.marks[0].weight

    def get_current_weight(self) -> None:
        return self.marks[len(self.marks) - 1].weight

    def show_weight_change(self) -> None:
        return round(self.get_weight_on_start() - self.get_current_weight(), 1)

    def __repr__(self) -> str:
        return f"Marks are {self.marks}"


if __name__ == "__main__":
    graph = GraphMaker()
    current_time = datetime.now()
    graph.add_mark(datetime(2023, 1, 1), 70.6)
    print(graph)
