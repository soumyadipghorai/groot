import json
import requests
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np 
import random
from tqdm import tqdm 

laptopParentData = []
counter = 0
for i in tqdm(range(24), desc= "scraping laptop") : 
    url = "https://sathya.in/laptop?i="+str(i+1)
    page = requests.get(url)
    htmlContent = page.content
    soup = BeautifulSoup(htmlContent, 'html.parser')
    laptopImageDiv = soup.find_all("div", {"class" : "art-picture-block"})
    for laptopImage in laptopImageDiv : 
        childList = []
        image = laptopImage.find('a').find('img')['src']
        childList.append(counter)
        childList.append('https:'+image)
        counter += 1 

        laptopParentData.append(childList)

df = pd.DataFrame(laptopParentData, columns = ['index', 'link'])
path = "../data/laptop/"
df.to_csv(path + 'laptopImage.csv', encoding='utf-8', index= False)