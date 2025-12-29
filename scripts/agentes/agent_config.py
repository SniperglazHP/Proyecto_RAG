from openai import OpenAI
import os

# Cliente OpenAI con tu API Key
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
