import requests
from bs4 import BeautifulSoup
import pandas as pd
from huggingface_hub import login
import os
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager


def get_data_from_url(main_url,url:str)->dict:
    data={
    'url':None, #
    'number_of_rooms':None, #
    'region':None,#
    'price_dollar':None,#
    'what_floor':None,#
    'max_of_floors':None,#
    'type':None,#
    'state':None,#
    'house_type':None,#
    'ceiling_height':None,#
    'area':None, #
    'kitchen_area':None,#
    'year':None,#
    'heating':None,#
    'furniture':None,#
    'docs':None,#
    'exchange_possible':None,#
    'installment_plan':None,#
    'mortgage_possible':None,#
    'from_whom':None, #
    'lat':None,#
    'lon':None, #
    'added':None,#
    'upped':None,#
    'view':None,#
    'like':None#
    }
    data['url']=f"{main_url}{url}"
    response=requests.get(f"{main_url}{url}")
    page=BeautifulSoup(response.content,'html.parser')
    page1=page.find_all('div',class_='label')
    if page.find('div',class_='content-wrapper')!=None:
        if page.find('div',class_='content-wrapper').find('div',class_='main-content')!=None:
            if page.find('div',class_='content-wrapper').find('div',class_='main-content').find('div',class_='details-header')!=None:
                if page.find('div',class_='content-wrapper').find('div',class_='main-content').find('div',class_='details-header').find('div',class_='left')!=None:
                    if page.find('div',class_='content-wrapper').find('div',class_='main-content').find('div',class_='details-header').find('div',class_='left').find('h1')!=None:
                        str1=page.find('div',class_='content-wrapper').find('div',class_='main-content').find('div',class_='details-header').find('div',class_='left').find('h1').text.strip()
                        data['number_of_rooms']=str1
    if page.find('div',class_='address')!=None:
        address=page.find('div',class_='address').text.strip()
        if ', 'in address:
            data['region']=address[:address.index(', ')]
        else:data['region']=address
    if page.find('div', class_='price-dollar')!=None:
        data['price_dollar']=page.find('div', class_='price-dollar').text.strip().replace('$ ','').replace(' ','')

    for i in page1:
        if i.find(string='Тип предложения')!=None:
            if i.parent.find(class_='info')!=None:  
                data['from_whom']=i.parent.find(class_='info').text.strip()
        if i.find(string='Этаж')!=None:
            if i.parent.find(class_='info')!=None:
                if len(i.parent.find(class_='info').text.strip().split())==4:
                    data['max_of_floors']=i.parent.find(class_='info').text.strip().split()[-1]
                    data['what_floor']=i.parent.find(class_='info').text.strip().split()[0]
        if i.find(string='Серия')!=None:
            if i.parent.find(class_='info')!=None:  
                data['type']=i.parent.find(class_='info').text.strip()
        if i.find(string='Состояние')!=None:
            if i.parent.find(class_='info')!=None:  
                data['state']=i.parent.find(class_='info').text.strip()        
        if i.find(string='Высота потолков')!=None:
            if i.parent.find(class_='info')!=None:  
                data['ceiling_height']=i.parent.find(class_='info').text.strip()                    
        if i.find(string='Площадь')!=None:
            if i.parent.find(class_='info')!=None:
                if len(i.parent.find(class_='info').text.strip().split(', '))==2:
                    data['area']=i.parent.find(class_='info').text.strip().split(', ')[0]
                    data['kitchen_area']=i.parent.find(class_='info').text.strip().split()[-1]
                else: data['area']=i.parent.find(class_='info').text.strip().split(', ')[0]                  
        if i.find(string='Дом')!=None:
            if len(i.parent.find(class_='info').text.strip().split(', '))>1:
                data['year']=i.parent.find(class_='info').text.strip().split(', ')[1]
                data['house_type']=i.parent.find(class_='info').text.strip().split(', ')[0]
            else:
                data['house_type']=i.parent.find(class_='info').text.strip().split(', ')[0]
        if i.find(string='Отопление')!=None:
            data['heating']=i.parent.find(class_='info').text.strip()
        if i.find(string='Мебель')!=None:      
            data['furniture']=i.parent.find(class_='info').text.strip()    
        if i.find(string='Правоустанавливающие документы')!=None:
            data['docs']=' '.join(i.parent.find(class_='info').text.strip().split())
        if i.find(string='Возможность рассрочки')!=None:
            data['installment_plan']=i.parent.find(class_='info').text.strip()
        if i.find(string='Возможность ипотеки')!=None:
            data['mortgage_possible']=i.parent.find(class_='info').text.strip()
        if i.find(string='Возможность обмена')!=None:
            data['exchange_possible']=i.parent.find(class_='info').text.strip()
    if page.find(id='map2gis')!=None:
        if page.find(id='map2gis').get('data-lat')!=None:            
            data['lat']=page.find(id='map2gis').get('data-lat')
    if page.find(id='map2gis')!=None:
        if page.find(id='map2gis').get('data-lon')!=None:   
            data['lon']=page.find(id='map2gis').get('data-lon')
    if page.find('span',class_='added-span')!=None:        
        data['added']=page.find('span',class_='added-span').text.strip()
    if page.find('span',class_='upped-span')!=None:        
        data['upped']=page.find('span',class_='upped-span').text.strip()
    if page.find('span',class_='view-count')!=None:
        data['view']=page.find('span',class_='view-count').text.strip()
    if page.find('span', class_=['favourite-count', 'table-comments'])!=None:
        data['like']=page.find('span', class_=['favourite-count', 'table-comments']).text.strip()
    return data

