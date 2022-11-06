import requests
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np 
import random
from tqdm import tqdm 

ethenicshirtParentData = []
counter = 0
for i in tqdm(range(50), desc = 'scraping ethenic') : 
    url = "https://paytmmall.com/shop/search?q=formal%20shirt&from=organic&child_site_id=6&site_id=2&category=9628&page="+str(i+1)
    page = requests.get(url)
    htmlContent = page.content
    soup = BeautifulSoup(htmlContent, 'html.parser')
    ethenicshirtImageDiv = soup.find_all("div", {"class" : "_3nWP"})
    for ethenicshirtImage in ethenicshirtImageDiv : 
        childList = []
        image = ethenicshirtImage.find('img')['src']
        # print(image)
        childList.append(counter)
        childList.append(image)
        counter += 1 

        ethenicshirtParentData.append(childList)

df = pd.DataFrame(ethenicshirtParentData, columns = ['index', 'link'])
path = "../data/ethenic/"
df.to_csv(path + 'ethenicshirtImage.csv', encoding='utf-8', index= False)
print(len(df))