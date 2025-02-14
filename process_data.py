import pandas as pd

if __name__ == '__main__':
    weather_data = pd.read_table("aquacrop/data/810018.txt")
    weather_data.to_excel("临淄区.xlsx", index=False)
    data = pd.read_excel("临淄区.xlsx")
    data.to_csv('weather.txt', sep='\t', index=False)