def get_imgs(main_url:str,url:str):
    path='house_kg_img/'+main_url.replace('https://','').replace('/','_')+url.replace('/','_')
    os.makedirs(path,exist_ok=True)
    options = Options()
    options.headless = True
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    driver.get(f"{main_url}{url}")
    html = driver.page_source
    page = BeautifulSoup(html, 'html.parser')  
    divs=page.find_all('div', class_=["fotorama__thumb", "fotorama__loaded", "fotorama__loaded--img"])
    count=1
    for i in divs:
        if i!=None:
            if i.find('img')!=None:
                with open(f'{path}/img{count}.jpg','wb') as f:
                    f.write(requests.get(i.find('img').get('src')).content)
                    count+=1


data={
    'url':[], #
    'number_of_rooms':[], #
    'region':[],#
    'price_dollar':[],#
    'what_floor':[],#
    'max_of_floors':[],#
    'type':[],#
    'state':[],
    'house_type':[],#
    'ceiling_height':[],#
    'area':[], #
    'kitchen_area':[],#
    'year':[],#
    'heating':[],#
    'furniture':[],#
    'docs':[],#
    'exchange_possible':[],#
    'installment_plan':[],#
    'mortgage_possible':[],#
    'from_whom':[], #
    'lat':[],#
    'lon':[], #
    'added':[],#
    'upped':[],#
    'view':[],
    'like':[]
}

count_pages=649
number_page=1

df=pd.read_csv('house_kg_page.csv',delimiter='|')
urls=df['url'].to_list()
# print(df['url'])
for i in range(1,count_pages+1):
    pages=requests.get(f'https://www.house.kg/kupit-kvartiru?sort_by=upped_at%20desc&page={i}')
    page=BeautifulSoup(pages.content,'html.parser')
    titles=page.find('div',class_='content-wrapper').select('.listings-wrapper > .listing')
    for i in titles:
        a=i.select('div .right-info > .top-info > .left-side > p > a')[0]
        # print('https://www.house.kg'+a.get('href'))
        if not(('https://www.house.kg'+a.get('href')) in urls):
            print('ssssssss')
            data1=get_data_from_url('https://www.house.kg',a.get('href'))
            for i in data1.keys():
                data[i].append(data1[i])
        # get_imgs('https://www.house.kg',a.get('href'))    
    print(f'PAGE {number_page} ENDED')
    number_page+=1
    df=pd.DataFrame(data=data)   
    df.to_csv(f'house_kg_page.csv',sep='|')

print(len(df.columns))    

