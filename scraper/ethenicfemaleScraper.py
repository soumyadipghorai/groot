import requests
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np 
import random
from tqdm import tqdm 

ethenicshirtFemaleParentData = []
counter = 0
for i in tqdm(range(3), desc = 'scraping ethenic female') : 
    url = "https://paytmmall.com/shop/search?q=formal%20shirt%20female&from=organic&child_site_id=6&site_id=2&category=5875&page="+str(i+1)
    page = requests.get(url)
    htmlContent = page.content
    soup = BeautifulSoup(htmlContent, 'html.parser')
    # print(soup)
    ethenicshirtFemaleImageDiv = soup.find_all("div", {"class" : "_3nWP"})
    for ethenicshirtFemaleImage in ethenicshirtFemaleImageDiv : 
        childList = []
        image = ethenicshirtFemaleImage.find('img')['src']
        # print(image)
        childList.append(counter)
        childList.append(image)
        counter += 1 

        ethenicshirtFemaleParentData.append(childList)

df = pd.DataFrame(ethenicshirtFemaleParentData, columns = ['index', 'link'])
path = "../data/ethenic/"
df.to_csv(path + 'ethenicshirtFemaleImage.csv', encoding='utf-8', index= False)
print(len(df))