import requests, json

url = "http://127.0.0.1:8000/analyze/"

samples = [
    {"text": "Breaking news: Government to give free money to all citizens next week.", "source": "whatsapp"},
    {"text": "स्वास्थ्य मंत्रालय ने टीकाकरण कार्यक्रम की आधिकारिक घोषणा की।", "source": "news"},
    {"text": "અમાદવાદમાં આજે એલિયન્સ ઉતર્યા હતા!", "source": "social"},
    {"text": "NASA confirms discovery of water on the Moon.", "source": "news"},
]

for s in samples:
    r = requests.post(url, json=s)
    print(json.dumps(r.json(), ensure_ascii=False, indent=2))
