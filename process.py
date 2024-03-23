class Process:
    pid: int
    arrival_time: int
    number_of_cpu_bursts: int
    io_burst_duration: list[int]
    cpu_burst_duration: list[int]
    state: str
    preempted: int

    def __init__(self, pid: int = None, arrival_time: int = None, number_of_cpu_bursts: int = None,
                 io_burst_duration: list[int] = None, cpu_burst_duration: list[int] = None):
        self.pid = pid
        self.arrival_time = arrival_time
        self.number_of_cpu_bursts = number_of_cpu_bursts
        self.io_burst_duration = io_burst_duration or []
        self.cpu_burst_duration = cpu_burst_duration or []
        self.state = "new" # new, new_added, ready, terminated, blocked
        self.preempted = 0
        self.current_cpu_burst_index = 0
        self.current_io_burst_index = 0
        # start/end time for the process
        self.start_time = -1
        self.complete_time = -1

    def __str__(self):
        return f"{self.pid}-{self.state}"

    def __repr__(self):
        return self.__str__()

    def terminate(self, complete_time: int):
        self.state = "terminated"
        self.current_cpu_burst_index = 0
        self.current_io_burst_index = 0
        self.complete_time = complete_time

    def is_terminated(self):
        return self.state == "terminated"

    def total_remaining_cpu_bursts(self):
        return sum(self.cpu_burst_duration)

    def is_cpu_bursts_completed(self):
        return self.current_cpu_burst_index == len(self.cpu_burst_duration) - 1

    def waiting_time(self):
        return self.start_time - self.arrival_time

    def turnaround_time(self):
        return self.complete_time - self.arrival_time

    def predicted_cpu_bursts(self, a: float):
        predicted = []
        prev_burst = 0
        for cpu in self.cpu_burst_duration:
            next_burst = a * cpu + (1.0 - a) * prev_burst
            prev_burst = next_burst
            predicted.append(next_burst)
            return sum(predicted)