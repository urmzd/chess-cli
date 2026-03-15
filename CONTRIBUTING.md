# Contributing

Thanks for your interest in contributing to **chess-cli**.

## Prerequisites

- **Python 3.12+** — install via [pyenv](https://github.com/pyenv/pyenv) or your OS package manager
- **[uv](https://docs.astral.sh/uv/)** — Python package and project manager
- **[just](https://github.com/casey/just)** — command runner
- **[GH_TOKEN](https://cli.github.com/)** — GitHub CLI authentication (for releases)

## Getting Started

```sh
git clone https://github.com/urmzd/chess-cli.git
cd chess-cli
just init
```

## Development

| Command | What it does |
|---------|-------------|
| `just fmt` | Check formatting (ruff) |
| `just fmt-fix` | Fix formatting |
| `just lint` | Check lints (ruff) |
| `just lint-fix` | Fix lints |
| `just typecheck` | Run mypy |
| `just test` | Run pytest |
| `just ci` | Full CI check (fmt + lint + typecheck + test) |

## Commit Convention

This project uses [Conventional Commits](https://www.conventionalcommits.org/) enforced via [gitit](https://github.com/urmzd/gitit):

| Prefix | Purpose |
|--------|---------|
| `feat` | New feature |
| `fix` | Bug fix |
| `docs` | Documentation |
| `refactor` | Refactoring |
| `test` | Tests |
| `chore` | Maintenance |
| `ci` | CI changes |

Format: `type(scope): description`

## Pull Requests

1. Fork the repository
2. Create a feature branch (`feat/your-feature`)
3. Make your changes and ensure `just ci` passes
4. Push to your fork and open a Pull Request
5. Keep PRs focused — one logical change per PR

## Code Style

- **ruff** for formatting and linting (line-length 100)
- **mypy** for type checking
- Frozen Pydantic models for immutable state
- Conventional Commits enforced via pre-commit hook
