# lesson_01a_tokens_and_usage.py — same first call, plus token/cost reporting
import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()  # Load API key from .env file

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

response = client.chat.completions.create(
    model="gpt-4o-mini",  # The LLM model to use
    messages=[
        {"role": "user", "content": "What is an LLM?"},
        {"role": "assistant", "content": "An LLM is a model trained on text..."},
        {"role": "user", "content": "Give one real-world use."},
    ],
)

# Extract and print the reply
answer = response.choices[0].message.content
print("LLM says:", answer)

# --- Tokens / cost (usage is returned by the API after each call) ---
usage = response.usage
prompt_tokens = usage.prompt_tokens  # input: your messages (and system prompt if any)
completion_tokens = usage.completion_tokens  # output: the model's reply
total_tokens = usage.total_tokens  # prompt + completion

print()
print("Token usage:")
print(f"  prompt_tokens:     {prompt_tokens}")
print(f"  completion_tokens: {completion_tokens}")
print(f"  total_tokens:      {total_tokens}")

# Approximate list prices for gpt-4o-mini (USD per 1 million tokens).
# Check https://openai.com/api/pricing for current numbers — they can change.
PRICE_PER_1M_INPUT = 0.15
PRICE_PER_1M_OUTPUT = 0.60

est_cost_usd = (
    prompt_tokens * PRICE_PER_1M_INPUT / 1_000_000
    + completion_tokens * PRICE_PER_1M_OUTPUT / 1_000_000
)
print(f"  estimated_cost_usd: ${est_cost_usd:.6f}  (approx.; rates may be outdated)")
