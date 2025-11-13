import os, time, subprocess, pandas as pd

ALGO_ORDER_COLS = {
    "default": ["Algorithm","Workload","Avg_TAT","Avg_WT","Avg_RT"],
    "rr": ["Algorithm","Workload","TQ","Avg_TAT","Avg_WT","Avg_RT"]
}

def run_script(script):
    print(f"▶ Running {script} ...")
    start = time.time()
    subprocess.run(["python", script], check=True)
    end = time.time()
    print(f"✔ {script} completed in {end - start:.2f} seconds\n")
    return end - start

def reorder_cols(df, rr=False):
    cols = ALGO_ORDER_COLS["rr"] if rr else ALGO_ORDER_COLS["default"]
    # add missing cols if any
    for c in cols:
        if c not in df.columns:
            df[c] = "-" if c == "TQ" else None
    return df[cols]

def main():
    os.makedirs("results", exist_ok=True)
    algos = ["fcfs", "sjf", "priority", "rr"]
    runtimes = {}
    for algo in algos:
        runtimes[algo] = run_script(f"run_{algo}.py")

    raw_frames, avg_frames = [], []
    for algo in algos:
        raw_path = f"results/{algo}_raw.csv"
        avg_path = f"results/{algo}_averaged.csv"
        if os.path.exists(raw_path):
            df = pd.read_csv(raw_path)
            df = reorder_cols(df, rr=(algo=="rr"))
            raw_frames.append(df)
        if os.path.exists(avg_path):
            df = pd.read_csv(avg_path)
            df = reorder_cols(df, rr=(algo=="rr"))
            avg_frames.append(df)

    if raw_frames:
        pd.concat(raw_frames, ignore_index=True).to_csv("results/all_algorithms_raw.csv", index=False)
    if avg_frames:
        pd.concat(avg_frames, ignore_index=True).to_csv("results/all_algorithms_averaged.csv", index=False)

    print("\n✅ All algorithms finished!")
    print("📊 Combined summaries saved to:")
    print("   - results/all_algorithms_raw.csv")
    print("   - results/all_algorithms_averaged.csv\n")
    print("⏱ Runtime summary (seconds):")
    for k,v in runtimes.items():
        print(f"   {k.upper():<10} {v:.2f} s")

if __name__ == "__main__":
    main()
