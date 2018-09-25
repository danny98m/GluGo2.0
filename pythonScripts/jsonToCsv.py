import pandas as pd

def main():
    df = pd.read_json('test_kates_data.json')
    df.to_csv('test_kates_data.csv')

if __name__ == "__main__":
    main()

