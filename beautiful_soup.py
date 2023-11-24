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
    "https://vancouver.craigslist.org/rds/ctd/d/surrey-2018-nissan-altima-sr-great-on/7681664187.html",
    "https://vancouver.craigslist.org/rds/ctd/d/surrey-2015-hyundai-elantra-bad-credit/7687990526.html",
    "https://vancouver.craigslist.org/rds/ctd/d/surrey-2015-volkswagen-passat-cc/7687991329.html",
    "https://vancouver.craigslist.org/rds/ctd/d/surrey-2015-volkswagen-jetta-tsi/7687989624.html",
    "https://vancouver.craigslist.org/rds/ctd/d/surrey-2017-nissan-sentra-sr-turbo/7686719350.html",
    "https://vancouver.craigslist.org/rds/ctd/d/surrey-2017-hyundai-elantra-apple/7686314862.html",
    "https://vancouver.craigslist.org/van/ctd/d/richmond-2013-nissan-sentra-sr-sport/7681732937.html",
    "https://vancouver.craigslist.org/pml/ctd/d/maple-ridge-east-2016-nissan-altima-25s/7683097839.html",
    "https://vancouver.craigslist.org/rds/ctd/d/surrey-2015-honda-civic-si-turbo-manual/7689156400.html",
    "https://vancouver.craigslist.org/rds/ctd/d/surrey-2017-mazda-mazda3-sport-finance/7688055833.html",
    "https://vancouver.craigslist.org/rds/ctd/d/surrey-2019-nissan-rogue-sv-awd-clean/7688016666.html",
    "https://vancouver.craigslist.org/rds/ctd/d/surrey-2017-hyundai-elantra-applze/7688017448.html",
    "https://vancouver.craigslist.org/rds/ctd/d/surrey-2017-nissan-sentra-sr-turbo/7688017684.html",
    "https://vancouver.craigslist.org/rds/ctd/d/surrey-2013-nissan-sentra-sv-great-on/7688000636.html",
    "https://vancouver.craigslist.org/rds/ctd/d/surrey-2019-hyundai-elantra-apple/7688000783.html",
    "https://vancouver.craigslist.org/rds/ctd/d/surrey-2015-hyundai-elantra-bad-credit/7687990526.html",
    "https://vancouver.craigslist.org/van/ctd/d/vancouver-2015-kia-sportage-lx-awd-call/7687616644.html",
    "https://vancouver.craigslist.org/rds/ctd/d/surrey-2019-hyundai-elantra-apple/7681661243.html",
    "https://vancouver.craigslist.org/bnc/ctd/d/chevrolet-malibu/7681635336.html",
    "https://vancouver.craigslist.org/bnc/ctd/d/burnaby-2007-lexus-is250-awd/7680106783.html"
]

# Remove duplicates from the URL list
unique_urls = list(set(urls))

# Create lists to store data
data = []

def get_data():
    # Iterate through each URL and extract data
    for url in unique_urls:
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

                # Limit description size to 3000 characters
                description = description[:1000]
            else:
                description = "Description not available"

            # Append data to the list
            data.append([title, price, condition, cylinders, fuel, odometer, transmission, title_status, paint_color, drive, vehicle_type, description, location, url])
        else:
            print(f"Failed to fetch the page: {url}")

    # Format the data with a serial number column to paste into Google Sheets
    output = "Serial Number\tTitle\tPrice\tCondition\tCylinders\tFuel\tOdometer\tTransmission\tTitle Status\tPaint Color\tDrive\tType\tDescription\tLocation\tURL\n"  # Headers

    for idx, row in enumerate(data, start=1):
        output += f"{idx}\t" + "\t".join(row) + "\n"

    print(output)


if __name__ == "__main__":
    get_data()