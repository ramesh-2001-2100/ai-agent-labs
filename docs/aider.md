# Using Aider (AI Pair Programming in the Terminal)

Aider is a **pre-existing, standalone tool** (https://aider.chat).  
It is **not** code you write yourself. You install the `aider-chat` package once and then use the `aider` command to have an LLM edit your codebase conversationally.

## What Aider Actually Is

- You run `aider` inside a git repository.
- You chat with a powerful model (GPT-4o, Claude 3.5 Sonnet, etc.).
- You say things in plain English:
  - "Add error handling to the email parser"
  - "Refactor ReAct.py to use a proper tool registry"
  - "Write a test for the stack class"
- Aider reads relevant files, builds a repo map, proposes **precise edits**, shows diffs, and applies them when you approve.
- It can run tests, lint, commit changes, etc.

This is the real "aider chat" experience.

## Prerequisites (already set up here)

- `aider` CLI is installed (`aider --version`)
- OpenAI key is in `.env` (Aider picks it up automatically)
- This is a git repo (Aider likes working inside git repos)

## Basic Usage

### Start an interactive chat session

```powershell
cd C:\Users\lrame\code\ai-agent-labs
aider
```

Aider will start, show the model, and give you a prompt like:

```
aider> 
```

Type normal requests. Type `/help` inside the session for built-in commands.

### One-shot request (no interactive shell)

```powershell
aider --message "Explain the structure of the ReAct agent and suggest one improvement"
```

### Work on specific files only

```powershell
aider ai_agents/local_agent.py research/app.py
```

### Popular shortcuts (Aider supports these flags)

```powershell
aider --4o                 # gpt-4o
aider --sonnet             # Claude 3.5 Sonnet (if you have Anthropic key)
aider --mini               # cheaper/faster model
aider --no-auto-commits    # don't commit automatically
aider --watch-files        # watch for external file changes
aider --lint               # run linter after edits
```

See all options:

```powershell
aider --help
```

## Using Aider from Custom Code (Python)

You rarely need to. The best "integration" is usually just calling the CLI.

### Simple subprocess wrapper

```python
import subprocess
from pathlib import Path

def run_aider(message: str, files: list[str] = None, auto_commit: bool = False):
    cmd = ["aider", "--message", message]
    if files:
        cmd.extend(files)
    if not auto_commit:
        cmd.append("--no-auto-commits")
    
    # Run from the repo root
    result = subprocess.run(
        cmd,
        cwd=Path(__file__).parent.parent,
        capture_output=True,
        text=True
    )
    return result.stdout, result.stderr

# Example
out, err = run_aider("Add a docstring to the main function", ["research/app.py"])
print(out)
```

### Even simpler: just shell out

```python
import os
os.system('aider --message "your request" --no-auto-commits')
```

## Recommended Starting Commands in This Repo

```powershell
# 1. Just explore (read-only feel)
aider --dry-run --message "What are the main folders and what do they contain?"

# 2. Start a real session focused on one area
aider --message "Help me improve the local agent examples" ai_agents/

# 3. Quick analysis
aider --message "Review the Terraform file for security issues" cloud/s3_cross_account_replication.tf
```

## Useful In-Session Commands (once inside `aider>`)

- `/add file.py` — add more files to context
- `/drop file.py` — remove from context
- `/ls` — list tracked files
- `/git ...` — run git commands
- `/undo` — undo the last change
- `/clear` — clear chat history
- `/help`

## Configuration

Aider reads:

- Environment variables / `.env` (already working)
- `.aider.conf.yml` in the repo root (optional)

Example `.aider.conf.yml`:

```yaml
model: gpt-4o
auto-commits: false
dirty-commits: false
```

## Notes

- `.aider*` files (chat history, caches) are already ignored in `.gitignore`.
- Aider works best when the repo is clean or you understand the current changes.
- It supports many providers: OpenAI, Anthropic, Ollama (local models), etc.

## Official Resources

- Website: https://aider.chat
- Docs: https://aider.chat/docs/
- GitHub: https://github.com/paul-gauthier/aider

---

This is the real Aider experience. The previous `aider_chat/` Python wrapper was not using Aider at all — it was a basic OpenAI chat script and has been removed.
