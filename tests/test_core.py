"""Tests for DevPulse AI modules."""

import pytest
from src.core.git_parser import GitParser
from src.core.ai_engine import AIEngine, AIConfig


class TestGitParser:
    """Test GitParser functionality."""

    def test_git_parser_initialization(self):
        """Test GitParser can be initialized."""
        parser = GitParser(".")
        assert parser.repo is not None

    def test_get_repo_root(self):
        """Test getting repository root."""
        parser = GitParser(".")
        root = parser.get_repo_root()
        assert root.exists()

    def test_get_current_branch(self):
        """Test getting current branch."""
        parser = GitParser(".")
        branch = parser.get_current_branch()
        assert isinstance(branch, str)
        assert len(branch) > 0


class TestAIEngine:
    """Test AIEngine functionality."""

    def test_ai_config_creation(self):
        """Test AIConfig can be created with defaults."""
        config = AIConfig()
        assert config.model == "llama3"
        assert config.temperature == 0.3
        assert config.max_tokens == 1024

    def test_ai_config_custom(self):
        """Test AIConfig with custom values."""
        config = AIConfig(model="qwen3.5:4b", temperature=0.5)
        assert config.model == "qwen3.5:4b"
        assert config.temperature == 0.5

    def test_ai_engine_initialization(self):
        """Test AIEngine can be initialized."""
        engine = AIEngine()
        assert engine.config is not None
        assert engine.client is not None


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
