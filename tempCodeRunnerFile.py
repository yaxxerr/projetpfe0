import requests

API_KEY = "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"  # <--- Put your real OpenRouter API key here

headers = {
    "Authorization": f"Bearer {API_KEY}"
}

response = requests.get("https://openrouter.ai/api/v1/auth/key", headers=headers)

print("Status code:", response.status_code)
print("Response:", response.json())