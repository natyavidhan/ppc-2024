import requests

headers = {
    'Content-Type': 'application/json',
}

params = {
    'key': 'key',
}

json_data = {
    'contents': [
        {
            'parts': [
                {
                    'text': 'Explain how AI works',
                },
            ],
        },
    ],
}

response = requests.post(
    'https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash-latest:generateContent',
    params=params,
    headers=headers,
    json=json_data,
)
print(response.text)