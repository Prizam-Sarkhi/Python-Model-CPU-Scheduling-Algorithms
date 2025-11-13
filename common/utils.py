import pandas as pd, os

def export_csv(data, filename, columns=None):
    df = pd.DataFrame(data)
    if columns:
        df = df[columns]
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    df.to_csv(filename, index=False)
    return df
