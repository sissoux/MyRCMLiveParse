import pandas as pd

# Sample DataFrame
data = {
    'A': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
    'B': [0, 20, 40, 60, 80, 100, 120, 140, 160, 180]  # Assuming B is in seconds
}
df = pd.DataFrame(data)

# Convert column B to datetime
df['B'] = pd.to_datetime(df['B'], unit='s')

for d in df.rolling(window='40s', on='B', min_periods=1).A:
    print(d[-1]-d[0])

# print(df.assign(pace_5m=lambda d: d.rolling(window='40s', on='B', min_periods=1).A.mean()))
