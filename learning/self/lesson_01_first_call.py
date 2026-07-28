# lesson_01_first_call.py
import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()  # Load API key from .env file

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

response = client.chat.completions.create(
    model="gpt-4o-mini",       # The LLM model to use
    messages=[
        {"role": "user", "content": "What is an LLM?"},
        {"role": "assistant", "content": "An LLM is a model trained on text..."},
        {"role": "user", "content": "Give one real-world use."},
    ]
)

# Extract and print the reply
answer = response.choices[0].message.content
print("LLM says:", answer)
