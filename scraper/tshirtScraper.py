import requests
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np 
import random
from tqdm import tqdm 

tshirtParentData = []
counter = 0
for i in tqdm(range(50), desc = 'scraping tshort') : 
    url = "https://paytmmall.com/men-t-shirts-glpid-5030?page="+str(i+1)+"&category=5030"
    page = requests.get(url)
    htmlContent = page.content
    soup = BeautifulSoup(htmlContent, 'html.parser')
    # print(soup)
    tshirtImageDiv = soup.find_all("div", {"class" : "_3nWP"})
    for tshirtImage in tshirtImageDiv : 
        childList = []
        image = tshirtImage.find('img')['src']
        # print(image)
        childList.append(counter)
        childList.append(image)
        counter += 1 

        tshirtParentData.append(childList)

df = pd.DataFrame(tshirtParentData, columns = ['index', 'link'])
path = "../data/tshirt/"
df.to_csv(path + 'tshirtImage.csv', encoding='utf-8', index= False)
print(len(df))