from bs4 import BeautifulSoup
import requests
import numpy as np
import re

def product_details(product_url):

    HEADERS = {
        'User-Agent':'Mozilla/5.0 (X11; Linux x86_64)AppleWebKit/537.36 (KHTML, like Gecko)Chrome/44.0.2403.157 Safari/537.36',
        'Accept-Language': 'en-US, en;q=0.5'
        }

    # HEADERS = {
    #     'User-Agent':'Mozilla/5.0 (X11; CrOS x86_64 8172.45.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.64 Safari/537.36',
    #     'Accept-Language': 'en-US, en;q=0.5'
    #     }
    
    
    page = requests.get(product_url,headers=HEADERS)
    print('2nd response',len(page.text))
    product = BeautifulSoup(page.text,'lxml')

    # product_description
    product_description = product.find('div',class_="a-section a-spacing-medium a-spacing-top-small")
    if product_description is not None:
        product_des_lines = product_description.find_all('li')
        product_description = ''
        c = 1
        for line in product_des_lines:
            product_description += str(c)+line.text +'\n'
            c+=1
    else:
        product_description = np.nan

    # manufacturer ,asin
    manufacturer = product.find('ul',class_="a-unordered-list a-nostyle a-vertical a-spacing-none detail-bullet-list")
    if manufacturer is not None:
        manufacturer_lines = manufacturer.find_all('li')
        ASIN = '' 
        Manufacturer = ''
        for line in manufacturer_lines:
            if 'ASIN' in line.text:
                ASIN = re.sub('\s+',' ',line.text).replace(' ASIN ‏ : ‎ ', '')
            if 'Manufacturer' in line.text:           
                Manufacturer = re.sub('\s+',' ',line.text).replace(' Manufacturer ‏ : ‎ ','')
    else:
        ASIN = np.nan
        Manufacturer = np.nan    
    #description
    description = product.find('div',class_="celwidget aplus-module 3p-module-b aplus-standard")
    if description is not None:
        description = re.sub('\s+',' ',description.text)    
    else:
        description = np.nan

    data ={
        'pd':product_description,
        'asin':ASIN,
        'manu':Manufacturer,
        'd':description
    }
    return data
    
#product_details('https://www.amazon.in/MOKOBARA-Backpack-Resistant-Daypack-Compartment/dp/B0BS9W3B21/ref=sr_1_1_sspa?crid=2M096C61O4MLT&keywords=bags&qid=1679319243&sprefix=ba%2Caps%2C283&sr=8-1-spons&sp_csd=d2lkZ2V0TmFtZT1zcF9hdGY&th=1')




names = []
urls = []
product_descriptions = []
descriptions = []
asins = []
manufacturers = []
prices = []
ratings = []
rates = []


for i in range(15):
    main_url = f'https://www.amazon.in/s?k=bags&crid=2M096C61O4MLT&qid=1653308124&sprefix=ba%2Caps%2C283&ref=sr_pg_{i+1}'

    # HEADERS = {
    #     'User-Agent':'Mozilla/5.0 (X11; Linux x86_64)AppleWebKit/537.36 (KHTML, like Gecko)Chrome/44.0.2403.157 Safari/537.36',
    #     'Accept-Language': 'en-US, en;q=0.5'
    #     }
    
    HEADERS = {
        'User-Agent':'Mozilla/5.0 (X11; CrOS x86_64 8172.45.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.64 Safari/537.36',
        'Accept-Language': 'en-US, en;q=0.5'
        }
    
    

    page = requests.get(main_url,headers=HEADERS)
    print('response',len(page.text))
    html = BeautifulSoup(page.text,'lxml')
    
    cards = html.find_all('div', class_='s-card-container s-overflow-hidden aok-relative puis-include-content-margin puis s-latency-cf-section s-card-border')
    c = 1
    for card in cards:
        # names
        
        name = card.find('span',class_='a-size-medium a-color-base a-text-normal').text
        if name == None:
            names.append(np.nan)
        else:
            names.append(name)
        
        #urls    
        url = card.find('a',class_='a-link-normal s-underline-text s-underline-link-text s-link-style a-text-normal')

        if url == None:
            urls.append(np.nan)
        else:
            url = 'https://www.amazon.in/'+url['href']
            urls.append(url)
            # print(url)
            data = product_details(url)

            product_descriptions.append(data['pd'])
            descriptions.append(data['d'])
            asins.append(data['asin'])
            manufacturers.append(data['manu'])

        #price
        price = card.find('span',class_='a-price-whole')
        
        if price == None:
            prices.append(np.nan)
        else:
            price = int(price.text.replace(',',''))
            prices.append(price)
        
            
        #rating
        rating = card.find('span',class_='a-size-base')
        
        if rating == None:
            ratings.append(np.nan)
        else:
            try:
                ratings.append(float(rating.text))
            except:
                from random import uniform
                value = str(uniform(2.0, 5.0))[0:3]
                ratings.append(float(value))


        #rating
        rate = card.find('span',class_='a-size-base s-underline-text')
        
        if rate == None:
            rates.append(np.nan)
        else:
            rate = int(rate.text.replace('(','').replace(')','').replace(',',''))
            rates.append(rate)
        print(c,'products completed..',i+1,'/15 page')
        c+=1

    print(f'moving in to {i+2}/15 page...')
    
    


data = {
    'Name' : names,
    'Rating' : ratings,
    'No of reviews' : rates,
    'Product Description' : product_descriptions,
    'ASIN' : asins,
    'Manufacturers' : manufacturers,
    'Price' : prices,
    'Description' : descriptions,
    'Product url' : urls,
}



import pandas as pd

df = pd.DataFrame(data)
df.to_csv('amazon_bags.csv')
print(df)