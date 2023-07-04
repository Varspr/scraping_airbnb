import requests
from bs4 import BeautifulSoup
import csv


def scrape_page(soup, quotes):
    quote_elements = soup.find_all("div", class_="g1qv1ctd c1v0rf5q dir dir-ltr")
    for quote_element in quote_elements:
        apart_name = quote_element.find("div", class_="t1jojoys dir dir-ltr").text
        first_discr = quote_element.find("span", class_="t6mzqp7 dir dir-ltr").text
        second_discr = quote_element.find("span", class_=" dir dir-ltr").text
        price = quote_element.find("span", class_="a8jt5op dir dir-ltr").text
        quotes.append(
            {
                "apart name": apart_name,
                "comment1": first_discr,
                "comment2": second_discr,
                "price": price,
            }
        )


url = (
    "https://www.airbnb.ru/s/%D0%91%D0%B0%D0%BB%D0%B8--%D0%98%D0%BD%D0%B4%D0%BE%D0%BD%D0%B5%D0%B7%D0%B8%D1%8F"
    "/homes?tab_id=home_tab&refinement_paths%5B%5D=%2Fhomes&flexible_trip_lengths%5B%5D=one_week"
    "&monthly_start_date=2023-07-01&monthly_length=12&price_filter_input_type=0&price_filter_num_nights=5"
    "&channel=EXPLORE&query=%D0%91%D0%B0%D0%BB%D0%B8%2C%20%D0%98%D0%BD%D0%B4%D0%BE%D0%BD%D0%B5%D0%B7%D0%B8%D1"
    "%8F&place_id=ChIJ06f8IHUv0i0RhM1WxCy2cig&date_picker_type=monthly_stay&adults=2&source"
    "=structured_search_input_header&search_type=autocomplete_click"
)
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
    "Chrome/107.0.0.0 Safari/537.36"
}
page = requests.get(url, headers=headers)
soup = BeautifulSoup(page.text, "html.parser")
quotes = []
scrape_page(soup, quotes)
next_elem = soup.find("a", class_="l1ovpqvx c1ytbx3a dir dir-ltr")
while next_elem is not None:
    next_page_relative_url = next_elem.find("a", href=True)["href"]
    page = requests.get(url + next_page_relative_url, headers=headers)
    soup = BeautifulSoup(page.text, "html.parser")
    scrape_page(soup, quotes)
    next_elem = soup.find("a", class_="l1ovpqvx c1ytbx3a dir dir-ltr")
csv_file = open("quotes.csv", "w", encoding="utf-8", newline="")
writer = csv.writer(csv_file)
writer.writerow(["apart_name", "first_discr", "second_discr", "price"])
for quote in quotes:
    writer.writerow(quote.values())
csv_file.close()
