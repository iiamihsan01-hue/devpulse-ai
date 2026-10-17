"""AI engine that communicates with a local Ollama instance."""

from pydantic import BaseModel, Field
import ollama


# ------------------------------------------------------------------
# Configuration
# ------------------------------------------------------------------

DEFAULT_MODEL = "llama3"


class AIConfig(BaseModel):
    """Settings for the Ollama-backed AI engine."""

    model: str = Field(default=DEFAULT_MODEL, description="Ollama model tag to use")
    temperature: float = Field(default=0.3, ge=0.0, le=2.0)
    max_tokens: int = Field(default=1024, gt=0)


# ------------------------------------------------------------------
# Prompt templates
# ------------------------------------------------------------------

CODE_REVIEW_PROMPT = """\
You are a senior software engineer performing a code review.
Analyze the following git diff and provide:

1. **Summary** – one-paragraph overview of the changes.
2. **Issues** – potential bugs, security concerns, or style problems.
3. **Suggestions** – concrete improvements with brief rationale.

Be concise and actionable.

```diff
{diff}
```
"""

COMMIT_MSG_PROMPT = """\
You are a developer writing a git commit message following the \
Conventional Commits specification.

Based on the diff below, produce:
- A short subject line (≤72 characters) in the form `type(scope): description`
- A blank line
- An optional body with bullet points explaining *why* the change was made

Return ONLY the commit message, no extra commentary.

```diff
{diff}
```
"""


# ------------------------------------------------------------------
# Engine
# ------------------------------------------------------------------


class AIEngine:
    """Thin wrapper around the Ollama Python client.

    Parameters
    ----------
    config : AIConfig | None
        Engine settings.  Uses sensible defaults when omitted.
    """

    def __init__(self, config: AIConfig | None = None) -> None:
        self.config = config or AIConfig()
        self.client = ollama.Client()

    # ------------------------------------------------------------------
    # Public helpers
    # ------------------------------------------------------------------

    def review_code(self, diff: str) -> str:
        """Send a staged diff for code review and return the response."""
        prompt = CODE_REVIEW_PROMPT.format(diff=diff)
        return self._chat(prompt)

    def generate_commit_message(self, diff: str) -> str:
        """Generate a conventional commit message from a staged diff."""
        prompt = COMMIT_MSG_PROMPT.format(diff=diff)
        return self._chat(prompt)

    def check_connection(self) -> bool:
        """Return True if the local Ollama server is reachable."""
        try:
            self.client.list()
            return True
        except Exception:
            return False

    # ------------------------------------------------------------------
    # Internals
    # ------------------------------------------------------------------

    def _chat(self, prompt: str) -> str:
        """Send a single-turn chat completion and return the text."""
        response = self.client.chat(
            model=self.config.model,
            messages=[{"role": "user", "content": prompt}],
            options={
                "temperature": self.config.temperature,
                "num_predict": self.config.max_tokens,
            },
        )
        return response["message"]["content"]
