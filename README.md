

```markdown
# 🔬 AI Agent Labs & Engineering Hub

Welcome to my central playground for building local-first agentic workflows, multi-cloud architectures, and foundational programming scripts. This repository tracks my ongoing transition into AI platform development and advanced backend systems.

---

## 🗺️ Project Architecture

* **`ai_agents/`**: Hands-on exploration of local agentic patterns. Includes code snippets analyzing the `ReAct` framework and custom tool execution loops using lightweight models via Ollama.
* **`cloud/`**: Infrastructure-as-Code engineering labs. Focuses on cloud security architectures, such as cross-account S3 bucket replication using Terraform.
* **`research/`**: Core non-AI Python foundations. A structured sandbox for practicing robust script writing, algorithmic problem solving, exception handling, and handling variable scopes.
* **`docs/`**: Source markdown documentation files compiled and automatically served on the web via GitHub Pages.

---

## 🌐 Live Documentation Dashboard

I maintain a live, hosted index mapping out my learning tracks, environment configurations, and deep dives for this repository. 

👉 **[Visit the Live Labs Dashboard](https://ramesh-2001-2100.github.io/ai-agent-labs/)**



## 🛠️ Local Development & Prerequisites

To safely run the scripts in this repository without disturbing global system files, configure a localized Python virtual environment:

### 1. Initialize the Virtual Environment
```powershell
# Navigate to project root and create venv
python -m venv .venv

# Activate on Windows (PowerShell)
.\.venv\Scripts\Activate.ps1

```

### 2. Install Dependencies

```powershell
pip install -r requirements.txt

```

### 3. Local Hardware Compute Setup

For the advanced workflows in the `/ai_agents` directory, your machine needs local execution runtimes to process foundational text and data models privately:

* **Containerization**: [Docker Desktop](https://www.docker.com/) for isolated service management.
* **Inference Engine**: [Ollama](https://ollama.com/) running a standard `llama3.2:latest` model for fast local text processing.

---

## 📜 License

MIT

