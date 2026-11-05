# lesson_01_first_call.py
#
# Preconditions (API key):
# - Put OPENAI_API_KEY=sk-... in the repo-root .env (ai-agent-labs/.env).
#   find_dotenv() walks up from cwd, so running from learning/self still finds it.
#
# Why a "new terminal" does NOT always fix 401 Incorrect API key:
# - A key set only in that shell dies with the shell. A new terminal helps then.
# - A key set as a Windows *User* or *Machine* environment variable is loaded into
#   every new terminal and every app (including Grok). A new session re-inherits it.
# - python-dotenv's default load_dotenv() does NOT overwrite variables already in
#   os.environ, so a stale User/Machine OPENAI_API_KEY wins over .env and you get 401.
#
# This script loads the nearest .env with override=True so the repo key is used.
# To clean up a permanent stale key on Windows (optional):
#   [Environment]::SetEnvironmentVariable('OPENAI_API_KEY', $null, 'User')
#   then open a new terminal (or update User env to the current key).
#
import os
from openai import OpenAI
from dotenv import find_dotenv, load_dotenv

# Prefer repo .env over a stale User/Machine OPENAI_API_KEY already in the process.
load_dotenv(find_dotenv(usecwd=True), override=True)

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
