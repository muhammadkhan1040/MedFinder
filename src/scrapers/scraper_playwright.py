import asyncio
from playwright.async_api import async_playwright
import json
import time

BASE_URL = "https://dawaai.pk"
LISTING_URL = "https://dawaai.pk/all-medicines/a"
LIMIT = 20

def clean_text(text):
    """Clean text by removing excessive whitespace and newlines"""
    if not text:
        return ""
    # Replace multiple newlines with a single space
    text = ' '.join(text.split())
    # Remove excessive spaces
    import re
    text = re.sub(r'\s+', ' ', text)
    return text.strip()

async def scrape_medicine_details(page, url):
    """Scrape details from a single medicine page"""
    try:
        await page.goto(url, wait_until='networkidle', timeout=30000)
        await page.wait_for_timeout(2000)  # Wait for dynamic content
        
        data = {}
        
        # Name
        name = await page.locator('h1').first.text_content()
        data['name'] = name.strip() if name else ""
        
        # Brand
        brand = await page.locator('a[href*="/brands/"]').first.text_content()
        data['brand'] = brand.strip() if brand else ""
        
        # Categories
        categories = []
        cat_elements = await page.locator('a[href*="/medicine-category/"], a[href*="/disease/"]').all()
        for cat in cat_elements:
            cat_text = await cat.text_content()
            if cat_text and cat_text.strip() not in categories:
                categories.append(cat_text.strip())
        data['categories'] = categories
        
        # Composition
        generic = await page.locator('a[href*="/generic/"]').first.text_content()
        data['composition'] = generic.strip() if generic else ""
        
        # Price - look for text containing "Rs." and "/"
        price = "N/A"
        try:
            # Get all text from the page
            page_text = await page.content()
            import re
            # Find price pattern
            matches = re.findall(r'Rs\.\s*[\d,]+\.?\d*/\w+', page_text)
            if matches:
                price = matches[0]
        except:
            pass
        data['price'] = price
        
        # Pack Info
        pack_info = "N/A"
        try:
            page_text = await page.content()
            import re
            match = re.search(r'Pack Size:\s*[^\n<]+', page_text)
            if match:
                pack_info = match.group(0).strip()
                # Clean HTML tags if any
                pack_info = re.sub(r'<[^>]+>', '', pack_info)
        except:
            pass
        data['pack_info'] = pack_info
        
        # Image
        img_url = ""
        try:
            img = await page.locator('.product-slider img, .product-image img, img[src*="product.dawaai.pk"]').first.get_attribute('src')
            img_url = img if img else ""
        except:
            pass
        data['image_url'] = img_url
        
        # Content sections using tab IDs
        tab_sections = {
            'introduction': 'tab-1',
            'primary_uses': 'tab-2',
            'indications': 'tab-3',
            'side_effects': 'tab-4',
            'warnings': 'tab-5',
            'contraindications': 'tab-6',
            'faqs': 'tab-7'
        }
        
        for key, tab_id in tab_sections.items():
            content = ""
            try:
                tab_div = page.locator(f'#{tab_id}')
                if await tab_div.count() > 0:
                    content = await tab_div.text_content()
                    content = clean_text(content) if content else ""
            except:
                pass
            data[key] = content
        
        # Expert Advice
        expert_advice = ""
        try:
            intro_tab = page.locator('#tab-1')
            if await intro_tab.count() > 0:
                intro_text = await intro_tab.text_content()
                if intro_text and 'Expert Advice' in intro_text:
                    import re
                    match = re.search(r'Expert Advice\s*(.+?)(?=\n\n|\Z)', intro_text, re.DOTALL)
                    if match:
                        expert_advice = clean_text(match.group(1))
        except:
            pass
        data['expert_advice'] = expert_advice
        
        # Disclaimer
        disclaimer = ""
        try:
            faqs_tab = page.locator('#tab-7')
            if await faqs_tab.count() > 0:
                faqs_text = await faqs_tab.text_content()
                if faqs_text and 'Disclaimer' in faqs_text:
                    import re
                    match = re.search(r'Disclaimer\s*(.+?)(?=\n\n|\Z)', faqs_text, re.DOTALL)
                    if match:
                        disclaimer = clean_text(match.group(1))
        except:
            pass
        data['disclaimer'] = disclaimer
        
        return data
        
    except Exception as e:
        print(f"Error scraping {url}: {e}")
        return None

async def main():
    import string
    import os
    
    # Load existing medicines to avoid duplicates/resume
    existing_medicines = []
    seen_urls = set()
    if os.path.exists('medicines.json'):
        try:
            with open('medicines.json', 'r', encoding='utf-8') as f:
                existing_medicines = json.load(f)
                for med in existing_medicines:
                    # We don't have the URL in the json, but we can check by name or just append new ones.
                    # Ideally we should store the URL in the json to deduplicate.
                    # For now, let's just append and maybe deduplicate by name later if needed.
                    # Actually, let's keep a separate progress file or just append to the list.
                    pass
        except:
            pass
    
    print(f"Loaded {len(existing_medicines)} existing medicines.")
    
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        
        # Iterate through a-z
        for char in string.ascii_lowercase:
            listing_url = f"{BASE_URL}/all-medicines/{char}"
            print(f"\nFetching listing from {listing_url}...")
            
            try:
                await page.goto(listing_url, wait_until='networkidle', timeout=60000)
                await page.wait_for_timeout(2000)
                
                # Find medicine links
                links = []
                link_elements = await page.locator('a[href*="/medicine/"]').all()
                
                for link_elem in link_elements:
                    href = await link_elem.get_attribute('href')
                    if href:
                        links.append(href)
                
                # Remove duplicates from the list
                links = list(dict.fromkeys(links))
                print(f"Found {len(links)} medicines starting with '{char}'.")
                
                # Process links
                for i, link in enumerate(links):
                    # Check if we already have this medicine (by name maybe? or just scrape everything and filter later)
                    # Since we don't store URL in json, let's just scrape. 
                    # To implement resume, we could check if name exists, but names might be duplicate.
                    # Let's just scrape and append.
                    
                    print(f"[{char.upper()} {i+1}/{len(links)}] Scraping {link}...")
                    
                    # Retry logic
                    max_retries = 3
                    details = None
                    for attempt in range(max_retries):
                        details = await scrape_medicine_details(page, link)
                        if details:
                            break
                        print(f"  Retry {attempt+1}/{max_retries}...")
                        await page.wait_for_timeout(2000)
                    
                    if details:
                        existing_medicines.append(details)
                        
                        # Save progress every 10 medicines
                        if len(existing_medicines) % 10 == 0:
                            with open('medicines.json', 'w', encoding='utf-8') as f:
                                json.dump(existing_medicines, f, indent=2, ensure_ascii=False)
                            print(f"  Saved progress ({len(existing_medicines)} total)")
                    
                    await page.wait_for_timeout(500)  # Small delay
                
                # Save after each letter
                with open('medicines.json', 'w', encoding='utf-8') as f:
                    json.dump(existing_medicines, f, indent=2, ensure_ascii=False)
                print(f"Completed letter '{char}'. Saved {len(existing_medicines)} total.")
                
            except Exception as e:
                print(f"Error processing letter '{char}': {e}")
                continue

        await browser.close()
        
    # Final save
    with open('medicines.json', 'w', encoding='utf-8') as f:
        json.dump(existing_medicines, f, indent=2, ensure_ascii=False)
    
    print(f"Done. Saved {len(existing_medicines)} medicines to medicines.json")

if __name__ == "__main__":
    asyncio.run(main())
