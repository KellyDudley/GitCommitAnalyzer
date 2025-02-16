# GitCommitAnalyzer

A comprehensive tool for analyzing Git repository commit history and generating detailed insights about development patterns.

## Features

- **Commit Statistics**: Total commits, contributors, and date ranges
- **Frequency Analysis**: Hourly, daily, and weekday activity patterns  
- **Data Visualization**: Professional charts and graphs
- **Multiple Export Formats**: JSON, HTML reports, and CSV files
- **Flexible Output**: Text summaries, interactive reports, or raw data

## Installation

1. Clone the repository:
```bash
git clone https://github.com/YourUsername/GitCommitAnalyzer.git
cd GitCommitAnalyzer
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Quick Start

```bash
# Basic analysis
./git_analyzer.py

# Include frequency analysis
./git_analyzer.py -f

# Generate visualizations
./git_analyzer.py -f -v

# Create HTML report
./git_analyzer.py -f -v -o html

# Export to CSV
./git_analyzer.py -f --export-csv
```

## Usage

```
Usage: git_analyzer.py [OPTIONS]

  Analyze Git commit history and generate statistics.

Options:
  -r, --repo PATH            Path to git repository (default: current directory)
  -o, --output [json|text|html]  Output format  [default: text]
  -f, --frequency            Include commit frequency analysis
  -v, --visualize            Generate visualization charts
  --report TEXT              HTML report filename (when output=html)  [default: report.html]
  --export-csv               Export data to CSV files
  --help                     Show this message and exit.
```

## Output Formats

### Text Output
Simple, readable summary displayed in the terminal.

### JSON Output
Structured data perfect for integration with other tools:
```bash
./git_analyzer.py -f -o json > analysis.json
```

### HTML Reports
Beautiful, interactive reports with embedded charts:
```bash
./git_analyzer.py -f -v -o html --report my_project_analysis.html
```

### CSV Export
Detailed data exported to CSV files for spreadsheet analysis:
- `commits.csv` - Individual commit details
- `authors.csv` - Author contribution statistics
- `frequency.csv` - Time-based activity patterns
- `timeline.csv` - Daily commit timeline

## Examples

### Basic Repository Analysis
```bash
./git_analyzer.py
```
Output:
```
=== Git Commit Analysis ===
Repository: /path/to/your/repo
Total commits: 142

Date range:
  First commit: 2024-01-15T10:30:00
  Last commit: 2024-02-15T16:45:23

Authors:
  John Doe: 89 commits
  Jane Smith: 53 commits
```

### Frequency Analysis with Charts
```bash
./git_analyzer.py -f -v
```
Generates frequency statistics and saves visualization charts to the `plots/` directory.

### Comprehensive Analysis
```bash
./git_analyzer.py -f -v --export-csv -o html --report full_analysis.html
```
Creates an HTML report with charts AND exports all data to CSV files.

## File Structure

```
GitCommitAnalyzer/
├── git_analyzer.py      # Main application
├── visualizer.py        # Chart generation
├── report_generator.py  # HTML report creation
├── csv_exporter.py      # CSV export functionality
├── config.py           # Configuration management
├── examples.py         # Usage examples
├── requirements.txt    # Python dependencies
└── README.md          # This file
```

## Requirements

- Python 3.7+
- GitPython 3.1.40+
- Click 8.1.7+
- Matplotlib 3.8.2+ (for visualizations)
- Pandas 2.1.4+ (for data processing)
- Jinja2 3.1.2+ (for HTML reports)

## Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/your-feature`
3. Commit your changes: `git commit -am 'Add some feature'`
4. Push to the branch: `git push origin feature/your-feature`
5. Submit a pull request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Development

### Running Examples
```bash
./examples.py
```

### Running Tests
```bash
python -m pytest tests/
```

## Tips

- Use `-f` flag for detailed insights into development patterns
- Combine `-v` with `-f` to get visual representations of your data
- HTML reports are great for sharing with teams or stakeholders
- CSV exports allow for custom analysis in Excel or other tools

## Troubleshooting

**Missing dependencies**: Run `pip install -r requirements.txt`

**Permission denied**: Make sure the script is executable: `chmod +x git_analyzer.py`

**Not a git repository**: Make sure you're in a directory with a `.git` folder, or specify the path with `-r`

**Charts not generating**: Install matplotlib: `pip install matplotlib`