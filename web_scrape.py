import requests
import json
from bs4 import BeautifulSoup
import time
from datetime import datetime

class Product:
    def __init__(self, title, reviews):
        self.title = title
        self.reviews = reviews
#PRODUCT 1
# Define the base URL for the product's customer reviews page
base_url = "https://www.amazon.in/Fastrack-Limitless-Biggest-SingleSync-Watchfaces/product-reviews/B0BZ8T21V4/ref=cm_cr_getr_d_paging_btm_next_10?ie=UTF8&reviewerType=all_reviews&pageNumber="

# Define headers to mimic a web browser request
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36",
    "Referer": "https://www.amazon.in/"
}

# Initialize an empty list to store reviews
reviews = []
product_title = ''

# Loop through multiple pages
for page_number in range(1, 11):  # Scraping pages 1 and 10
    url = base_url + str(page_number)

    # Add a sleep to avoid being blocked
    time.sleep(3)

    # Send an HTTP GET request to the current page with headers
    response = requests.get(url, headers=headers)

    # Check if the request was successful
    if response.status_code == 200:

        # Parse the HTML content of the page using BeautifulSoup
        soup = BeautifulSoup(response.text, "html.parser")
        if (page_number == 1):
            product_title = soup.find('a', class_='a-link-normal').text.strip()

        # Locate and extract customer reviews
        review_elements = soup.find_all("div", class_="a-section celwidget")

        for review_element in review_elements:
            review_t = review_element.find('span', class_="a-size-base a-color-secondary review-date").text.strip().split()
            review_time = datetime.strptime(' '.join(review_t[-3:]), '%d %B %Y')  # Convert to datetime
            review_text = review_element.find("span", class_="a-size-base review-text review-text-content").text.strip()
            data = {"review_text": review_text, "review_time": review_time.strftime("%Y-%m-%d")}
            reviews.append(data)

    else:
        print(f"Failed to retrieve page {page_number}. Status code: {response.status_code}")

product1 = Product(product_title, reviews)
#PRODUCT 2
base_url = "https://www.amazon.in/Fire-Boltt-Invincible-Smartwatch-Bluetooth-Connection/product-reviews/B0BRMY96P9/ref=cm_cr_arp_d_paging_btm_next_2?ie=UTF8&reviewerType=all_reviews&pageNumber="

# Define headers to mimic a web browser request
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36",
    "Referer": "https://www.amazon.in/"
}

# Initialize an empty list to store reviews
reviews = []
product_title = ''

# Loop through multiple pages
for page_number in range(1, 11):  # Scraping pages 1 and 10
    url = base_url + str(page_number)

    # Add a sleep to avoid being blocked
    time.sleep(3)

    # Send an HTTP GET request to the current page with headers
    response = requests.get(url, headers=headers)

    # Check if the request was successful
    if response.status_code == 200:

        # Parse the HTML content of the page using BeautifulSoup
        soup = BeautifulSoup(response.text, "html.parser")
        if (page_number == 1):
            product_title = soup.find('a', class_='a-link-normal').text.strip()

        # Locate and extract customer reviews
        review_elements = soup.find_all("div", class_="a-section celwidget")

        for review_element in review_elements:
            review_t = review_element.find('span', class_="a-size-base a-color-secondary review-date").text.strip().split()
            review_time = datetime.strptime(' '.join(review_t[-3:]), '%d %B %Y')  # Convert to datetime
            review_text = review_element.find("span", class_="a-size-base review-text review-text-content").text.strip()
            data = {"review_text": review_text, "review_time": review_time.strftime("%Y-%m-%d")}
            reviews.append(data)

    else:
        print(f"Failed to retrieve page {page_number}. Status code: {response.status_code}")

product2 = Product(product_title, reviews)


# Create a dictionary to store the product data
review_data = {"products": [product1.__dict__,product2.__dict__]}#see what __dict__ does... maybe converts a class to dictionary... if one looks at it class is kind of dictionary

# Save the JSON data to a file
with open("amazon_reviews.json", "w", encoding="utf-8") as json_file:
    json.dump(review_data, json_file, ensure_ascii=False, indent=4)
    print("Reviews have been scraped and saved to amazon_reviews.json.")
