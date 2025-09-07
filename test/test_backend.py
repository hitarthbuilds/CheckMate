# test_backend.py

import requests

# URL of your running FastAPI endpoint
url = "http://127.0.0.1:8000/analyze/"

# Example texts to test
test_cases = [
    {"text": "The moon is made of cheese.", "source": "tweet"},
    {"text": "NASA confirms water on Mars.", "source": "news"},
    {"text": "Share this WhatsApp message to win a prize!", "source": "whatsapp"},
]

for i, case in enumerate(test_cases, 1):
    response = requests.post(url, json=case)
    if response.status_code == 200:
        data = response.json()
        print(f"Test Case {i}:")
        print(f"Text: {case['text']}")
        print(f"Prediction: {data['prediction']}")
        print(f"Confidence: {data['confidence']}")
        print(f"Credibility Score: {data['credibility_score']}")
        print(f"Verdict: {data['verdict']}")
        print(f"Explanation: {data['explain']}")
        print(f"Components: {data['components']}")
        print("-" * 50)
    else:
        print(f"Test Case {i} failed with status code {response.status_code}")
