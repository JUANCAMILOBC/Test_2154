import requests
from bs4 import BeautifulSoup
import ast
import json



def extract_urls(url):
    list_urls = list()
    list_urls.append(url)
    page = requests.get(url)
    soup_home = BeautifulSoup(page.content,'html.parser')
    base_url = url.replace('/test-sites/e-commerce/scroll', '')

    for new_urls in soup_home.find_all('a', class_='category-link', href=True):
        new_link = base_url + new_urls['href']
        list_urls.append(new_link)
        new_page = requests.get(new_link)
        soup_new = BeautifulSoup(new_page.content, 'html.parser')
        for new_urls_2 in soup_new.find_all('a', class_='subcategory-link', href=True):
            new_link = base_url + new_urls_2['href']
            list_urls.append(new_link)
    return list_urls

def extract_items(List_urls):
    Items_listed = {}
    for cont_url,url_data in enumerate(List_urls):
        i = 0
        new_items = requests.get(url_data)
        soup_new = BeautifulSoup(new_items.content, 'html.parser')
        #print('url',url_data)
        if ('laptops' in url_data) or ('tablets' in url_data) or ('touch' in url_data):
            temp_data = ''
            for value in soup_new.find_all('div', {'class': ['row ecomerce-items ecomerce-items-scroll']}):

                temp_data = ast.literal_eval(value['data-items'][1:-1])
            for cont_ID in range(len(temp_data)):
                temp_data[cont_ID]['price'] = float(temp_data[cont_ID]['price'])

            if ('laptops' in url_data):
                Items_listed['computers_laptops'] = temp_data
            if ('tablets' in url_data):
                Items_listed['computers_tables'] = temp_data
            if ('touch' in url_data):
                Items_listed['phones_touch'] = temp_data
        else:
            band_str_dict = 0
            temp_data = ''
            for cont_url_2, new_urls in enumerate(soup_new.find_all('div', {'class': ['caption']})):

                ID_ref = new_urls.a['href'].split('/')[5]

                if band_str_dict == 0:
                    temp_data = '{\"id\": '+ID_ref+', \"title\": \''+new_urls.a['title']+'\', \"description\": \''+\
                        new_urls.p.text+'\', \"price\": '+new_urls.h4.text.replace('$','')+'}'
                    band_str_dict = 1
                else:
                    temp_data += ' , {\"id\": '+ID_ref+', \"title\": \''+new_urls.a['title']+'\', \"description\": \''+\
                        new_urls.p.text+'\', \"price\": '+new_urls.h4.text.replace('$','')+'}'

            if ('computers' in url_data):
                Items_listed['computers'] = ast.literal_eval(temp_data)
            elif ('phones' in url_data):
                Items_listed['phones'] = ast.literal_eval(temp_data)
            else:
                Items_listed['home'] = ast.literal_eval(temp_data)

    json_object = json.dumps(Items_listed)
    return json_object

if __name__ == '__main__':
    url = 'https://webscraper.io/test-sites/e-commerce/scroll'
    all_urls = extract_urls(url)
    print(all_urls)
    json_data = extract_items(all_urls)
    print(json_data)
    with open("sample.json", "w") as outfile:
        outfile.write(json_data)