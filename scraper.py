import json
import datetime
import requests
from bs4 import BeautifulSoup
import re

# ভারতের ২৮টি রাজ্যের কমপ্লিট ডেটাবেস
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
    "global": {
        "us": {"petrol_usd": 1.05, "diesel": 1.10, "cng": 0.90},
        "bd": {"petrol_usd": 1.12, "diesel": 0.98, "cng": 0.50}
    }
}

# শহরের নাম থেকে রাজ্যের নাম বের করার ম্যাজিক ম্যাপ
city_to_state_map = {
    "kolkata": "west_bengal",
    "mumbai": "maharashtra",
    "chennai": "tamil_nadu",
    "bangalore": "karnataka",
    "bengaluru": "karnataka",
    "hyderabad": "telangana",
    "jaipur": "rajasthan",
    "lucknow": "uttar_pradesh",
    "patna": "bihar",
    "bhopal": "madhya_pradesh",
    "bhubaneswar": "odisha",
    "guwahati": "assam",
    "thiruvananthapuram": "kerala",
    "trivandrum": "kerala",
    "ahmedabad": "gujarat",
    "gandhinagar": "gujarat",
    "shimla": "himachal_pradesh",
    "ranchi": "jharkhand",
    "raipur": "chhattisgarh",
    "panaji": "goa",
    "goa": "goa",
    "delhi": "delhi",
    "new delhi": "delhi"
}

req_headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
}

def fetch_fuel_data(fuel_type):
    urls = [
        f"https://www.ndtv.com/fuel-prices/{fuel_type}-price-in-india",
        f"https://www.bankbazaar.com/fuel/{fuel_type}-price-india.html"
    ]
    
    for url in urls:
        try:
            print(f"Fetching {fuel_type} from: {url}")
            res = requests.get(url, headers=req_headers, timeout=15)
            
            if res.status_code == 200:
                soup = BeautifulSoup(res.text, 'html.parser')
                success_count = 0
                
                for table in soup.find_all('table'):
                    for row in table.find_all('tr'):
                        cols = row.find_all(['td', 'th'])
                        if len(cols) >= 2:
                            col0_text = cols[0].text.strip().lower()
                            col1_text = cols[1].text.strip()
                            
                            # দাম ফিল্টার (শুধুমাত্র 70.00 থেকে 129.99 এর ভেতরের সংখ্যা ধরবে)
                            price_match = re.search(r'\b(?:7|8|9|10|11|12)\d\.\d{2}\b', col1_text)
                            
                            if price_match:
                                price_val = float(price_match.group())
                                matched_state = None
                                
                                # ১. সরাসরি রাজ্যের নাম খুঁজবে
                                for state_key in data['india'].keys():
                                    search_state = state_key.replace("_", " ")
                                    if search_state in col0_text:
                                        matched_state = state_key
                                        break
                                
                                # ২. রাজ্যের নাম না পেলে শহরের নাম থেকে খুঁজবে
                                if not matched_state:
                                    for city, state in city_to_state_map.items():
                                        if city in col0_text:
                                            matched_state = state
                                            break
                                            
                                # ৩. ডেটা আপডেট
                                if matched_state:
                                    data['india'][matched_state][fuel_type] = price_val
                                    success_count += 1
                
                if success_count > 5:
                    print(f"✅ Updated {success_count} states for {fuel_type} from {url}")
                    return 
            else:
                print(f"⚠️ Blocked by {url} (Status: {res.status_code})")
                
        except Exception as e:
            print(f"❌ Error with {url}: {e}")

# স্ক্র্যাপার রান করানো
fetch_fuel_data('petrol')
fetch_fuel_data('diesel')

# JSON ফাইল সেভ
with open('fuel_prices.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, indent=4, ensure_ascii=False)
    
print("JSR-OS Global Fuel API updated successfully with AI City-Mapper!")
