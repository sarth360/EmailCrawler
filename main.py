import requests
from bs4 import BeautifulSoup
import re
import csv
import time
from urllib.parse import urljoin, urlparse
import urllib3
from tqdm import tqdm

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


MAX_PAGES = 15
REQUEST_DELAY = 1.5  # seconds
CSV_FILE = "Emails.csv"
HEADERS = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64)'}


visited_urls = set()
found_emails = set()
email_buffer = []
url_queue = []

progress_bar = None




def normalize_url(url):
    if not url.startswith(('http://', 'https://')):
        url = 'https://' + url
    return url


def extract_emails(text):
    return set(re.findall(r'\b[\w\.-]+@[\w\.-]+\.\w{2,4}\b', text))


def write_email_to_buffer(email, source_url):
    email_buffer.append((email, source_url))
    if len(email_buffer) >= 10:
        flush_email_buffer()


def flush_email_buffer():
    global email_buffer
    if not email_buffer:
        return
    try:
        with open(CSV_FILE, 'a', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerows(email_buffer)
        email_buffer.clear()
    except Exception as e:
        print(f"❌ Failed to write buffered emails: {e}")


def initialize_csv():
    try:
        with open(CSV_FILE, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(['Email', 'Source URL'])
        print(f"📁 Initialized CSV: {CSV_FILE}")
    except Exception as e:
        print(f"❌ Cannot initialize CSV: {e}")




def crawl(domain):
    global progress_bar
    progress_bar = tqdm(total=MAX_PAGES, desc="🌐 Crawling Pages", ncols=80)

    while url_queue and len(visited_urls) < MAX_PAGES:
        url = url_queue.pop(0)
        if url in visited_urls:
            continue

        visited_urls.add(url)
        progress_bar.update(1)
        print(f"\n🔍 Visiting: {url}")

        try:
            response = requests.get(url, headers=HEADERS, timeout=10, verify=False)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, 'html.parser')

            page_emails = extract_emails(soup.get_text())
            new_emails = [email for email in page_emails if email not in found_emails]

            for email in new_emails:
                found_emails.add(email)
                write_email_to_buffer(email, url)

            if new_emails:
                print(f"📧 Found {len(new_emails)} new emails.")

            for tag in soup.find_all('a', href=True):
                link = urljoin(url, tag['href'])
                parsed = urlparse(link)
                if parsed.netloc == domain and link not in visited_urls and link not in url_queue:
                    url_queue.append(link)

            time.sleep(REQUEST_DELAY)

        except Exception as e:
            print(f"⚠️ Failed to crawl {url}: {e}")
            flush_email_buffer()

    progress_bar.close()




if __name__ == "__main__":
    start_url = input("""Welcome to the Email ID Extractor! 
This simple yet powerful tool helps you quickly gather email addresses from any webpage.
Just paste a starting URL, and the extractor will scan it and 15 other pages it can find to return email IDs it detects.
Enter URL(e.g. https://www.opmcm.gov.np/en/): 
""").strip()
    start_url = normalize_url(start_url)
    parsed = urlparse(start_url)
    domain = parsed.netloc

    initialize_csv()
    url_queue.append(start_url)

    try:
        crawl(domain)
    except Exception as final_error:
        print(f"🚨 Final error: {final_error}")

    flush_email_buffer()

    print(f"\n✅ Done. Pages visited: {len(visited_urls)} | Emails found: {len(found_emails)}")
    print(found_emails)
