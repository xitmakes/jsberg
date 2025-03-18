
```markdown
# JSBerg

JSBerg is a fast and efficient URL scraper that extracts links, JavaScript files, CSS files, images, and inline URLs from a list of websites.

## Features
- Follows redirects and extracts final destination URLs.
- Scrapes URLs from `<a>`, `<script>`, `<link>`, and `<img>` tags.
- Extracts inline URLs from JavaScript and CSS.
- Uses multithreading for faster processing.
- Saves results in `links.txt`.

## Installation
```bash
pip install -r requirements.txt
```

## Usage
```bash
python3 berg.py hosts.txt
```
- `hosts.txt`: A file containing a list of hostnames (one per line).
- Extracted links will be saved in `links.txt`.

## Dependencies
- `requests`
- `beautifulsoup4`

## License
MIT License
```

Let me know if you need any modifications! 🚀
