import os
import csv
import asyncio
from playwright.async_api import async_playwright
from urllib.parse import urljoin, urlparse

async def scrape_website(URL: str):
    base_url = URL
    visited_urls = set()
    urls_to_visit = [base_url]
    data = []

    def get_full_url(link, base):
        return urljoin(base, link)

    def is_valid_url(url, base):
        parsed_base = urlparse(base)
        parsed_url = urlparse(url)
        return parsed_url.netloc == parsed_base.netloc

    async def scrape_page(page, url):
        print(f"Scraping: {url} ... This could take a while, please be patient.")
        await page.goto(url)
        await asyncio.sleep(5)
        
        sections = await page.query_selector_all('section')
        for section in sections:
            title_element = await section.query_selector('h1, h2, h3')
            description_element = await section.query_selector('p')
            
            if title_element and description_element:
                title = (await title_element.inner_text()).strip()
                description = (await description_element.inner_text()).strip()
                data.append({
                    "URL": url,
                    "Title": title,
                    "Description": description
                })
        
        links = await page.query_selector_all('a')
        for link in links:
            href = await link.get_attribute('href')
            if href:
                full_url = get_full_url(href, url)
                if is_valid_url(full_url, base_url) and full_url not in visited_urls:
                    urls_to_visit.append(full_url)

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()

        while urls_to_visit:
            current_url = urls_to_visit.pop(0)
            if current_url not in visited_urls:
                visited_urls.add(current_url)
                await scrape_page(page, current_url)

        os.makedirs('data', exist_ok=True)
        with open('back_end/data/website_data.txt', 'w', encoding='utf-8') as file:
            for item in data:
                file.write(f"URL: {item['URL']}\nTitle: {item['Title']}\nDescription: {item['Description']}\n\n")
        
        with open('back_end/data/website_data.csv', 'w', newline='', encoding='utf-8') as csvfile:
            fieldnames = ['URL', 'Title', 'Description']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            for item in data:
                writer.writerow(item)

        print("Data has been scraped and saved to back_end/data/website_data.csv")
        await browser.close()

# Run the async function
# URL = 'http://example.com'  # Replace with the actual URL you want to scrape
# asyncio.run(scrape_website(URL))

path="back_end/data/website_data.txt"

