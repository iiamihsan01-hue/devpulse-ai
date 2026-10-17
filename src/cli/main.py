"""DevPulse AI – offline developer assistant powered by Ollama.

Usage
-----
    devpulse audit          Review staged changes
    devpulse commit         Generate a commit message for staged changes
    devpulse log            Show recent commit history
"""

import typer
from rich.console import Console
from rich.markdown import Markdown
from rich.panel import Panel

from src.core.ai_engine import AIEngine, AIConfig
from src.core.git_parser import GitParser

# ------------------------------------------------------------------
# App setup
# ------------------------------------------------------------------

app = typer.Typer(
    name="devpulse",
    help="Offline AI-powered developer assistant for git repositories.",
    add_completion=False,
)
console = Console()


# ------------------------------------------------------------------
# Shared helpers
# ------------------------------------------------------------------


def _ensure_ollama(engine: AIEngine) -> None:
    """Exit early when the local Ollama server is unreachable."""
    if not engine.check_connection():
        console.print(
            "[bold red]Error:[/] Cannot reach Ollama. "
            "Make sure it is running (`ollama serve`)."
        )
        raise typer.Exit(code=1)


def _ensure_staged(parser: GitParser) -> str:
    """Return the staged diff or exit if nothing is staged."""
    if not parser.has_staged_changes():
        console.print(
            "[bold yellow]Nothing staged.[/] "
            "Stage changes with `git add` first."
        )
        raise typer.Exit(code=1)
    return parser.get_staged_diff()


# ------------------------------------------------------------------
# Commands
# ------------------------------------------------------------------


@app.command()
def audit(
    model: str = typer.Option(
        "llama3", "--model", "-m", help="Ollama model to use for the review"
    ),
    repo: str = typer.Option(
        ".", "--repo", "-r", help="Path to the git repository"
    ),
) -> None:
    """Review staged code changes using a local LLM."""
    parser = GitParser(repo)
    engine = AIEngine(AIConfig(model=model))

    _ensure_ollama(engine)
    diff = _ensure_staged(parser)

    with console.status("[bold cyan]Analyzing staged changes…"):
        review = engine.review_code(diff)

    console.print(Panel(Markdown(review), title="Code Review", border_style="green"))


@app.command()
def commit(
    model: str = typer.Option(
        "llama3", "--model", "-m", help="Ollama model to use"
    ),
    repo: str = typer.Option(
        ".", "--repo", "-r", help="Path to the git repository"
    ),
) -> None:
    """Generate a commit message for staged changes using a local LLM."""
    parser = GitParser(repo)
    engine = AIEngine(AIConfig(model=model))

    _ensure_ollama(engine)
    diff = _ensure_staged(parser)

    with console.status("[bold cyan]Generating commit message…"):
        message = engine.generate_commit_message(diff)

    console.print(Panel(message, title="Suggested Commit Message", border_style="blue"))

    if typer.confirm("Use this commit message?"):
        parser.repo.git.commit("-m", message)
        console.print("[bold green]✓ Committed![/]")
    else:
        console.print("[dim]Commit cancelled.[/]")


@app.command()
def log(
    count: int = typer.Option(
        10, "--count", "-n", help="Number of recent commits to show"
    ),
    repo: str = typer.Option(
        ".", "--repo", "-r", help="Path to the git repository"
    ),
) -> None:
    """Show recent commit history for the repository."""
    parser = GitParser(repo)
    commits = parser.get_recent_commits(count)

    if not commits:
        console.print("[yellow]No commits found.[/]")
        raise typer.Exit()

    from rich.table import Table

    table = Table(title=f"Recent Commits ({parser.get_current_branch()})")
    table.add_column("SHA", style="cyan", width=8)
    table.add_column("Date", style="green", width=16)
    table.add_column("Author", style="magenta", width=20)
    table.add_column("Message", style="white")

    for c in commits:
        table.add_row(c.sha, c.date, c.author, c.message)

    console.print(table)


# ------------------------------------------------------------------
# Entry point
# ------------------------------------------------------------------

if __name__ == "__main__":
    app()
