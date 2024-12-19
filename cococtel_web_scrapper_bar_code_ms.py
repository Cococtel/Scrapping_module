import requests
from bs4 import BeautifulSoup
import json

def make_petition(url):
    return requests.get(url)

def main(isbn):
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36"}
    url = 'https://go-upc.com/search?q='
    petition = make_petition(url+isbn)
    #petition = requests.get(url+isbn, headers=headers)

    if petition.status_code == 200:
        print("información: " + extract_info(petition))
        return_json(extract_info(url+isbn))
    else:
        print (f'Error: {petition.status_code}')

def extract_info(page):
    soup = BeautifulSoup(page.text, 'html.parser')

    product_name = soup.find_all('h1', 'product-name')
    product_name = product_name[0].text.strip()

    product_photo = soup.find('img')
    if product_photo and 'src' in product_photo.attrs:
        product_photo = product_photo['src']

    description_section = soup.find("h2", string=lambda t: t and "Description" in t)
    description = description_section.find_next("span").text.strip() if description_section else "No description section found"

    additional_attributes_section = soup.find("h2", string=lambda t: t and "Additional Attributes" in t)
    additional_attributes = additional_attributes_section.find_next("span").text.strip() if additional_attributes_section else "No additional attributes section found"

    ean_label = soup.find("td", string=lambda t: t and "EAN" in t)
    ean = ean_label.find_next_sibling("td").text.strip() if ean_label else "No EAN found"

    return product_name, product_photo, description, additional_attributes, ean

def return_json(product_name, product_photo, description, additional_atributes, ean):
    json_dictionary = {
        'Name': product_name,
        'Photo_link': product_photo,
        'Description': description,
        'Addittional_atributes': additional_atributes,
        'isbn': ean
    }
    return json.dumps(json_dictionary)


isbn = '7702489000108'
main(isbn)

# Last print => 
# ('Roscas Pirrosquitas Piquitos 17g X1 Unidad', 'https://go-upc.s3.amazonaws.com/images/198752971.png', 'No description found.', 'No additional attributes found.', '7702489000108')