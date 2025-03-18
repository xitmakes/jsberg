#!/usr/bin/env python3
import sys
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import concurrent.futures
import re

def fetch_urls(host, output_file):
    try:
        # Normalize host URL (ensure it has a scheme)
        if not host.startswith(('http://', 'https://')):
            host = 'http://' + host
        
        # Fetch the page content, following redirects
        session = requests.Session()
        response = session.get(host, timeout=15, allow_redirects=True)
        response.raise_for_status()
        
        # Check for redirects
        if response.history:
            print(f"{host} redirected to {response.url}")
        
        # Parse HTML
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Extract all possible links
        links = set()
        final_url = response.url  # Base URL after redirects

        # 1. <a> tags (hyperlinks)
        for a_tag in soup.find_all('a', href=True):
            url = a_tag['href']
            full_url = urljoin(final_url, url)
            links.add(full_url)

        # 2. <script> tags (JavaScript files)
        for script_tag in soup.find_all('script', src=True):
            url = script_tag['src']
            full_url = urljoin(final_url, url)
            links.add(full_url)

        # 3. <link> tags (CSS files, etc.)
        for link_tag in soup.find_all('link', href=True):
            url = link_tag['href']
            full_url = urljoin(final_url, url)
            links.add(full_url)

        # 4. <img> tags (images)
        for img_tag in soup.find_all('img', src=True):
            url = img_tag['src']
            full_url = urljoin(final_url, url)
            links.add(full_url)

        # 5. Extract URLs from inline JavaScript/CSS (basic regex)
        text_content = response.text
        url_pattern = re.compile(r'(?:https?://|//)[^\s\'"<>]+|(?:src|href)=[\'"]([^\'"]+)[\'"]')
        inline_urls = url_pattern.findall(text_content)
        for match in inline_urls:
            # Handle both full URLs and relative paths
            url = match if isinstance(match, str) else match[0]
            full_url = urljoin(final_url, url)
            links.add(full_url)

        # Save links to file in real-time
        with open(output_file, 'a') as f:
            for link in sorted(links):
                f.write(f"{link}\n")
        
        return links
    except Exception as e:
        print(f"Error fetching {host}: {e}")
        return set()

def main():
    # Check if hosts file is provided
    if len(sys.argv) != 2:
        print("Usage: python3 fetch.py hosts.txt")
        sys.exit(1)
    
    hosts_file = sys.argv[1]
    output_file = 'links.txt'
    
    # Clear the output file at the start
    try:
        open(output_file, 'w').close()  # Creates or clears the file
    except Exception as e:
        print(f"Error initializing {output_file}: {e}")
        sys.exit(1)
    
    # Read hosts from file
    try:
        with open(hosts_file, 'r') as f:
            hosts = [line.strip() for line in f if line.strip()]
    except FileNotFoundError:
        print(f"Error: {hosts_file} not found")
        sys.exit(1)
    
    total_unique_links = set()
    
    # Use ThreadPoolExecutor for concurrent fetching
    with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
        future_to_host = {executor.submit(fetch_urls, host, output_file): host for host in hosts}
        for future in concurrent.futures.as_completed(future_to_host):
            host = future_to_host[future]
            try:
                links = future.result()
                total_unique_links.update(links)
                print(f"Scraped and saved {len(links)} links from {host}")
            except Exception as e:
                print(f"Error processing {host}: {e}")
    
    print(f"Total unique links processed: {len(total_unique_links)}")

if __name__ == "__main__":
    main()
