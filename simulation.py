from typing import Optional, Union

from process import Process
from queue import Queue, PriorityQueue
from copy import deepcopy

MAX_CPU_TIME = 20000

def delete_from_queue(queue: PriorityQueue, pid: int):
    p_index = -1
    for i, t_p in enumerate(queue.queue):
        _, p = t_p
        if p.pid == pid:
            p_index = i
    if p_index >= 0:
        del queue.queue[p_index]


class GanttChart:
    def __init__(self, pid: int, start_time: int, end_time: int, algo: str):
        self.start_time = start_time
        self.end_time = end_time
        self.pid = pid
        self.algo = algo


class Simulator:
    current_process: Optional[Process]
    prev_process: Optional[Process]
    gantt_chart: list[GanttChart]

    def __init__(self, processes: list[Process], q1: int, q2: int, alpha: float):
        self.current_time = 0
        self.processes = processes
        self.q1 = q1
        self.q2 = q2
        self.alpha = alpha
        self.current_process = None
        self.prev_process = None
        self.queue1: Queue[Process] = Queue()
        self.queue2: Queue[Process] = Queue()
        # PriorityQueue was used to always arrange process based on minimum remaining cpu bursts
        self.queue3: PriorityQueue[tuple[int, Process]] = PriorityQueue()
        self.queue4: Queue[Process] = Queue()
        self.io_queue: Queue[Process] = Queue()
        self.round_robin_1_process_total_cpu_duration_for_burst = {p.pid: 0 for p in self.processes}
        self.round_robin_2_process_total_cpu_duration_for_burst = {p.pid: 0 for p in self.processes}
        self.round_robin_2_process_burst_cpu_duration = {p.pid: 0 for p in self.processes}
        self.processes_start_time = {p.pid: 0 for p in self.processes}
        self.gantt_chart: list[GanttChart] = []
        self.queues_per_time = {}
        self.logs = []
        self.recent_queue_per_process: dict[int, Union[Queue, PriorityQueue]] = {p.pid: None for p in self.processes}
        self.free_cpu_time = 0
        if self.current_process is not None:
            self.current_process.predicted_cpu_bursts(self.a)

    def run_round_robin_1(self):
        # get process in queue
        self.current_process = self.queue1.get()

        #capture start time of process
        if self.current_process.start_time == -1:
            self.current_process.start_time = self.current_time

        # get current burst
        current_burst = self.current_process.cpu_burst_duration[self.current_process.current_cpu_burst_index]
        current_burst_start = self.current_time
        self.add_to_log(
            f"[Round Robin 1/{self.current_time}] processing for process {self.current_process.pid}, at {self.current_time}")
        while current_burst > -1:
            if current_burst == 0:
                self.gantt_chart.append(
                    GanttChart(self.current_process.pid, current_burst_start, self.current_time, "RR1"))
                # total cpu time for this burst
                self.round_robin_1_process_total_cpu_duration_for_burst[self.current_process.pid] = 0
                # all burst are done terminate process
                if self.current_process.is_cpu_bursts_completed():
                    self.current_process.terminate(self.current_time)
                    self.add_to_log(
                        f"[Round Robin 1/{self.current_time}] process {self.current_process.pid} finished all bursts at {self.current_time}")
                else: # this cpu burst finished, add it to IO queue and block the process
                    self.current_process.state = "blocked"
                    self.current_process.current_cpu_burst_index += 1
                    self.recent_queue_per_process[self.current_process.pid] = self.queue1
                    self.io_queue.put(self.current_process)
                    self.add_to_log(
                        f"[Round Robin 1/{self.current_time}] process {self.current_process.pid} finished current burst {self.current_process.current_cpu_burst_index} at {self.current_time}, adding to IO Queue")
                break
                #  total cpu duration equals quantum * 10 limit, add it to next queue
            elif current_burst > 0 and self.round_robin_1_process_total_cpu_duration_for_burst[
                self.current_process.pid] == 10 * self.q1:
                self.round_robin_1_process_total_cpu_duration_for_burst[self.current_process.pid] = 0
                self.current_process.state = "ready"
                self.add_to_log(
                    f"[Round Robin 1/{self.current_time}] process {self.current_process.pid} finished its limit at {self.current_time}, "
                    f"adding to next queue")
                # add it tp next queue
                self.queue2.put(self.current_process)
                self.gantt_chart.append(
                    GanttChart(self.current_process.pid, current_burst_start, self.current_time, "RR1"))
                break
            #time quantum finished for this cpu, but it back to queue, and allow other process to work
            elif current_burst > 0 and self.current_time == current_burst_start + self.q1:
                self.current_process.state = "ready"
                # add it back to queue1
                self.queue1.put(self.current_process)
                self.add_to_log(
                    f"[Round Robin 1/{self.current_time}] process {self.current_process.pid} finished it's time quanta at {self.current_time}")
                self.gantt_chart.append(
                    GanttChart(self.current_process.pid, current_burst_start, self.current_time, "RR1"))
                break
            else:
                # process this burst and set state as running
                current_burst -= 1
                self.current_process.cpu_burst_duration[self.current_process.current_cpu_burst_index] = current_burst
                self.tick()
                self.round_robin_1_process_total_cpu_duration_for_burst[self.current_process.pid] += 1
                self.current_process.state = "running"

    def run_round_robin_2(self):
        # get process from queue2 without removing it
        self.current_process = self.queue2.queue[0]
        self.current_process.state = "running"
        # increase burst time duration
        current_burst = self.current_process.cpu_burst_duration[self.current_process.current_cpu_burst_index]
        self.add_to_log(
            f"[Round Robin 2/{self.current_time}] processing for process {self.current_process.pid}, at {self.current_time}")
        current_burst -= 1
        self.current_process.cpu_burst_duration[self.current_process.current_cpu_burst_index] = current_burst
        start_time = self.processes_start_time[self.current_process.pid]
        # capture start time
        if start_time == 0:
            self.processes_start_time[self.current_process.pid] = self.current_time
            start_time = self.current_time
        self.tick()
        self.round_robin_2_process_total_cpu_duration_for_burst[self.current_process.pid] += 1
        self.round_robin_2_process_burst_cpu_duration[self.current_process.pid] += 1

        if current_burst == 0:
            # this burst finished remove it from queue
            self.queue2.queue.remove(self.current_process)
            # all process finished remove it from queue
            if self.current_process.is_cpu_bursts_completed():
                self.current_process.terminate(self.current_time)
                self.add_to_log(
                    f"[Round Robin 2/{self.current_time}] process {self.current_process.pid} finished all bursts at {self.current_time}")
            else:
                # this burst finished, mark process blocked and it to IO queue
                self.current_process.state = "blocked"
                self.current_process.current_cpu_burst_index += 1
                self.recent_queue_per_process[self.current_process.pid] = self.queue2
                self.io_queue.put(self.current_process)
                self.add_to_log(
                    f"[Round Robin 2/{self.current_time}] process {self.current_process.pid} finished current burst {self.current_process.current_cpu_burst_index} at {self.current_time}, adding to IO Queue")
            self.round_robin_2_process_burst_cpu_duration[self.current_process.pid] = 0
            self.round_robin_2_process_total_cpu_duration_for_burst[self.current_process.pid] = 0
            self.gantt_chart.append(GanttChart(self.current_process.pid, start_time, self.current_time, "RR2"))
            self.processes_start_time[self.current_process.pid] = 0
            # total quantum for this process reached limit, remove it from this queue, and add it to next queue
        elif current_burst > 0 and self.round_robin_2_process_total_cpu_duration_for_burst[
            self.current_process.pid] == 10 * self.q2:
            self.round_robin_2_process_total_cpu_duration_for_burst[self.current_process.pid] = 0
            self.round_robin_2_process_burst_cpu_duration[self.current_process.pid] = 0
            self.current_process.state = "ready"
            self.add_to_log(
                f"[Round Robin 2/{self.current_time}] process {self.current_process.pid} finished its limit at {self.current_time}, "
                f"adding to next queue")
            # remove from queue2
            self.queue2.queue.remove(self.current_process)
            # add it to queue3
            self.queue3.put((self.current_process.total_remaining_cpu_bursts(), self.current_process))
            self.gantt_chart.append(GanttChart(self.current_process.pid, start_time, self.current_time, "RR2"))
            self.processes_start_time[self.current_process.pid] = 0
            # time auantum finished for this process remove it from this queue, and add it to the end again
        elif current_burst > 0 and self.round_robin_2_process_burst_cpu_duration[self.current_process.pid] == self.q2:
            self.round_robin_2_process_burst_cpu_duration[self.current_process.pid] = 0
            self.current_process.state = "ready"
            self.queue2.queue.remove(self.current_process)
            self.queue2.put(self.current_process)
            self.round_robin_2_process_burst_cpu_duration[self.current_process.pid] = 0
            self.add_to_log(
                f"[Round Robin 2/{self.current_time}] process {self.current_process.pid} finished it's time quanta at {self.current_time}")
            self.gantt_chart.append(GanttChart(self.current_process.pid, start_time, self.current_time, "RR2"))
            self.processes_start_time[self.current_process.pid] = 0
        else:
            # lower priority put it on ready
            self.current_process.state = "ready"

    def run_first_come_first_served(self):
        # get process without removing
        self.current_process = self.queue4.queue[0]
        self.current_process.state = "running"
        start_time = self.processes_start_time[self.current_process.pid]
        if start_time == 0:
            self.processes_start_time[self.current_process.pid] = self.current_time
            start_time = self.current_time
        self.add_to_log(
            f"[FCFS {self.current_process.pid}/{self.current_time}] processing for {self.current_process.pid}, at {self.current_time}")
        current_burst = self.current_process.cpu_burst_duration[self.current_process.current_cpu_burst_index]
        current_burst -= 1
        self.current_process.cpu_burst_duration[self.current_process.current_cpu_burst_index] = current_burst
        self.tick()
        # finished current burst
        if current_burst == 0:
            # remove oit from queue4
            self.queue4.get()
            if self.current_process.is_cpu_bursts_completed():
                self.current_process.terminate(self.current_time)
                self.add_to_log(
                    f"[FCFS {self.current_process.pid}/{self.current_time}] process {self.current_process.pid} finished all bursts at {self.current_time}")
            else:
                # add it to IO queue and mark it as blocked
                self.current_process.state = "blocked"
                self.current_process.current_cpu_burst_index += 1
                self.recent_queue_per_process[self.current_process.pid] = self.queue4
                self.io_queue.put(self.current_process)
                self.add_to_log(
                    f"[FCFS {self.current_process.pid}/{self.current_time}] process {self.current_process.pid} finished current burst {self.current_process.current_cpu_burst_index} at {self.current_time}, adding to IO Queue")
            self.gantt_chart.append(GanttChart(self.current_process.pid, start_time, self.current_time, "FCFS"))
            self.processes_start_time[self.current_process.pid] = 0
        elif current_burst > 0:
            # mark it as ready
            self.current_process.state = "ready"

    def run_shortest_remaining_time_first(self):
        # get process withput removing it
        self.current_process = self.queue3.queue[0][1]
        start_time = self.processes_start_time[self.current_process.pid]
        # capture time
        if start_time == 0:
            self.processes_start_time[self.current_process.pid] = self.current_time
            start_time = self.current_time

        # preempted happened, add it to queue4 and remove it from current queue if it equals 3
        if self.prev_process is not None and not self.current_process.pid == self.prev_process.pid:
            self.prev_process.preempted += 1
            # preempted equals 3 delete from this queue and add it to queue3
            if self.prev_process.preempted == 3:
                self.add_to_log(
                    f"[SRTF {self.current_process.pid}/{self.current_time}] process {self.prev_process.pid} was preemted 3 times, at {self.current_time}")
                delete_from_queue(self.queue3, self.prev_process.pid)
                self.queue4.put(self.prev_process)
                return
        #process this burst
        self.current_process.state = "running"
        self.prev_process = self.current_process
        self.add_to_log(
            f"[SRTF {self.current_process.pid}/{self.current_time}] processing for {self.current_process.pid}, at {self.current_time}")
        current_burst = self.current_process.cpu_burst_duration[self.current_process.current_cpu_burst_index]
        current_burst -= 1
        self.current_process.cpu_burst_duration[self.current_process.current_cpu_burst_index] = current_burst
        self.tick()
        if current_burst == 0:
            # delete from queue
            delete_from_queue(self.queue3, self.current_process.pid)
            self.prev_process = None
            # all bursts finished
            if self.current_process.is_cpu_bursts_completed():
                self.current_process.terminate(self.current_time)
                self.add_to_log(
                    f"[SRTF {self.current_process.pid}/{self.current_time}] process {self.current_process.pid} finished all bursts at {self.current_time}")
            else:
                # this burst finished makr it blocked and add it to IO queue
                self.current_process.state = "blocked"
                self.current_process.current_cpu_burst_index += 1
                self.recent_queue_per_process[self.current_process.pid] = self.queue3
                self.io_queue.put(self.current_process)
                self.add_to_log(
                    f"[SRTF {self.current_process.pid}/{self.current_time}] process {self.current_process.pid} finished current burst {self.current_process.current_cpu_burst_index} at {self.current_time}, adding to IO Queue")
            self.gantt_chart.append(GanttChart(self.current_process.pid, start_time, self.current_time, "SRTF"))
            self.processes_start_time[self.current_process.pid] = 0
        elif current_burst > 0:
            self.current_process.state = "ready"

    def check_arrived_processes(self):
        # find which process to run, set state as new_added
        for process in self.processes:
            if process.state == "new" and process.arrival_time <= self.current_time:
                process.state = "new_added"
                self.queue1.put(process)

    def check_io_queue(self):
        # check which processes finished thier IO, if finished return it back to it's queue
        indexes_to_remove = []
        for i, process in enumerate(self.io_queue.queue):
            current_io_index = process.current_io_burst_index
            try:
                process.io_burst_duration[current_io_index] -= 1
            except IndexError:
                return
            # finished io return to queue
            if process.io_burst_duration[current_io_index] <= 0 and \
                    self.recent_queue_per_process[process.pid] is not None:
                self.add_to_log(
                    f"[IO] process {process.pid} finished IO at {self.current_time}, returning back to queue")
                process.current_io_burst_index += 1
                # mark it as ready and remove it
                process.state = "ready"
                indexes_to_remove.append(i)
                queue_to_add = self.recent_queue_per_process[process.pid]
                if queue_to_add == self.queue3:
                    self.queue3.put((process.total_remaining_cpu_bursts(), process))
                else:
                    self.recent_queue_per_process[process.pid].put(process)
        # remove from IO queue
        for index in indexes_to_remove:
            try:
                del self.io_queue.queue[index]
            except IndexError:
                pass

    # represents a cpu tick
    def tick(self):
        self.queues_per_time[self.current_time] = (
        deepcopy(self.queue1.queue), deepcopy(self.queue2.queue), deepcopy(self.queue3.queue),
        deepcopy(self.queue4.queue))
        self.current_time += 1
        # check which process arrived and add them to queue1
        self.check_arrived_processes()
        # check which processes finished IO processing
        self.check_io_queue()

    def add_to_log(self, message: str):
        print(message)
        self.logs.append(message)

    def run(self):
        # run simulation until all processes are terminated and all queues are empty
        while (not all(p.is_terminated() for p in self.processes) or not self.queue1.empty() or \
                not self.queue2.empty() or not self.queue3.empty() or not self.queue4.empty()) and not self.current_time >= MAX_CPU_TIME:
            self.check_arrived_processes()
            # start with queue1, if empty go to next queue2, and so on, queue1 highest priority, queue4 lowest priority
            if not self.queue1.empty():
                self.run_round_robin_1()
            elif not self.queue2.empty():
                self.run_round_robin_2()
            elif not self.queue3.empty():
                self.run_shortest_remaining_time_first()
            elif not self.queue4.empty():
                self.run_first_come_first_served()
            else:
                # no queue to be processed
                self.tick()
                self.free_cpu_time += 1

    def cpu_utilization(self):
        # calculate cpu utilization
        working_time = self.current_time - self.free_cpu_time
        if self.current_time > 0:
            return round((working_time / self.current_time) * 100, 1)
        return 0

    def avg_waiting_time(self):
        # calculate average time
        return round(sum(p.waiting_time() for p in self.processes) / len(self.processes), 1)