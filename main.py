import os
import requests
import re

neuranet_api_key = os.getenv('NEURANET_API_KEY') # save your NeuraNET API key as an environment variable

user_message = input("Enter Task: ")

data = {
    "settings": {
        "model": "nlite"
    },
    "conversation": {
        "history": [
            {
                "sender": "instruct",
                "content": "You are an expert in python. Only provide python code as output. Never output any text before or after the python code, as the output will be directly executed in a shell. Only give the code, no explanations or descriptions, do not put the code in codeblocks either (```)."
            },
            {
                "sender": "user",
                "content": f"Create a Python script for: {user_message}"
            }
        ]
    }
}

headers = {
    "Authorization": f"Bearer {neuranet_api_key}",
    "Content-Type": "application/json"
}
response = requests.post("https://neuranet-ai.com/api/v1/chat", headers=headers, json=data) # send request to API

generated_code = response.json()['choices'][0]['text']

match = re.search(r'```python\s*(.*?)\s*```', generated_code, re.DOTALL) # just in case
if match:
    generated_code = match.group(1)
else:
    pass

try:
    exec(generated_code)
except Exception as e:
    print(f"An error occurred during execution: {e}")
    print("Generated Code:\n" + generated_code)
