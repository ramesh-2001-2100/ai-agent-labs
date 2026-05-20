------------------------------------------------------------------------

``` markdown
# 🚀 AnythingLLM + Ollama Setup Guide

[![Docker](https://img.shields.io/badge/Docker-ready-blue?logo=docker)](https://www.docker.com/)
[![Ollama](https://img.shields.io/badge/Ollama-installed-green)](https://ollama.com/)
[![License](https://img.shields.io/badge/license-MIT-lightgrey)](LICENSE)

A lean guide to running [AnythingLLM](https://docs.anythingllm.com/) with [Ollama](https://ollama.com/) locally.  
Covers **first‑time installation** and **next‑time startup (post reboot)**.

---

## ⚡ TL;DR Quickstart

```powershell
# First-time setup
ollama pull llama3.2:latest

docker run -d --name anythingllm `
  -p 8080:3001 `
  -e STORAGE_DIR=/app/server/storage `
  -v anythingllm_storage:/app/server/storage `
  mintplexlabs/anythingllm

# Next time startup
docker start anythingllm
```

👉 Access the UI at: `http://localhost:8080`

------------------------------------------------------------------------

## 1️⃣ First‑time setup

### Step 1: Install Ollama

- **Windows**: [Download MSI installer](https://ollama.com/download)

- **macOS/Linux**:

  ``` bash
  curl -fsSL https://ollama.com/install.sh | sh
  ```

- Verify Ollama is running:

  ``` powershell
  ollama --version
  ```

### Step 2: Pull models

- Download the chat model:

  ``` powershell
  ollama pull llama3.2:latest
  ```

- Confirm it's available:

  ``` powershell
  ollama list
  ```

### Step 3: Start Docker Desktop

- Launch Docker Desktop and wait until the whale icon shows "running."

- Test connectivity:

  ``` powershell
  docker info
  ```

### Step 4: Run AnythingLLM container

Run the container with persistent storage:

``` powershell
docker run -d --name anythingllm `
  -p 8080:3001 `
  -e STORAGE_DIR=/app/server/storage `
  -v anythingllm_storage:/app/server/storage `
  mintplexlabs/anythingllm
```

Check it's running:

``` powershell
docker ps
```

You should see `0.0.0.0:8080->3001/tcp`.

### Step 5: Open the web app

- Visit:

      http://localhost:8080

- Complete the setup wizard:

  - **Users**: "Just me"

  - **Password**: **Yes** (recommended even for personal use).

    - Without a password → anyone with access to your laptop/browser can open `http://localhost:8080` and use the instance.

    - With a password → adds a login step, protects against accidental or unauthorized use.

  - **Chat LLM**: `llama3.2:latest` (via Ollama).

  - **Vector DB**: choose default option, built‑in, good for personal use).

### Step 6: ⚠️ Switch from "Agent" to "Standard Chat" Mode

By default, AnythingLLM might automatically start a new thread in **Agent Execution** mode (`@agent`). Smaller local models like `llama3.2` can get stuck in a loop trying to call background software tools instead of simply talking to you.

If you see a message stating `@agent: Swapping over to agent chat`:

1.  Type `/exit` in the chat bar and press Enter to terminate any active loops.

2.  Navigate to your **Workspace Settings** (the gear icon next to your workspace name in the left sidebar) or look at the thread-specific control toggles.

3.  Ensure the default chat handling preference is explicitly set to **Normal Chat / Query** rather than Agent execution.

4.  ## Alternatively, click **New Thread** and avoid invoking the `@agent` command or selecting active tools to keep the communication standard and fast.

## 2️⃣ Next‑time startup (post reboot)

### Step 1: Ensure Ollama is running

- Ollama usually starts automatically.

- Test with:

  ``` powershell
  ollama run llama3.2:latest
  ```

### Step 2: Start Docker Desktop

- Launch Docker Desktop and wait until it's active.

### Step 3: Start the AnythingLLM container

``` powershell
docker start anythingllm
```

### Step 4: Open the web app

    http://localhost:8080

## \### Step 5: Post

## 🛠️ Troubleshooting

- **Container name conflict**

  ``` powershell
  docker stop anythingllm
  docker rm anythingllm
  ```

  Then rerun the `docker run …` command.

- **Check logs** if the app doesn't load:

  ``` powershell
  docker logs -f anythingllm
  ```

  Look for `Primary server in HTTP mode listening on port 3001`.

### Ensure nothing is changed on UI configuration

ensure you double check the any UI configuration as per Step 6 above. If any new changes, please revert to original changes.

------------------------------------------------------------------------

## 📜 License

MIT
