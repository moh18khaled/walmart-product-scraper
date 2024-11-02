import time
import json
import requests
import re
import random
from bs4 import BeautifulSoup
import os

def get_json_data(subcategory_url):
    """Fetch JSON data from the specified subcategory URL and return product links."""
    
    product_links = set()
    max_page_number = 8
    page_number = 1

    while page_number <= max_page_number:
        url = re.sub(r'page=\d+', f'page={page_number}', subcategory_url)
        print(page_number, max_page_number, url, '<><>><\n')
        
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
        }
        
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, "html.parser")
            json_data_element = soup.find('script', id="__NEXT_DATA__")

            if json_data_element:
                json_data = json.loads(json_data_element.string)
                if max_page_number == 1:
                    max_page_number = json_data['props']['pageProps']['initialData']['searchResult']['paginationV2']['maxPage']
                
                items = json_data['props']['pageProps']['initialData']['searchResult']['itemStacks']
                for link in items[0]['items']:
                    if link['__typename'] == 'Product':
                        full_link = 'https://www.walmart.com' + link['canonicalUrl']
                        product_links.add(full_link)
                        
        page_number += 1
        #time.sleep(random.uniform(2, 1))
    print(f"Found {len(product_links)} product links.")
    return product_links

def append_to_json(file_path, new_data):
    """Append new data to an existing JSON file or create it if it doesn't exist."""
    if os.path.exists(file_path):
        with open(file_path, 'r', encoding='utf-8') as file:
            try:
                data = json.load(file)
            except json.JSONDecodeError:
                data = []
    else:
        data = []

    data.extend(new_data)

    with open(file_path, 'w', encoding='utf-8') as file:
        json.dump(data, file, ensure_ascii=False, indent=4)

def fetch_product_details(product_links):
    """Fetch product details for each link and save to JSON without modifying existing content."""
    all_product_info = []

    for url in product_links:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
        }

        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            json_data_element = soup.find('script', id="__NEXT_DATA__")

            if json_data_element:
                json_data = json.loads(json_data_element.string)

                product_info = {
                    'StoreName': 'walmart',
                    'Category': 'Girl',
                    'SubCategory': 'Jeans',
                }

                # Safely access product title
                product_info['Title'] = json_data['props']['pageProps']['initialData']['data']['product'].get('name', 'N/A')

                # Safely access price information
                price_info = json_data['props']['pageProps']['initialData']['data']['product'].get('priceInfo')
                if price_info:
                    current_price_info = price_info.get('currentPrice')
                    if current_price_info:
                        product_info['Price'] = current_price_info.get('price', 'N/A')
                        product_info['Currency'] = current_price_info.get('currencyUnit', 'N/A')
                    else:
                        product_info['Price'] = 'N/A'
                else:
                    product_info['Price'] = 'N/A'

                # Safely access description
                product_info['Description'] = json_data['props']['pageProps']['initialData']['data'].get('idml', {}).get('shortDescription', 'N/A')

                # Safely access availability
                product_info['Availability'] = json_data['props']['pageProps']['initialData']['data']['product'].get('availabilityStatus', 'N/A')

                # Safely access average rating
                reviews_info = json_data['props']['pageProps']['initialData']['data'].get('reviews', {})
                product_info['AverageRating'] = reviews_info.get('roundedAverageOverallRating', 'N/A')

                # Add the product URL and image URL
                product_info['ProductPage'] = url
                product_info['Image'] = json_data['props']['pageProps']['initialData']['data']['product']['imageInfo'].get('thumbnailUrl', 'N/A')

                # Extract reviews if available
                reviews_data = reviews_info.get('customerReviews', [])
                product_info['TopReviews'] = [{'ReviewText': review.get('reviewText', ''),
                                               'Rating': review.get('rating', '')} for review in reviews_data]

                all_product_info.append(product_info)
            else:
                with open('soup_output.html', 'w', encoding='utf-8') as file:
                    file.write(soup.prettify())
                print(f"JSON data element not found for: {url}")
        else:
            print(f"Failed to retrieve product data. Status code: {response.status_code} for {url}")
        
        # Add a delay of 2 seconds before fetching the next product
        time.sleep(random.uniform(2, 1))

    # Append all product information to JSON file without overwriting existing content
    print(len(all_product_info))
    append_to_json('product_info.json', all_product_info)
    print(f"All product information saved to 'product_info.json'.")

# Example usage:
subcategory_url = "https://www.walmart.com/browse/clothing/girls-jeans/5438_7712430_1660851_2500436_2814775?povid=FashionTopNav_Kids_Girls_Clothing_Jeans"  # Replace with your desired subcategory URL

# Step 1: Get product links from JSON data
product_links = get_json_data(subcategory_url)

# Step 2: Fetch product details from the extracted links
if product_links:
    fetch_product_details(product_links)
