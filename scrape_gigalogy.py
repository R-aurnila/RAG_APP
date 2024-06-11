import time
from playwright.sync_api import sync_playwright
from urllib.parse import urljoin, urlparse

def scrape_gigalogy():
    base_url = 'https://www.gigalogy.com'
    visited_urls = set()
    urls_to_visit = [base_url]
    data = []

    def get_full_url(link, base):
        return urljoin(base, link)

    def is_valid_url(url, base):
        parsed_base = urlparse(base)
        parsed_url = urlparse(url)
        return parsed_url.netloc == parsed_base.netloc

    def scrape_page(page, url):
        print(f"Scraping: {url}")
        page.goto(url)
        time.sleep(5)
        
        # Find the specific data elements (update the selectors based on the actual structure of the website)
        sections = page.query_selector_all('section')
        for section in sections:
            title_element = section.query_selector('h1, h2, h3')
            description_element = section.query_selector('p')
            
            if title_element and description_element:
                title = title_element.inner_text().strip()
                description = description_element.inner_text().strip()
                data.append(f"URL: {url}\nTitle: {title}\nDescription: {description}\n")
        
        # Extract all links
        links = page.query_selector_all('a')
        for link in links:
            href = link.get_attribute('href')
            if href:
                full_url = get_full_url(href, url)
                if is_valid_url(full_url, base_url) and full_url not in visited_urls:
                    urls_to_visit.append(full_url)

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()

        while urls_to_visit:
            current_url = urls_to_visit.pop(0)
            if current_url not in visited_urls:
                visited_urls.add(current_url)
                scrape_page(page, current_url)

        # Save the data to a TXT file
        with open('app/data/gigalogy_data.txt', 'w', encoding='utf-8') as file:
            file.write("\n".join(data))

        print("Data has been scraped and saved to app/data/gigalogy_data.txt")
        browser.close()

if __name__ == "__main__":
    scrape_gigalogy()
