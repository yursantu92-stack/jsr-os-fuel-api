import json
import datetime
import urllib.request
import re

# ভারতের ২৮টি রাজ্য এবং গ্লোবাল লোকেশনের কমপ্লিট ডেটাবেস (Fallback Data)
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
        "west_bengal": {"petrol": 106.03, "diesel": 92.76, "cng": 85.50}
    },
    "global": {
        "us": {"petrol_usd": 3.80, "diesel": 4.10, "cng": 2.50},
        "ae": {"petrol_aed": 3.22, "diesel": 3.30, "cng": 2.90},
        "gb": {"petrol_usd": 1.90, "diesel": 1.95, "cng": 1.50},
        "au": {"petrol_usd": 1.30, "diesel": 1.35, "cng": 1.10}
    }
}

# লাইভ ডেটা স্ক্র্যাপ করার চেষ্টা (Zero-Dependency)
try:
    req = urllib.request.Request('https://www.goodreturns.in/petrol-price.html', headers={'User-Agent': 'Mozilla/5.0'})
    html = urllib.request.urlopen(req, timeout=10).read().decode('utf-8')
    
    # HTML থেকে রাজ্যের নাম এবং দাম খুঁজে বের করার লজিক
    state_pattern = r'<td><a href=".*?/petrol-price-in-(.*?)\.html".*?>(.*?)</a></td>\s*<td>.*?</td>\s*<td>₹ (.*?)</td>'
    matches = re.findall(state_pattern, html, re.IGNORECASE)
    
    for match in matches:
        state_slug = match[0].replace('-', '_').lower()
        price = float(match[2].replace(',', ''))
        if state_slug in data['india']:
            data['india'][state_slug]['petrol'] = price
            
except Exception as e:
    print(f"Live API Blocked. Using JSR secure fallback data. Error: {e}")

# JSON ফাইলে ডেটা সেভ করা
with open('fuel_prices.json', 'w') as f:
    json.dump(data, f, indent=4)
    
print("JSR-OS Global Fuel API updated successfully!")
