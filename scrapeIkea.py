from bs4 import BeautifulSoup
import requests
import time
import pandas as pd
from pathlib import Path
from sheet_update import update_sheet


# List bookcases and scrape

def main():
    # url used for scraping, inspect and identify correct element
    html_text = requests.get("https://www.ikea.com/in/en/cat/bookcases-10382/").text
    soup = BeautifulSoup(html_text, 'lxml')
    # List elements and get Product Name, Size, Previous Price, New Price,
    # these details are available in pip-product-compact
    details = soup.find_all('div', class_='pip-product-compact')

    # Define DataFrame and use to append the results
    df = pd.DataFrame(columns=['productName', 'Measurement', 'newPrice', 'prevPrice'])

    for indx, det in enumerate(details):
        size_details = det.find('span', class_='pip-header-section__description-measurement').text
        prev_price = det.find('div', class_='pip-compact-price-package__previous-price-wrapper')
        has_child = len(prev_price.find_all())

        if has_child == 0:
            # print(det['data-product-name'], det['data-price'], size_details, det['data-price'])
            df.loc[indx] = [det['data-product-name'], size_details, det['data-price'], det['data-price']]
        else:
            prev_rs1 = prev_price.find('span', class_='pip-price pip-price--secondary')
            prev_rs2 = prev_rs1.find('span', class_='pip-price__integer').text
            df.loc[indx] = [det['data-product-name'], size_details, det['data-price'], prev_rs2]

    # Write to CSV, for verifying locally
    # filepath = Path('C:/Users/sumepati/Desktop/out.csv')
    # filepath.parent.mkdir(parents=True, exist_ok=True)
    # df.to_csv(filepath, index=False)
    update_sheet("Sheet1", df)


if __name__ == '__main__':
    main()
