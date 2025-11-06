from openai import OpenAI
import os

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

try:
    models = client.models.list()
    print("✅ API key is valid! Total models available:", len(models.data))
except Exception as e:
    print("⚠️ Error:", e)
