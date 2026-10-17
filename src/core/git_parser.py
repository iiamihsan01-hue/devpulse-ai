"""Git repository parser for extracting diffs and commit history."""

from dataclasses import dataclass
from pathlib import Path

import git


@dataclass
class CommitInfo:
    """Lightweight representation of a single git commit."""

    sha: str
    author: str
    message: str
    date: str


class GitParser:
    """Reads staged diffs and recent commit logs from a local git repo.

    Parameters
    ----------
    repo_path : str | Path
        Root directory of the git repository.  Defaults to the current
        working directory.
    """

    def __init__(self, repo_path: str | Path = ".") -> None:
        self.repo = git.Repo(repo_path, search_parent_directories=True)

    # ------------------------------------------------------------------
    # Staged diff
    # ------------------------------------------------------------------

    def get_staged_diff(self) -> str:
        """Return the unified diff of all staged (index) changes.

        Returns an empty string when nothing is staged.
        """
        return self.repo.git.diff("--cached")

    def has_staged_changes(self) -> bool:
        """Check whether the index contains any staged changes."""
        return bool(self.repo.git.diff("--cached", "--name-only"))

    # ------------------------------------------------------------------
    # Commit log
    # ------------------------------------------------------------------

    def get_recent_commits(self, count: int = 10) -> list[CommitInfo]:
        """Return the *count* most recent commits on the current branch.

        Parameters
        ----------
        count : int
            Maximum number of commits to return.
        """
        commits: list[CommitInfo] = []
        for c in self.repo.iter_commits(max_count=count):
            commits.append(
                CommitInfo(
                    sha=c.hexsha[:8],
                    author=str(c.author),
                    message=c.message.strip(),
                    date=c.committed_datetime.strftime("%Y-%m-%d %H:%M"),
                )
            )
        return commits

    # ------------------------------------------------------------------
    # Helpers
    # ------------------------------------------------------------------

    def get_current_branch(self) -> str:
        """Return the name of the active branch."""
        return str(self.repo.active_branch)

    def get_repo_root(self) -> Path:
        """Return the absolute path of the repository root."""
        return Path(self.repo.working_dir)
