import numpy as np
from collections import deque
from common.workload_generator import generate_workload
from common.metrics import compute_metrics
from common.utils import export_csv
from algorithms.sjf import SJFScheduler

WORKLOADS = {
    "Light": {"process_count":100,"arrival_lambda":0.2,"burst_dist":("exponential",8),"priority_range":(1,10)},
    "Heavy": {"process_count":100,"arrival_lambda":1.0,"burst_dist":("exponential",40),"priority_range":(1,10)},
    "Mixed": {"process_count":100,"arrival_lambda":0.8,"burst_dist":("bimodal",(5,70,0.8)),"priority_range":(1,10)},
}
ITERATIONS=10
ALGO_NAME="SJF"

def run_algorithm(algo_class, workload_name, params):
    import copy
    results=[]
    for i in range(ITERATIONS):
        base=generate_workload(workload_name,params,seed=100+i)
        algo=algo_class()
        procs=copy.deepcopy(base)
        ready,completed=deque(),[]
        time=0; idx=0; cur=None
        while len(completed)<len(procs):
            while idx<len(procs) and procs[idx].arrival_time==time:
                ready.append(procs[idx]); idx+=1
            cur=algo.select(ready,cur)
            if cur:
                if cur.start_time==-1:
                    cur.start_time=time; cur.response_time=time-cur.arrival_time
                cur.remaining_time-=1
                for q in ready: q.wait_time+=1
                if hasattr(algo,'tick'): algo.tick()
                if cur.remaining_time<=0:
                    cur.completion_time=time+1; completed.append(cur); cur=None
            time+=1
        avg_tat,avg_wt,avg_rt=compute_metrics(completed)
        results.append({"Algorithm":ALGO_NAME, "Workload":workload_name,
                         "Avg_TAT":avg_tat,"Avg_WT":avg_wt,"Avg_RT":avg_rt})
    return results

if __name__=="__main__":
    allres=[]
    for w,p in WORKLOADS.items():
        allres.extend(run_algorithm(SJFScheduler,w,p))

    # Averaged per workload with Algorithm column
    avgdata=[]
    for w in WORKLOADS.keys():
        subset=[r for r in allres if r["Workload"]==w]
        avgdata.append({"Algorithm":ALGO_NAME,"Workload":w,
            "Avg_TAT":np.mean([r["Avg_TAT"] for r in subset]),
            "Avg_WT":np.mean([r["Avg_WT"] for r in subset]),
            "Avg_RT":np.mean([r["Avg_RT"] for r in subset])})

    # Export with desired column order
    export_csv(allres,"results/sjf_raw.csv",
               columns=["Algorithm","Workload","Avg_TAT","Avg_WT","Avg_RT"])
    export_csv(avgdata,"results/sjf_averaged.csv",
               columns=["Algorithm","Workload","Avg_TAT","Avg_WT","Avg_RT"])
    print("Saved results for SJF")
