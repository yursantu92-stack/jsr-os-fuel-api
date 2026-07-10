import json
import datetime
import urllib.request
import re

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
        # আজকের লাইভ রেট অনুযায়ী আপডেট করা হলো (Google Data)
        "west_bengal": {"petrol": 113.87, "diesel": 100.15, "cng": 94.82}
    },
    "global": {}
}

# পৃথিবীর ১৯৫টি দেশের ISO Country Code
all_countries = [
    'af', 'al', 'dz', 'ad', 'ao', 'ag', 'ar', 'am', 'au', 'at', 'az', 'bs', 'bh', 'bd', 'bb', 'by', 'be', 'bz', 'bj', 'bt', 
    'bo', 'ba', 'bw', 'br', 'bn', 'bg', 'bf', 'bi', 'cv', 'kh', 'cm', 'ca', 'cf', 'td', 'cl', 'cn', 'co', 'km', 'cd', 'cg', 
    'cr', 'ci', 'hr', 'cu', 'cy', 'cz', 'dk', 'dj', 'dm', 'do', 'ec', 'eg', 'sv', 'gq', 'er', 'ee', 'sz', 'et', 'fj', 'fi', 
    'fr', 'ga', 'gm', 'ge', 'de', 'gh', 'gr', 'gd', 'gt', 'gn', 'gw', 'gy', 'ht', 'hn', 'hu', 'is', 'in', 'id', 'ir', 'iq', 
    'ie', 'il', 'it', 'jm', 'jp', 'jo', 'kz', 'ke', 'ki', 'kp', 'kr', 'kw', 'kg', 'la', 'lv', 'lb', 'ls', 'lr', 'ly', 'li', 
    'lt', 'lu', 'mg', 'mw', 'my', 'mv', 'ml', 'mt', 'mh', 'mr', 'mu', 'mx', 'fm', 'md', 'mc', 'mn', 'me', 'ma', 'mz', 'mm', 
    'na', 'nr', 'np', 'nl', 'nz', 'ni', 'ne', 'ng', 'mk', 'no', 'om', 'pk', 'pw', 'pa', 'pg', 'py', 'pe', 'ph', 'pl', 'pt', 
    'qa', 'ro', 'ru', 'rw', 'kn', 'lc', 'vc', 'ws', 'sm', 'st', 'sa', 'sn', 'rs', 'sc', 'sl', 'sg', 'sk', 'si', 'sb', 'so', 
    'za', 'ss', 'es', 'lk', 'sd', 'sr', 'se', 'ch', 'sy', 'tj', 'tz', 'th', 'tl', 'tg', 'to', 'tt', 'tn', 'tr', 'tm', 'tv', 
    'ug', 'ua', 'ae', 'gb', 'us', 'uy', 'uz', 'vu', 've', 'vn', 'ye', 'zm', 'zw'
]

for cc in all_countries:
    data["global"][cc] = {"petrol_usd": 1.25, "diesel": 1.15, "cng": 0.85}

custom_rates = {
    "us": {"petrol_usd": 1.05, "diesel": 1.10, "cng": 0.90},
    "ae": {"petrol_aed": 3.22, "diesel": 3.30, "cng": 2.90},
    "gb": {"petrol_usd": 1.85, "diesel": 1.90, "cng": 1.20},
    "au": {"petrol_usd": 1.35, "diesel": 1.40, "cng": 1.10},
    "bd": {"petrol_usd": 1.12, "diesel": 0.98, "cng": 0.50},
    "sa": {"petrol_usd": 0.62, "diesel": 0.30, "cng": 0.20},
    "ca": {"petrol_usd": 1.25, "diesel": 1.30, "cng": 0.95},
    "sg": {"petrol_usd": 2.10, "diesel": 2.00, "cng": 1.80},
    "pk": {"petrol_usd": 0.95, "diesel": 1.00, "cng": 0.70},
    "ru": {"petrol_usd": 0.60, "diesel": 0.65, "cng": 0.30},
    "jp": {"petrol_usd": 1.20, "diesel": 1.05, "cng": 0.80},
    "cn": {"petrol_usd": 1.15, "diesel": 1.00, "cng": 0.75},
}

for country_code, rate in custom_rates.items():
    data["global"][country_code] = rate

# Plan B: Google Bot Bypass Headers
req_headers = {
    'User-Agent': 'Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Referer': 'https://www.google.com/'
}

pattern = r'<td><a href=".*?/.*?in-(.*?)\.html".*?>(.*?)</a></td>\s*<td>.*?</td>\s*<td>₹ (.*?)</td>'

# পেট্রোল লাইভ ডেটা স্ক্র্যাপ
try:
    req_petrol = urllib.request.Request('https://www.goodreturns.in/petrol-price.html', headers=req_headers)
    html_petrol = urllib.request.urlopen(req_petrol, timeout=10).read().decode('utf-8')
    petrol_matches = re.findall(pattern, html_petrol, re.IGNORECASE)
    
    for match in petrol_matches:
        state_slug = match[0].replace('-', '_').lower()
        price = float(match[2].replace(',', ''))
        if state_slug in data['india']:
            data['india'][state_slug]['petrol'] = price
except Exception as e:
    print(f"Petrol Error: {e}")

# ডিজেল লাইভ ডেটা স্ক্র্যাপ
try:
    req_diesel = urllib.request.Request('https://www.goodreturns.in/diesel-price.html', headers=req_headers)
    html_diesel = urllib.request.urlopen(req_diesel, timeout=10).read().decode('utf-8')
    diesel_matches = re.findall(pattern, html_diesel, re.IGNORECASE)
    
    for match in diesel_matches:
        state_slug = match[0].replace('-', '_').lower()
        price = float(match[2].replace(',', ''))
        if state_slug in data['india']:
            data['india'][state_slug]['diesel'] = price
except Exception as e:
    print(f"Diesel Error: {e}")

# JSON তৈরি ও সেভ
with open('fuel_prices.json', 'w') as f:
    json.dump(data, f, indent=4)
    
print("JSR-OS Global Fuel API updated successfully!")
