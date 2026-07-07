import json
import datetime

# এটি একটি বেসিক ডেমো স্ট্রাকচার। পরবর্তীতে আসল API দিয়ে এটি আপডেট করা যাবে।
data = {
    "last_updated": str(datetime.datetime.now()),
    "india": {
        "west_bengal": {"petrol": 106.03, "diesel": 92.76, "cng": 85.50},
        "delhi": {"petrol": 94.72, "diesel": 87.62, "cng": 74.09}
    },
    "global": {
        "usa": {"petrol_usd": 3.80},
        "uae": {"petrol_aed": 3.22}
    }
}

with open('fuel_prices.json', 'w') as f:
    json.dump(data, f, indent=4)
