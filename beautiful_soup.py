import requests
from bs4 import BeautifulSoup

# URLs of Craigslist car listings
urls = [
    "https://vancouver.craigslist.org/rds/cto/d/surrey-north-2013-low-kms-hyundai/7685815655.html",
    "https://vancouver.craigslist.org/rds/cto/d/surrey-honda-civic-2013/7690689574.html",
    "https://vancouver.craigslist.org/van/ctd/d/burnaby-2010-toyota-camry-hybrid-4dr/7690633689.html",
    "https://vancouver.craigslist.org/rds/cto/d/surrey-2010-honda-civic/7689686439.html",
    "https://vancouver.craigslist.org/rch/cto/d/richmond-2013-nissan-altima-25-sl/7688069895.html",
    "https://vancouver.craigslist.org/rds/cto/d/surrey-nissan-altima-2016/7689438975.html",
    "https://vancouver.craigslist.org/van/cto/d/burnaby-2013-nissan-altima/7689227562.html",
    "https://vancouver.craigslist.org/van/cto/d/burnaby-2015-nissan-altima-sv-limited/7688156758.html",
    "https://vancouver.craigslist.org/van/ctd/d/abbotsford-2017-nissan-altima-25/7682398377.html",
    "https://vancouver.craigslist.org/rds/ctd/d/surrey-2018-nissan-altima-sr-great-on/7681664187.html"
]

# Create lists to store data
data = []

def get_data():
    # Iterate through each URL and extract data
    for url in urls:
        response = requests.get(url)

        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')

            # Extracting title
            title = soup.find('span', id='titletextonly').text.strip()

            # Extracting price
            price_tag = soup.find('span', class_='price')
            price = price_tag.text.strip() if price_tag else "Price not listed"

            # Extracting location
            location_tag = soup.find('div', class_='mapaddress')
            location = location_tag.text.strip() if location_tag else "Location not available"

            # Extracting additional details from the 2nd attrgroup in mapAndAttrs
            map_and_attrs = soup.find('div', class_='mapAndAttrs')
            if map_and_attrs:
                attr_groups = map_and_attrs.find_all('p', class_='attrgroup')
                if len(attr_groups) > 1:
                    attr_group = attr_groups[1]  # Select the 2nd attrgroup
                    spans = attr_group.find_all('span')
                    additional_details = {}
                    for span in spans:
                        text_parts = span.text.split(':')
                        label = text_parts[0].strip()
                        value = text_parts[1].strip() if len(text_parts) > 1 else "N/A"
                        additional_details[label] = value


                # Extract specific details
                condition = additional_details.get('condition', 'N/A')
                cylinders = additional_details.get('cylinders', 'N/A')
                fuel = additional_details.get('fuel', 'N/A')
                odometer = additional_details.get('odometer', 'N/A')
                transmission = additional_details.get('transmission', 'N/A')
                title_status = additional_details.get('title status', 'N/A')
                paint_color = additional_details.get('paint color', 'N/A')
                drive = additional_details.get('drive', 'N/A')
                vehicle_type = additional_details.get('type', 'N/A')
            else:
                condition, cylinders, fuel, odometer, transmission, title_status, paint_color, drive, vehicle_type = "N/A", "N/A", "N/A", "N/A", "N/A", "N/A", "N/A", "N/A", "N/A"

            # Extracting description from postingbody
            posting_body = soup.find('section', id='postingbody')
            description = ""
            if posting_body:
                for content in posting_body.contents:
                    if content.name == 'div' and 'print-information' in content.get('class', []):
                        continue
                    if isinstance(content, str) and content.strip():
                        description += content.strip() + " "
                description = description.strip()
            else:
                description = "Description not available"

            # Append data to the list
            data.append([title, price, location, condition, cylinders, fuel, odometer, transmission, title_status, paint_color, drive, vehicle_type, description, url])
        else:
            print(f"Failed to fetch the page: {url}")

    # Format the data with a serial number column to paste into Google Sheets
    output = "Serial Number\tTitle\tPrice\tLocation\tCondition\tCylinders\tFuel\tOdometer\tTransmission\tTitle Status\tPaint Color\tDrive\tType\tDescription\tURL\n"  # Headers

    for idx, row in enumerate(data, start=1):
        output += f"{idx}\t" + "\t".join(row) + "\n"

    print(output)


if __name__ == "__main__":
    get_data()