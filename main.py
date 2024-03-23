import math
import sys
from copy import deepcopy
from random import randint

from PySide6.QtGui import QColor, QFont, QStandardItemModel, QStandardItem

from process import Process
from simulation import Simulator

from PySide6.QtWidgets import QApplication, QMainWindow, QTableWidgetItem, QFileDialog, QDialog
from PySide6.QtCore import Qt, QSize
from gui.main_window import Ui_MainWindow
from gui.results_dialog import Ui_results_dialog


class ResultsDialog(QDialog, Ui_results_dialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)


def generate_color():
    r = randint(0, 255)
    g = randint(0, 255)
    b = randint(0, 255)
    rand_color = (r, g, b)
    return rand_color


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui_results = ResultsDialog()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.simulator = None
        self.processes: list[Process] = []
        self.original_processes: list[Process] = []
        self.ui.file_radio.toggled.connect(self.file_radio_toggled)
        self.ui.save_processes.clicked.connect(self.save_to_file)
        self.ui.generate_radio.toggled.connect(self.generate_radio_toggled)
        self.ui.run_button.clicked.connect(self.run)
        self.ui.choose_file.clicked.connect(self.read_from_file)
        self.ui.main_widget.setCurrentIndex(1)
        self.ui.file_radio.setChecked(True)

    def file_radio_toggled(self):
        self.ui.generate_radio.setChecked(not self.ui.file_radio.isChecked())
        self.ui.run_button.setEnabled(True)
        self.ui.main_widget.setCurrentIndex(1)

    def generate_radio_toggled(self):
        self.ui.file_radio.setChecked(not self.ui.generate_radio.isChecked())
        self.ui.run_button.setEnabled(True)
        self.ui.main_widget.setCurrentIndex(0)

    def run(self):
        q1 = int(self.ui.q1.text())
        q2 = int(self.ui.q2.text())
        alpha = float(self.ui.alpha.text())
        if self.ui.generate_radio.isChecked():
            self.generate_processes()

        self.simulator = Simulator(self.processes, q1, q2, alpha)
        self.simulator.run()
        self.show_results()

    def draw_gantt_chart(self):
        table = self.ui_results.guant_chart
        colors_per_process = {}
        table.resizeColumnsToContents()
        table.resizeRowsToContents()
        table.setRowCount(math.ceil(len(self.simulator.gantt_chart)/8) + 1)
        table.setColumnCount(8)
        for process in self.processes:
            colors_per_process[process.pid] = generate_color()
        for column, gg in enumerate(self.simulator.gantt_chart):
            row = math.floor(column / 8)
            col = column % 8
            item = QTableWidgetItem(f"{gg.start_time}-{gg.end_time}  {gg.pid}({gg.algo})")
            item.setTextAlignment(Qt.AlignmentFlag.AlignLeft)
            item.setBackground(QColor(*colors_per_process[gg.pid]))
            table.setItem(row, col, item)
            item.setSizeHint(QSize(150, 50))


    def show_logs(self):
        log_view = self.ui_results.log
        log_view.resizeColumnsToContents()
        log_view.resizeRowsToContents()
        log_view.setRowCount(len(self.simulator.logs))
        log_view.setColumnCount(1)
        for i, log in enumerate(self.simulator.logs):
            log_item = QTableWidgetItem(log)
            log_item.setTextAlignment(Qt.AlignmentFlag.AlignLeft)
            log_view.setItem(i, 0, log_item)
            log_view.setColumnWidth(i, 600)

    def show_results(self):
        self.ui_results.cpu_utilization.setText(f"CPU Utilization: {self.simulator.cpu_utilization()}%")
        self.ui_results.average_waiting.setText(f"Average Waiting Time: {self.simulator.avg_waiting_time()}")
        table = self.ui_results.results_table
        table.resizeColumnsToContents()
        table.resizeRowsToContents()
        headers = ["PID", "Arrival Time", "Start Time", "End Time", "Waiting Time", "Turn Around Time", "CPU Bursts", "IO Bursts"]
        table.setRowCount(len(self.processes))
        table.setColumnCount(len(headers))
        original_processes = sorted(self.original_processes, key=lambda p: p.pid)
        processes = sorted(self.processes, key=lambda p: p.pid)
        for row, process in enumerate(zip(original_processes, processes)):
            o, p = process
            for column, item in enumerate([p.pid, p.arrival_time, p.start_time,
                                           p.complete_time, p.waiting_time(), p.turnaround_time(), ", ".join(map(str, o.cpu_burst_duration)), ", ".join(map(str, o.io_burst_duration))]):
                new_item = QTableWidgetItem(str(item))
                table.setItem(row, column, new_item)
        table.setHorizontalHeaderLabels(headers)
        self.draw_gantt_chart()
        self.show_logs()
        self.ui_results.exec()

    def read_from_file(self):
        file_name, _ = QFileDialog.getOpenFileName(self, "Choose File", filter="*.txt")
        if not file_name:
            return
        self.ui.file_name.setText(f"File Name: {file_name}")
        self.ui.run_button.setEnabled(True)
        print("Reading processes from file")
        with open(file_name, "r") as f:
            lines = f.readlines()
            for line in lines:
                if not line or line == "\n" or line.startswith("#"):
                    continue
                values = line.strip().split("\t")
                process = Process()
                process.pid = int(values[0])
                process.arrival_time = int(values[1])
                bursts = values[2:]
                for i, burst in enumerate(bursts):
                    burst = int(burst)
                    if i % 2 == 0:
                        process.cpu_burst_duration.append(burst)
                    else:
                        process.io_burst_duration.append(burst)
                self.processes.append(process)
        self.processes = sorted(self.processes, key=lambda p: p.arrival_time)
        self.original_processes = deepcopy(self.processes)

    def generate_processes(self):
        if not len(self.original_processes) == 0:
            return
        print("generating processes")
        max_number_of_processes = int(self.ui.max_number_of_processes.text())
        max_arrival_time = int(self.ui.max_arrival_time.text())
        max_no_of_cpu_bursts = int(self.ui.max_no_of_cpu_bursts.text())
        max_io_burst_duration = int(self.ui.max_io_burst_duration.text())
        min_io_burst_duration = int(self.ui.min_io_burst_duration.text())
        max_cpu_burst_duration = int(self.ui.max_cpu_burst_duration.text())
        min_cpu_burst_duration = int(self.ui.min_cpu_burst_duration.text())
        number_of_processes = randint(2, max_number_of_processes)

        print(f"number of processes {number_of_processes}")
        for index in range(number_of_processes):
            new_process = Process()
            new_process.pid = index
            new_process.arrival_time = randint(0, max_arrival_time)
            new_process.number_of_cpu_bursts = randint(2, max_no_of_cpu_bursts)
            for i in range(new_process.number_of_cpu_bursts):
                new_process.cpu_burst_duration.append(randint(min_cpu_burst_duration, max_cpu_burst_duration))
            max_number_of_io_burst = new_process.number_of_cpu_bursts - 1
            for i in range(max_number_of_io_burst):
                new_process.io_burst_duration.append(randint(min_io_burst_duration, max_io_burst_duration))
            self.processes.append(new_process)
        self.processes = sorted(self.processes, key=lambda p: p.arrival_time)
        self.original_processes = deepcopy(self.processes)

    def save_to_file(self):
        if len(self.original_processes) == 0:
            self.generate_processes()
        print("saving processes to file")
        with open("saved_processes.txt", "w") as file:
            lines = []
            for process in self.original_processes:
                all_bursts = [x for pair in zip(process.io_burst_duration, process.cpu_burst_duration) for x in pair]
                all_bursts_str = "\t".join(map(str, all_bursts))
                process_str = f"{process.pid}\t{process.arrival_time}\t{all_bursts_str}\n"
                lines.append(process_str)
            file.writelines(lines)


app = QApplication(sys.argv)
window = MainWindow()
window.show()
app.exec()
