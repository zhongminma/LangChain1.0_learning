from typing import Any
from google import genai
from google.genai import types
client = genai.Client()
# text generation docs: https://ai.google.dev/gemini-api/docs/text-generation?authuser=2
def gemini_llm(prompt: Any) -> Any:
    response = client.models.generate_content(
        model="models/gemini-flash-latest",
        contents=prompt,
        config=types.GenerateContentConfig(
            temperature=0.5,
        ),
    )
    return response.text
