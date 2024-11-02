# Walmart Product Scraper

This project is a Python script that scrapes product details from a specific Walmart subcategory page, extracting information such as product name, price, description, availability, and ratings. The script then saves this data into a JSON file for further analysis or usage.

## Features

- Extracts product links from the provided Walmart subcategory URL.

- Fetches detailed information for each product including:
  - Title, price, description, and availability
  - Average rating and top customer reviews
  - Image URLs and product page links
- Saves all product data in JSON format without overwriting existing content.

## Prerequisites
- Python 3.x
- Requests
- BeautifulSoup