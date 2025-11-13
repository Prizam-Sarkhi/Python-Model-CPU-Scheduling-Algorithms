import random, math, numpy as np
from .process import Process

def generate_arrivals_poisson(count, lam):
    arrivals = []
    t = 0.0
    for _ in range(count):
        inter = np.random.exponential(1.0 / lam) if lam > 0 else 0
        t += inter
        arrivals.append(int(math.floor(t)))
    return arrivals

def sample_burst(spec):
    typ = spec[0]
    if typ == "exponential":
        mean = spec[1]
        return max(1, int(round(np.random.exponential(mean))))
    elif typ == "bimodal":
        short_mean, long_mean, frac_short = spec[1]
        if random.random() < frac_short:
            return max(1, int(round(np.random.exponential(short_mean))))
        else:
            return max(1, int(round(np.random.exponential(long_mean))))
    else:
        raise ValueError("Unknown distribution type")

def generate_workload(name, params, seed=None):
    if seed:
        random.seed(seed); np.random.seed(seed)
    n = params["process_count"]
    lam = params["arrival_lambda"]
    burst_spec = params["burst_dist"]
    pr_low, pr_high = params["priority_range"]
    arrivals = generate_arrivals_poisson(n, lam)
    processes = []
    for i in range(n):
        p = Process(
            pid=i+1,
            arrival_time=arrivals[i],
            burst_time=sample_burst(burst_spec),
            priority=random.randint(pr_low, pr_high)
        )
        processes.append(p)
    processes.sort(key=lambda p: (p.arrival_time, p.pid))
    return processes
