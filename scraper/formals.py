import requests
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np 
import random
from tqdm import tqdm 

formalshirtParentData = []
counter = 0
for i in tqdm(range(50), desc='scraping formals') : 
    url = "https://paytmmall.com/shop/search?q=formal%20shirt&from=organic&child_site_id=6&site_id=2&category=8544&page="+str(i+1)
    page = requests.get(url)
    htmlContent = page.content
    soup = BeautifulSoup(htmlContent, 'html.parser')
    # print(soup)
    formalshirtImageDiv = soup.find_all("div", {"class" : "_3nWP"})
    for formalshirtImage in formalshirtImageDiv : 
        childList = []
        image = formalshirtImage.find('img')['src']
        # print(image)
        childList.append(counter)
        childList.append(image)
        counter += 1 

        formalshirtParentData.append(childList)

df = pd.DataFrame(formalshirtParentData, columns = ['index', 'link'])
path = "../data/formals/"
df.to_csv(path + 'formalshirtImage.csv', encoding='utf-8', index= False)
print(len(df))