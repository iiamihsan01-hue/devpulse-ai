# DevPulse AI

**Offline AI-powered developer assistant** that runs locally using Ollama and analyzes git repositories.

[![GitHub](https://img.shields.io/badge/GitHub-iiamihsan01--hue%2Fdevpulse--ai-blue?logo=github)](https://github.com/iiamihsan01-hue/devpulse-ai)
[![Python](https://img.shields.io/badge/Python-3.10%2B-blue?logo=python)](https://python.org)
[![License](https://img.shields.io/badge/License-MIT-green)](LICENSE)

## 🚀 Features

- **Code Review** — AI-powered analysis of staged changes using local LLMs
- **Commit Message Generation** — Automatic conventional commit messages
- **Git Integration** — Extract diffs and commit history directly from repos
- **Offline & Private** — Runs entirely locally with Ollama, no cloud dependencies
- **Rich CLI Output** — Beautiful formatted output with Rich library
- **Multi-Model Support** — Works with any Ollama-compatible model

## 📋 Quick Start

### Prerequisites

- Python 3.10+
- [Ollama](https://ollama.com) installed and running
- A git repository to analyze

### Installation

```bash
# Clone the repository
git clone https://github.com/iiamihsan01-hue/devpulse-ai.git
cd devpulse-ai

# Create virtual environment
python -m venv .venv
.venv\Scripts\activate  # Windows
# source .venv/bin/activate  # macOS/Linux

# Install dependencies
pip install -e .
```

### Setup Ollama

```bash
# In a separate terminal, start Ollama
ollama serve

# In another terminal, pull a model (first time only)
ollama pull llama2
# or use another model:
ollama pull qwen3.5:4b
```

### Usage

```bash
# Show recent commits
devpulse log -n 10

# Review staged changes with AI
git add .
devpulse audit --model qwen3.5:4b

# Generate a commit message
devpulse commit --model qwen3.5:4b
```

## 📖 Commands

### `devpulse audit`
Review staged code changes using a local LLM for bugs, style issues, and suggestions.

```bash
git add src/myfile.py
devpulse audit --model qwen3.5:4b
```

**Options:**
- `--model, -m` — Ollama model to use (default: `llama3`)
- `--repo, -r` — Path to git repository (default: `.`)

---

### `devpulse commit`
Generate a conventional commit message from staged changes.

```bash
git add src/feature.py
devpulse commit
```

Then confirm whether to apply the generated message. If approved, the commit is created automatically.

**Options:**
- `--model, -m` — Ollama model to use (default: `llama3`)
- `--repo, -r` — Path to git repository (default: `.`)

---

### `devpulse log`
Display recent commit history in a formatted table.

```bash
devpulse log -n 20
```

**Options:**
- `--count, -n` — Number of commits to show (default: `10`)
- `--repo, -r` — Path to git repository (default: `.`)

## 🏗️ Project Structure

```
devpulse-ai/
├── src/
│   ├── core/
│   │   ├── git_parser.py      # Git repository analysis
│   │   └── ai_engine.py       # Ollama LLM client
│   └── cli/
│       └── main.py            # Typer CLI commands
├── pyproject.toml             # Package configuration
├── requirements.txt           # Dependencies
└── README.md                  # This file
```

## 🔧 Architecture

### `GitParser` (git_parser.py)
Extracts git data from repositories:
- `get_staged_diff()` — Returns unified diff of staged changes
- `get_recent_commits()` — Fetches commit history
- `has_staged_changes()` — Checks if index has changes

### `AIEngine` (ai_engine.py)
Communicates with local Ollama instance:
- `review_code(diff)` — Performs code review analysis
- `generate_commit_message(diff)` — Creates conventional commits
- `check_connection()` — Verifies Ollama is reachable

### CLI (main.py)
Typer-based command-line interface with Rich formatted output:
- Rich panels for readable feedback
- Spinner animations during processing
- Error handling with graceful messages

## 🔌 Ollama Models

DevPulse AI works with any Ollama model. Recommended:

| Model | Size | Speed | Quality | Command |
|---|---|---|---|---|
| `llama2` | 3.8GB | Fast | Good | `ollama pull llama2` |
| `qwen3.5:4b` | 3.3GB | Fast | Excellent | `ollama pull qwen3.5:4b` |
| `mistral` | 4.1GB | Medium | Very Good | `ollama pull mistral` |
| `llama2-uncensored` | 3.8GB | Fast | Good | `ollama pull llama2-uncensored` |

Default is `llama3` if available.

## 📦 Dependencies

- **typer** — CLI framework
- **rich** — Beautiful terminal output
- **GitPython** — Git repository parsing
- **ollama** — Ollama Python client
- **pydantic** — Data validation

## 🎯 Use Cases

### 1. Local Code Review
Review your staged changes before committing:
```bash
devpulse audit
```

### 2. Conventional Commits
Generate proper commit messages automatically:
```bash
devpulse commit
```

### 3. Commit History
Quickly view recent work:
```bash
devpulse log -n 20
```

### 4. Team Workflow
Integrate into CI/CD for local pre-commit checks:
```bash
#!/bin/bash
devpulse audit || exit 1
git commit -m "$(devpulse commit --quiet)"
```

## 🚀 Coming Soon

- [ ] Web UI dashboard
- [ ] REST API endpoints
- [ ] Batch repository analysis
- [ ] Custom prompt templates
- [ ] Multiple repository support
- [ ] Configuration file (.devpulse.yaml)
- [ ] Docker containerization
- [ ] GitHub Actions integration

## 🛠️ Development

### Running Tests

```bash
# Install dev dependencies
pip install -e ".[dev]"

# Run tests
pytest tests/
```

### Adding New Commands

1. Create a new function in `src/cli/main.py`
2. Decorate with `@app.command()`
3. Use `GitParser` and `AIEngine` for functionality
4. Format output with Rich components

Example:
```python
@app.command()
def new_command(option: str = typer.Option("default")):
    """Description of the command."""
    parser = GitParser()
    engine = AIEngine()
    # Your implementation
    console.print("[green]Done![/]")
```

## 📝 License

This project is licensed under the [MIT License](LICENSE).

## 👨‍💻 Author

Created by **Najeeb** — AI developer assistant for local code analysis.

## 🤝 Contributing

Contributions are welcome! Please:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## ⚡ Quick Tips

- **Faster Processing:** Use smaller models like `qwen3.5:4b` for faster responses
- **Better Quality:** Use larger models like `mistral` for more detailed analysis
- **Offline First:** DevPulse AI requires no internet after models are downloaded
- **Local Privacy:** All code analysis happens on your machine

## 🐛 Troubleshooting

### Error: "Cannot reach Ollama"
- Make sure Ollama is running: `ollama serve`
- Check if port 11434 is accessible: `netstat -ano | findstr :11434`
- Verify Ollama is in PATH: `ollama --version`

### Error: "Model not found"
- Pull the model first: `ollama pull qwen3.5:4b`
- List available models: `ollama list`

### Command hangs
- Check Ollama process is running
- Try a smaller model for faster responses
- Increase timeout if processing large diffs

## 📞 Support

Have questions? Open an issue on GitHub:
👉 [GitHub Issues](https://github.com/iiamihsan01-hue/devpulse-ai/issues)

---

**Status:** ✅ Fully functional | **Last Updated:** October 2026
