#!/usr/bin/env python3
"""
    Prints csv of AWS Products by screen-scraping AWS products page
"""

from requests import get
from lxml import html


class ProductsPage:
    """
        AWS Products Page
    """
    def __init__(self, aws_url, products_page):
        self.aws_url = aws_url
        self.products_url = self.aws_url + products_page

    def products_page_content(self):
        """ HTTP call to products URL and return contents """
        response = get(self.products_url)
        if response.status_code != 200:
            raise Exception(f"Failed to fetch page: {response.status_code}")
        return response.content

    def parse_products_page(self):
        """ Parse products page and return list of products """
        html_content = self.products_page_content()
        html_obj = html.fromstring(html_content)

        # Debug: Save the HTML content to a file for inspection
        with open("debug.html", "wb") as f:
            f.write(html_content)

        output = []
        sections = html_obj.xpath('//*[contains(@class, "lb-item-wrapper")]')
        if not sections:
            print("No sections found. Check the HTML structure.")
        for section in sections:
            category = section.find('a/span').text.strip()
            products = []
            for svc in section.findall('div/div/a'):
                products.append({
                    'Category': category,
                    'Product': svc.text.strip(),
                    'Description': svc.find('span').text.strip(),
                    'Link': self.aws_url + svc.get('href').strip()
                })
            output += sorted(products, key=lambda x: x['Product'])
        return output

def main():
    """ Main method """
    products_page = ProductsPage(
        aws_url='https://aws.amazon.com',
        products_page='/products'
    )
    products_list = products_page.parse_products_page()

    if not products_list:
        print("No products found. Please check the AWS products page or the parsing logic.")
        return

    quotify = lambda x: '"' + x + '"'
    print(','.join(map(quotify, products_list[0].keys())))
    for product in products_list:
        print(','.join(map(quotify, product.values())))

if __name__ == '__main__':
    main()
