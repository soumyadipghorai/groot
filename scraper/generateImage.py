import urllib.request
import pandas as pd
from tqdm import tqdm 

def generateImage(dataframe_path, path) : 
    df = pd.read_csv(dataframe_path)
    for i in tqdm(range(len(df)), desc = 'generating image') : 
        urllib.request.urlretrieve(df.link.iloc[i], path + str(i+1)+".jpg")

if __name__ == "__main__" : 
    tshirt_df_path = '../data/tshirt/tshirtImage.csv'
    tshirt_storing_path = '../data/tshirt/tshirtImages/tshirtImage'

    formals_df_path = '../data/formals/formalshirtImage.csv'
    formals_storing_path = '../data/formals/formalsImages/formalsImage'

    ethenic_df_path = '../data/ethenic/ethenicshirtImage.csv'
    ethenic_storing_path = '../data/ethenic/ethenicImages/ethenicImage'

    laptop_df_path = '../data/laptop/laptopImage.csv'
    laptop_storing_path = '../data/laptop/laptopImages/laptopImage'
    
    etheni_female_df_path = '../data/ethenic/ethenicshirtFemaleImage.csv'
    etheni_female_storing_path = '../data/ethenic/ethenicfemaleImages/ethenicFemaleImage'

    print('generating tshirt')
    #generateImage(tshirt_df_path, tshirt_storing_path)

    print('generating formals')
    #generateImage(formals_df_path, formals_storing_path)

    print('generating ethenic')
    #generateImage(ethenic_df_path, ethenic_storing_path)

    print('generating ethenic feamle')
    #generateImage(etheni_female_df_path, tshirt_storing_path)

    print('generating latop')
    generateImage(tshirt_df_path, tshirt_storing_path)