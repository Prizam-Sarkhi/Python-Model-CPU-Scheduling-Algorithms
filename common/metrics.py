import numpy as np

def compute_metrics(processes):
    tats, wts, rts = [], [], []
    for p in processes:
        tat = p.completion_time - p.arrival_time
        wt = tat - p.burst_time
        rt = p.response_time if p.response_time != -1 else (p.start_time - p.arrival_time if p.start_time != -1 else 0)
        tats.append(tat); wts.append(wt); rts.append(rt)
    tats, wts, rts = np.array(tats, dtype=float), np.array(wts, dtype=float), np.array(rts, dtype=float)
    avg_tat, avg_wt, avg_rt = np.mean(tats), np.mean(wts), np.mean(rts)
    return avg_tat, avg_wt, avg_rt
