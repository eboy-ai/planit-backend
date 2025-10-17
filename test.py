import pandas as pd



cities_list = pd.read_excel('cities_list.xlsx')

# print(cities_list.head())
print(cities_list.head(1)['lon'])

