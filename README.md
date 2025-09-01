# Semantic Scholar DOI Extractor

A Python tool that extracts DOIs (Digital Object Identifiers) from Semantic Scholar citations using the Semantic Scholar API.

## Overview

This program processes a file containing citations with Semantic Scholar URLs and retrieves the corresponding DOIs for each paper. It outputs the DOIs as a comma-separated list both to the console and to a file.

## Features

- Extracts paper IDs from Semantic Scholar URLs (format: `https://api.semanticscholar.org/CorpusID:XXXXX`)
- Retrieves DOIs using the Semantic Scholar API
- Handles rate limiting with configurable delays
- Supports both authenticated (with API key) and unauthenticated requests
- Outputs results as comma-separated DOIs
- Saves output to `dois_output.txt`

## Requirements

- Python 3.12 or higher
- Dependencies (automatically installed):
  - `requests>=2.31.0`
  - `python-dotenv>=1.0.0`

## Installation

1. Clone this repository:
   ```bash
   git clone <repository-url>
   cd semschol1
   ```

2. Install dependencies:
   ```bash
   pip install -e .
   ```
   
   Or install directly:
   ```bash
   pip install requests python-dotenv
   ```

## Usage

Run the program with a citations file as an argument:

```bash
python main.py <citations_file>
```

Example:
```bash
python main.py cits.txt
```

### Input File Format

The citations file should contain BibTeX-style entries with Semantic Scholar URLs. Example:

```bibtex
@article{Author2024Title,
  title={Paper Title},
  author={Author Name},
  journal={Journal Name},
  year={2024},
  url={https://api.semanticscholar.org/CorpusID:123456789}
}
```

### Output

The program will:
1. Display progress and results in the console
2. Create `dois_output.txt` containing comma-separated DOIs

Example output:
```
10.1038/nature12345, 10.1126/science.abc123, 10.1073/pnas.0123456789
```

## API Key Configuration

While the program can run without an API key, having one significantly improves performance and reduces rate limiting issues.

### Getting an API Key

1. Visit [Semantic Scholar API](https://www.semanticscholar.org/product/api)
2. Sign up for a free API key
3. Create a `.env` file in the project directory:
   ```
   API_KEY=your_semantic_scholar_api_key_here
   ```

### Rate Limits

- **With API key**: 100 requests per 5 minutes (1.5 second delay between requests)
- **Without API key**: More restrictive limits (3 second delay between requests)

## Error Handling

The program handles various error cases:
- **404 errors**: Paper not found in Semantic Scholar database
- **429 errors**: Rate limit exceeded
- **Missing DOIs**: Some papers may not have DOIs assigned
- **Network errors**: Connection issues with the API

## Example Run

```bash
$ python main.py 299.bib

Found 26 Semantic Scholar URLs to process
Processing URL 1/26: https://api.semanticscholar.org/CorpusID:15782374
  -> DOI: 10.1554/05-412.1
Processing URL 2/26: https://api.semanticscholar.org/CorpusID:280317455
  -> DOI: 10.1038/s41467-024-12345-6
...

Found 26 DOIs:
10.1554/05-412.1, 10.1038/s41467-024-12345-6, ...

DOIs also saved to dois_output.txt
```

## Project Structure

```
semschol1/
├── main.py           # Main program script
├── pyproject.toml    # Project configuration
├── .env             # API key configuration (create this)
├── README.md        # This file
└── dois_output.txt  # Output file (generated)
```

## Troubleshooting

1. **Rate limit errors**: Add an API key or increase delays
2. **404 errors**: The paper ID may not exist in Semantic Scholar
3. **No DOI found**: Not all papers have DOIs assigned
4. **Module not found**: Install dependencies with `pip install -r requirements.txt`

## License

[Add your license information here]

## Contributing

[Add contribution guidelines if applicable]
