import os
import requests

API_URL = "https://router.huggingface.co/hf-inference/models/facebook/bart-large-cnn"

headers = {
    "Authorization": f"Bearer {os.getenv('HF_API_KEY')}"
}

def summarize_text(text):
    try:
        payload = {
            "inputs": text[:2000]
        }

        response = requests.post(API_URL, headers=headers, json=payload)
        result = response.json()

        if isinstance(result, list) and 'summary_text' in result[0]:
            return result[0]['summary_text']
        elif isinstance(result, dict) and 'error' in result:
            return f"API Error: {result['error']}"
        else:
            return str(result)

    except Exception as e:
        return f"Error: {str(e)}"