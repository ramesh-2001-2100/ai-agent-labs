# lesson_01c_temperature.py — system prompt = poem; compare low vs high temperature
#
# Preconditions: valid OPENAI_API_KEY (see comments at top of lesson_01_first_call.py).
#
import os
from openai import OpenAI
from dotenv import find_dotenv, load_dotenv

load_dotenv(find_dotenv(usecwd=True), override=True)

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# System steers *style*; user supplies *topic*
messages = [
    {
        "role": "system",
        "content": (
            "You are a poet. For whatever the user asks about, respond ONLY with a short poem "
            "(4–8 lines). Do not write an essay or bullet list—only a poem."
        ),
    },
    {
        "role": "user",
        "content": "What is an LLM?",
    },
]

# temperature: 0 ≈ deterministic/safer; higher ≈ more random/creative
# Typical range for chat models: 0.0 – 2.0 (defaults often around 1.0)
temperatures = [0.0, 1.2]

for temp in temperatures:
    print("=" * 50)
    print(f"temperature = {temp}")
    print("=" * 50)

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=messages,
        temperature=temp,
    )

    answer = response.choices[0].message.content
    print(answer)
    print()
