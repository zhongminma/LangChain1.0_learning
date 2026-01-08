import os
from typing import Any

from google import genai
from google.genai import types

client = genai.Client(api_key=os.environ["GOOGLE_API_KEY"])

def gemini_llm(prompt: Any) -> str:
    response = client.models.generate_content(
        model="models/gemini-2.0-flash",
        contents=prompt,
        config=types.GenerateContentConfig(
            temperature=0.1,
            max_output_tokens=256,
        ),
    )
    return response.text
