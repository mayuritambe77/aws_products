import requests
from bs4 import BeautifulSoup
import csv

def fetch_aws_products():
    # URL of the AWS products page
    url = "https://aws.amazon.com/products/"
    
    # Send an HTTP GET request to fetch the page content
    response = requests.get(url)
    if response.status_code != 200:
        print(f"Failed to fetch the page: {response.status_code}")
        return

    # Parse the HTML content using BeautifulSoup
    soup = BeautifulSoup(response.content, "html.parser")

    # Find the section containing product categories
    product_sections = soup.find_all("div", class_="lb-grid")  # Adjust this class based on the HTML structure
    if not product_sections:
        print("No product sections found. Check the HTML structure.")
        return

    print(f"Found {len(product_sections)} product sections")
    # Extract product details
    products = []
    for section in product_sections:
        # Extract category name
        category = section.find("h2")
        if category:
            print(f"Category: {category.text.strip()}")
        if not category:
            continue
        category_name = category.text.strip()

        # Extract product names and links
        product_links = section.find_all("a", class_="lb-txt-none")  # Adjust this class based on the HTML structure
        print(f"Found {len(product_links)} products in this category")
        for link in product_links:
            product_name = link.text.strip()
            product_url = link.get("href", "").strip()
            if product_name and product_url:
                products.append({
                    "Category": category_name,
                    "Product": product_name,
                    "Link": f"https://aws.amazon.com{product_url}" if product_url.startswith("/") else product_url
                })

    # Save the products to a CSV file
    with open("aws_products.csv", "w", newline="", encoding="utf-8") as csvfile:
        fieldnames = ["Category", "Product", "Link"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(products)

    print("AWS products have been saved to aws_products.csv")

if __name__ == "__main__":
    fetch_aws_products()