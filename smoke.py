import os
from google import genai
from pydantic import BaseModel

class Hello(BaseModel):
    greeting: str

client = genai.Client(api_key=os.environ['GEMINI_API_KEY'])
r = client.models.generate_content(
    model=os.environ['GEMINI_MODEL'],
    contents='Greet a college student in one short sentence.',
    config={'response_mime_type': 'application/json',
            'response_schema': Hello},
)
print(r.parsed)