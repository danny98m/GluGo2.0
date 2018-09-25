import pandas as pd
df = pd.read_json('test_kates_data.json')
df.to_csv('test_kates_data.csv')

