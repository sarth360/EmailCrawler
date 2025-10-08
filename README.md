# Email-Crawler
A Python tool that crawls websites to extract email addresses from web pages. It starts from a given URL and scans up to 15 pages within the same domain, saving discovered emails along with their source URLs into a CSV file.

## Features

- 🌐 **Web Crawling**: Automatically discovers and visits up to 15 pages within the same domain
- 📧 **Email Extraction**: Uses regex patterns to find email addresses in web content
- 📊 **CSV Output**: Saves results with email addresses and their source URLs
- 🚀 **Progress Tracking**: Visual progress bar showing crawling status
- ⚡ **Efficient Processing**: Buffered writing and duplicate prevention
- 🛡️ **Error Handling**: Robust error handling for network issues

## Requirements

- Python 3.12
- Required packages (see Installation)

## Installation

1. Clone this repository:
   ```bash
   git clone "https://github.com/sarth360/EmailCrawler"
   cd email-crawler
   ```

2. Install required dependencies:
   ```bash
   pip install requests beautifulsoup4 tqdm
   ```

## Usage

1. Run the main script:
   ```bash
   python main.py
   ```

2. Enter a starting URL when prompted:
   ```
   Enter URL(e.g. https://www.example.com/): https://www.yoursite.com
   ```

3. The program will:
   - Crawl up to 15 pages on the specified domain
   - Extract email addresses from each page
   - Save results to `Emails.csv`
   - Display progress and final statistics

## Output

The tool generates an `Emails.csv` file with two columns:
- **Email**: The extracted email address
- **Source URL**: The webpage where the email was found

## Configuration

You can modify these settings in `main.py`:
- `MAX_PAGES`: Maximum number of pages to crawl (default: 15)
- `REQUEST_DELAY`: Delay between requests in seconds (default: 1.5)
- `CSV_FILE`: Output filename (default: "Emails.csv")

## Technical Details

**Technologies Used:**
- `requests` - HTTP library for web requests
- `BeautifulSoup4` - HTML parsing and extraction
- `re` - Regular expressions for email pattern matching
- `csv` - CSV file handling
- `tqdm` - Progress bar display

## Use Cases

📧 Perfect for:
- Contact discovery and outreach
- Research and data collection
- Lead generation
- Website contact information gathering

## Disclaimer

Please ensure you comply with website terms of service and applicable laws when using this tool. Respect robots.txt files and rate limiting.
