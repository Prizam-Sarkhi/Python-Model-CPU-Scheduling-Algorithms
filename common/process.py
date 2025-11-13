from dataclasses import dataclass, field

@dataclass
class Process:
    pid: int
    arrival_time: int
    burst_time: int
    priority: int
    remaining_time: int = field(init=False)
    start_time: int = -1
    completion_time: int = -1
    wait_time: int = 0
    response_time: int = -1

    def __post_init__(self):
        self.remaining_time = int(self.burst_time)
