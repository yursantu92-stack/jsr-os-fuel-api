import json
import datetime
import cloudscraper
from bs4 import BeautifulSoup

# ভারতের ২৮টি রাজ্যের কমপ্লিট ডেটাবেস (আপডেটেড ফলব্যাক)
data = {
    "last_updated": str(datetime.datetime.now()),
    "india": {
        "andhra_pradesh": {"petrol": 109.50, "diesel": 97.50, "cng": 90.00},
        "arunachal_pradesh": {"petrol": 93.50, "diesel": 83.50, "cng": 75.00},
        "assam": {"petrol": 98.00, "diesel": 89.00, "cng": 85.00},
        "bihar": {"petrol": 107.00, "diesel": 94.00, "cng": 88.00},
        "chhattisgarh": {"petrol": 102.50, "diesel": 95.50, "cng": 80.00},
        "delhi": {"petrol": 94.72, "diesel": 87.62, "cng": 74.09},
        "goa": {"petrol": 95.50, "diesel": 87.50, "cng": 82.00},
        "gujarat": {"petrol": 94.50, "diesel": 90.50, "cng": 76.00},
        "haryana": {"petrol": 95.00, "diesel": 88.00, "cng": 80.00},
        "himachal_pradesh": {"petrol": 95.50, "diesel": 87.50, "cng": 82.00},
        "jharkhand": {"petrol": 99.50, "diesel": 94.50, "cng": 85.00},
        "karnataka": {"petrol": 102.50, "diesel": 88.50, "cng": 82.00},
        "kerala": {"petrol": 107.50, "diesel": 96.50, "cng": 85.00},
        "madhya_pradesh": {"petrol": 106.50, "diesel": 91.50, "cng": 90.00},
        "maharashtra": {"petrol": 104.00, "diesel": 90.50, "cng": 75.00},
        "manipur": {"petrol": 101.50, "diesel": 87.50, "cng": 82.00},
        "meghalaya": {"petrol": 96.50, "diesel": 84.50, "cng": 80.00},
        "mizoram": {"petrol": 95.50, "diesel": 82.50, "cng": 80.00},
        "nagaland": {"petrol": 98.50, "diesel": 86.50, "cng": 82.00},
        "odisha": {"petrol": 101.00, "diesel": 92.50, "cng": 85.00},
        "punjab": {"petrol": 96.50, "diesel": 87.50, "cng": 82.00},
        "rajasthan": {"petrol": 104.50, "diesel": 90.50, "cng": 85.00},
        "sikkim": {"petrol": 101.50, "diesel": 89.50, "cng": 82.00},
        "tamil_nadu": {"petrol": 100.50, "diesel": 92.50, "cng": 84.00},
        "telangana": {"petrol": 107.50, "diesel": 95.50, "cng": 92.00},
        "tripura": {"petrol": 97.50, "diesel": 86.50, "cng": 82.00},
        "uttar_pradesh": {"petrol": 94.50, "diesel": 87.50, "cng": 79.00},
        "uttarakhand": {"petrol": 93.50, "diesel": 88.50, "cng": 83.00},
        "west_bengal": {"petrol": 113.87, "diesel": 100.15, "cng": 94.82}
    },
    "global": {}
}

# গ্লোবাল ডেটা (সংক্ষিপ্ত করা হলো)
custom_rates = {
    "us": {"petrol_usd": 1.05, "diesel": 1.10, "cng": 0.90},
    "bd": {"petrol_usd": 1.12, "diesel": 0.98, "cng": 0.50}
}
for country_code, rate in custom_rates.items():
    data["global"][country_code] = rate

# Cloudscraper সেটআপ (এটি ওয়েবসাইটের ফায়ারওয়াল বাইপাস করবে)
scraper = cloudscraper.create_scraper(
    browser={
        'browser': 'chrome',
        'platform': 'windows',
        'desktop': True
    }
)

# পেট্রোল লাইভ ডেটা স্ক্র্যাপ
try:
    print("Bypassing security for Petrol prices...")
    response = scraper.get('https://www.goodreturns.in/petrol-price.html', timeout=20)
    
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        for a_tag in soup.find_all('a', href=True):
            if '-in-' in a_tag['href'] and '.html' in a_tag['href']:
                state_slug = a_tag['href'].split('-in-')[-1].replace('.html', '').replace('-', '_').lower()
                if state_slug in data['india']:
                    row = a_tag.find_parent('tr')
                    if row:
                        cols = row.find_all('td')
                        if len(cols) >= 3:
                            price_text = cols[2].text.replace('₹', '').replace(',', '').strip()
                            try:
                                data['india'][state_slug]['petrol'] = float(price_text)
                            except ValueError:
                                pass
        print("Petrol live data successfully fetched!")
    else:
        print(f"Petrol Fetch Failed. Status Code: {response.status_code}")
except Exception as e:
    print(f"Petrol Error: {e}")

# ডিজেল লাইভ ডেটা স্ক্র্যাপ
try:
    print("Bypassing security for Diesel prices...")
    response = scraper.get('https://www.goodreturns.in/diesel-price.html', timeout=20)
    
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        for a_tag in soup.find_all('a', href=True):
            if '-in-' in a_tag['href'] and '.html' in a_tag['href']:
                state_slug = a_tag['href'].split('-in-')[-1].replace('.html', '').replace('-', '_').lower()
                if state_slug in data['india']:
                    row = a_tag.find_parent('tr')
                    if row:
                        cols = row.find_all('td')
                        if len(cols) >= 3:
                            price_text = cols[2].text.replace('₹', '').replace(',', '').strip()
                            try:
                                data['india'][state_slug]['diesel'] = float(price_text)
                            except ValueError:
                                pass
        print("Diesel live data successfully fetched!")
    else:
        print(f"Diesel Fetch Failed. Status Code: {response.status_code}")
except Exception as e:
    print(f"Diesel Error: {e}")

# JSON তৈরি ও সেভ
with open('fuel_prices.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, indent=4, ensure_ascii=False)
    
print("JSR-OS Global Fuel API completed!")
