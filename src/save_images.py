!pip install urllib.request


import pandas as pd
import urllib.request

tshirt_df = pd.read_csv('D:\groot\notebooks\tshirtImage.csv')

for i in range(len(tshirt_df)):
    urllib.request.urlretrieve( tshirt_df['link'][i], f"{i}.jpg")