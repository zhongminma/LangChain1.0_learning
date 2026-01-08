import os
from google import genai

client = genai.Client(api_key=os.environ["GOOGLE_API_KEY"])

for m in client.models.list():
    name = getattr(m, "name", None)
    methods = getattr(m, "supported_generation_methods", None)
    if name:
        print(name, methods)
