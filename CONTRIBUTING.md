# Contributing to Socratic Mandate™

Thank you for your interest in contributing to the Socratic Mandate™ framework!

## Before You Start

Please read and understand the following:

### License

This project uses the **MIT License** for source code. By contributing, you agree that your contributions will be licensed under MIT.

### Trademarks

The following are trademarks of Nicholas Reid Angell and are **NOT** covered by the MIT License:

- Socratic Mandate™
- SocrAI:Verify™
- Trust Resilience Score™
- TRS™
- Socratic Green Team™

**Do not** use these trademarks in your contributions in ways that imply endorsement or official status. See [TRADEMARKS.md](TRADEMARKS.md) for details.

### Open Mathematics

**Angell's Laws** (the mathematical framework) is open academic work under MIT License with DOI. You are free to use, extend, and build upon this mathematics with attribution.

## How to Contribute

### Reporting Issues

1. Check existing issues first
2. Use the issue template
3. Include reproduction steps
4. Specify your environment

### Code Contributions

1. **Fork** the repository
2. **Create a branch** for your feature (`git checkout -b feature/amazing-feature`)
3. **Write tests** for new functionality
4. **Follow the code style** (we use Black, Ruff, and mypy)
5. **Commit** with clear messages
6. **Push** to your fork
7. **Open a Pull Request**

### Code Style

```bash
# Format code
black src/ tests/

# Lint
ruff check src/ tests/

# Type check
mypy src/
```

### Running Tests

```bash
# Install dev dependencies
pip install -e ".[dev]"

# Run tests
pytest

# With coverage
pytest --cov=src --cov-report=html
```

## Areas for Contribution

We especially welcome contributions in:

- **New LLM Provider Support**: Add support for additional LLM providers
- **Language Support**: Internationalization of friction prompts
- **PII Detection**: Improved patterns for different jurisdictions
- **TRS Analyzers**: More sophisticated semantic analysis
- **Documentation**: Tutorials, guides, translations
- **Testing**: Increased test coverage

## Code of Conduct

- Be respectful and inclusive
- Focus on constructive feedback
- Help others learn
- Report unacceptable behavior

## Questions?

Open a discussion or issue if you have questions about contributing.

---

**Thank you for helping make AI safer for everyone.**
