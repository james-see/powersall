# Powerball Analysis Tool

![Python 3.14+](https://img.shields.io/badge/python-3.14+-blue.svg)
![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)
[![GitHub Pages](https://img.shields.io/badge/docs-GitHub%20Pages-green.svg)](https://jamesacampbell.github.io/powersall)

Advanced Powerball lottery analysis and number generator tool with comprehensive statistical analysis, pattern detection, and interactive visualizations.

## Features

- **📊 Frequency Analysis**: Analyze number frequency patterns across thousands of Powerball draws
- **🔥 Hot/Cold Numbers**: Identify trending hot and cold numbers based on recent games
- **📈 Pattern Detection**: Discover patterns like odd/even distributions, sum ranges, and consecutive numbers
- **🎲 Smart Number Generator**: Generate numbers using statistical weighting based on historical data
- **🖥️ Interactive Web Interface**: Use the Streamlit web interface for intuitive analysis
- **📊 Data Visualizations**: Create interactive charts and graphs with modern web technologies
- **🚀 Modern Python**: Built with Python 3.14+ and modern package management using `uv`

## Installation

### Using uv (Recommended)

```bash
# Install uv if you haven't already
curl -LsSf https://astral.sh/uv/install.sh | sh

# Install the package
uv pip install powersall

# Or install in development mode
uv pip install -e .
```

### Using pip

```bash
pip install powersall
```

### Development Setup

```bash
# Clone the repository
git clone https://github.com/jamesacampbell/powersall.git
cd powersall

# Install with uv (recommended)
uv pip install -e ".[dev]"

# Or with pip
pip install -e ".[dev]"

# Quick development commands using Makefile
make help              # Show available commands
make install           # Install in development mode
make test             # Run tests
make lint             # Run linting and type checking
make format           # Format code
make build            # Build package
```

## Usage

### Command Line Interface

#### Basic Commands

```bash
# Show numbers for a specific date
powersall --date 2023-12-01

# Generate random numbers
powersall --pick

# Show frequency analysis
powersall --analysis

# Show hot/cold numbers
powersall --hot-cold

# Show pattern analysis
powersall --patterns

# Create interactive visualizations
powersall --visualize

# Launch web interface
powersall --web

# Save generated numbers to JSON
powersall --pick --save-db
```

#### Examples

```bash
# Get Powerball numbers for New Year's Day 2024
powersall -d "2024-01-01"

# Generate smart numbers based on recent trends
powersall --pick

# Analyze the last 100 games for hot/cold patterns
powersall --hot-cold

# Detect odd/even and sum patterns
powersall --patterns
```

### Web Interface

For a more interactive experience, use the Streamlit web interface:

```bash
powersall --web
```

This launches a web application where you can:
- Explore datasets interactively
- View real-time frequency analysis
- Generate visualizations on demand
- Analyze patterns with dynamic filtering

### Python API

```python
from powersall.functions import analyze_frequency, get_hot_cold_numbers, randomeyes
import pandas as pd

# Load your Powerball data
df = pd.read_csv("~/powerball.csv")

# Analyze frequency patterns
analyze_frequency(df)

# Get hot/cold numbers
get_hot_cold_numbers(df, recent_games=50)

# Generate random numbers
numbers = randomeyes()
print(f"Your numbers: {[numbers[i] for i in range(1, 6)]}")
print(f"Powerball: {numbers['powerball']}")
```

## Analysis Features

### Frequency Analysis
- **Most/Least Common Numbers**: Identify which numbers appear most frequently
- **Percentage Calculations**: See what percentage of draws each number appears in
- **Historical Trends**: Track how number frequencies change over time

### Hot/Cold Analysis
- **Hot Numbers**: Numbers that have appeared frequently in recent draws
- **Cold Numbers**: Numbers that haven't appeared in recent draws
- **Configurable Time Windows**: Analyze different time periods (default: last 50 games)

### Pattern Detection
- **Odd/Even Patterns**: Analyze the distribution of odd and even numbers
- **Sum Analysis**: Examine the ranges that sums typically fall into
- **Consecutive Numbers**: Detect how often consecutive numbers appear

### Smart Number Generation
- **Weighted Random**: Generate numbers based on historical frequency
- **Hot/Cold Biasing**: Option to favor hot or cold numbers
- **Statistical Soundness**: Uses proper random number generation techniques

## Data Sources

The tool automatically downloads the latest Powerball data from:
- **Primary Source**: [Lottery Numbers](https://www.lottonumbers.com/past-powerball-results)

Data is cached locally in `~/powerball.csv` for faster subsequent analysis.

## Development

### Project Structure

```
powersall/
├── powersall/          # Main package
│   ├── __init__.py
│   ├── powersall.py    # Main CLI and analysis functions
│   └── functions.py    # Core analysis functions
├── tests/              # Test suite
├── docs/               # GitHub Pages site
└── pyproject.toml      # Modern Python project configuration
```

### Testing

```bash
# Run all tests
uv run pytest

# Run with coverage
uv run pytest --cov=powersall

# Run specific test file
uv run pytest tests/test_functions.py
```

### Code Quality

```bash
# Format code
uv run black powersall/

# Sort imports
uv run isort powersall/

# Lint code
uv run flake8 powersall/

# Type checking
uv run mypy powersall/
```

## Publishing to PyPI

The project is configured for automatic PyPI publishing via GitHub Actions. To publish a new version:

1. **Update the version** (choose one method):

   ```bash
   # Automatic version bumping
   make bump-version-patch    # For bug fixes (2.0.0 -> 2.0.1)
   make bump-version-minor    # For new features (2.0.0 -> 2.1.0)
   make bump-version-major    # For breaking changes (2.0.0 -> 3.0.0)

   # Or manual version setting
   uv run bump-version --set 2.1.0
   ```

2. **Commit and tag the changes**:

   ```bash
   git add .
   git commit -m "Bump version to 2.1.0"
   git tag v2.1.0
   git push && git push --tags
   ```

3. **Automatic publishing**: The GitHub Actions workflow will automatically:
   - Build the package
   - Upload to PyPI using the `PYPI_API_TOKEN` secret
   - Create a GitHub Release with the built artifacts

### Manual Publishing

If you need to publish manually or test the build:

```bash
# Build the package
make build

# Check the built package
twine check dist/*

# Upload to PyPI (requires PYPI_API_TOKEN)
twine upload dist/*
```

**Note**: You'll need to set up a `PYPI_API_TOKEN` secret in your GitHub repository settings for automatic publishing.

## Documentation

- **📖 [GitHub Pages Site](https://jamesacampbell.github.io/powersall)**: Interactive documentation and demos
- **🔧 API Reference**: Comprehensive API documentation available in the GitHub Pages site
- **💡 Examples**: Usage examples and tutorials

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Support

- **🐛 Issues**: [GitHub Issues](https://github.com/jamesacampbell/powersall/issues)
- **💬 Discussions**: [GitHub Discussions](https://github.com/jamesacampbell/powersall/discussions)
- **📧 Email**: jc@normail.co

## Changelog

### Version 2.0.0
- **Major Update**: Complete rewrite for Python 3.14+
- **New Features**: Added frequency analysis, hot/cold detection, pattern analysis
- **Modern Package Management**: Migrated to `uv` and `pyproject.toml`
- **Interactive Web Interface**: Added Streamlit-based web application
- **GitHub Pages**: Comprehensive documentation site
- **Enhanced CLI**: More command-line options and better UX

### Version 1.0.8
- Original release with basic Powerball data fetching and number generation

---

*Built with ❤️ using modern Python and web technologies*

