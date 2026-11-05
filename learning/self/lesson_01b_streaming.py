# lesson_01b_streaming.py — same chat call as lesson_01, but stream tokens as they arrive
#
# Preconditions: valid OPENAI_API_KEY (see comments at top of lesson_01_first_call.py).
#
import os
from openai import OpenAI
from dotenv import find_dotenv, load_dotenv

load_dotenv(find_dotenv(usecwd=True), override=True)

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Same multi-turn messages as lesson_01_first_call.py (for easy comparison)
messages = [
    {"role": "user", "content": "What is an LLM?"},
    {"role": "assistant", "content": "An LLM is a model trained on text..."},
    {"role": "user", "content": "Give one real-world use."},
]

# stream=True → API returns chunks over time instead of one full response object
stream = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=messages,
    stream=True,
)

print("LLM says:", end=" ", flush=True)

# Each chunk may contain a small piece of text in delta.content (or None)
full_answer_parts: list[str] = []
for chunk in stream:
    delta = chunk.choices[0].delta
    piece = delta.content  # str fragment, or None for some chunks
    if piece:
        print(piece, end="", flush=True)  # print immediately (no waiting for full reply)
        full_answer_parts.append(piece)

print()  # newline after the streamed reply

# Optional: full text if you still need the complete string afterward
full_answer = "".join(full_answer_parts)
# print("\n(Full answer length:", len(full_answer), "chars)")
