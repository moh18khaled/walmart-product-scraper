import time
import json
import requests
from bs4 import BeautifulSoup

def get_json_data():
    subcategory_url = "https://www2.hm.com/en_us/women/products/socks-tights.htmlhttps://www.walmart.com/browse/clothing/girls-jeans/5438_7712430_1660851_2500436_2814775?povid=FashionTopNav_Kids_Girls_Clothing_Jeans"  # Replace with your desired subcategory URL

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
        'Referer': 'https://www.google.com/',
        'Accept-Language': 'en-US,en;q=0.9',
    }

    response = requests.get(subcategory_url, headers=headers)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, "html.parser")

        # Find the script tag containing JSON data
        json_data_element = soup.find('script', id="__NEXT_DATA__")

        if json_data_element and json_data_element.string:
            json_data = json.loads(json_data_element.string)  # Load the JSON from the script's content

            # Save JSON data to a file
            with open('h&mproduct.json', 'w', encoding='utf-8') as file:
                json.dump(json_data, file, ensure_ascii=False, indent=4)

            print("JSON data saved to 'product.json'.")
            return json_data
        else:
            print("JSON data element not found or is empty.")
    else:
        print(f"Failed to retrieve the page. Status code: {response.status_code}")


# Example usage:
get_json_data()
