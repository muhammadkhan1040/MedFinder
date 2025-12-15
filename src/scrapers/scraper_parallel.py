import asyncio
from playwright.async_api import async_playwright
import json
import time
import string
import os
from datetime import datetime

BASE_URL = "https://dawaai.pk"
MAX_WORKERS = 10  # Number of concurrent browser contexts
SAVE_INTERVAL = 50  # Save progress every N medicines

def clean_text(text):
    """Clean text by removing excessive whitespace and newlines"""
    if not text:
        return ""
    text = ' '.join(text.split())
    import re
    text = re.sub(r'\s+', ' ', text)
    return text.strip()

async def scrape_medicine_details(page, url):
    """Scrape details from a single medicine page"""
    try:
        await page.goto(url, wait_until='networkidle', timeout=30000)
        await page.wait_for_timeout(1000)
        
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
        
        # Price
        price = "N/A"
        try:
            page_text = await page.content()
            import re
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
        
        # Content sections
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

class ProgressTracker:
    """Thread-safe progress tracking with atomic saves"""
    def __init__(self, medicines_file='medicines.json', progress_file='progress.json'):
        self.medicines_file = medicines_file
        self.progress_file = progress_file
        self.lock = asyncio.Lock()
        self.medicines = []
        self.scraped_urls = set()
        self.save_counter = 0
        self.last_save_time = time.time()
        
    def load_existing_data(self):
        """Load existing medicines and track scraped URLs"""
        if os.path.exists(self.medicines_file):
            try:
                with open(self.medicines_file, 'r', encoding='utf-8') as f:
                    self.medicines = json.load(f)
                print(f"Loaded {len(self.medicines)} existing medicines")
            except Exception as e:
                print(f"Error loading medicines: {e}")
                self.medicines = []
        
        # Load progress file if exists
        if os.path.exists(self.progress_file):
            try:
                with open(self.progress_file, 'r', encoding='utf-8') as f:
                    progress = json.load(f)
                    self.scraped_urls = set(progress.get('scraped_urls', []))
                print(f"Loaded {len(self.scraped_urls)} scraped URLs from progress")
            except Exception as e:
                print(f"Error loading progress: {e}")
    
    async def add_medicine(self, url, medicine_data):
        """Add a medicine and save if needed"""
        async with self.lock:
            self.medicines.append(medicine_data)
            self.scraped_urls.add(url)
            self.save_counter += 1
            
            # Save every SAVE_INTERVAL medicines or every 2 minutes
            current_time = time.time()
            should_save = (
                self.save_counter >= SAVE_INTERVAL or 
                (current_time - self.last_save_time) >= 120
            )
            
            if should_save:
                await self._save()
                self.save_counter = 0
                self.last_save_time = current_time
    
    async def _save(self):
        """Atomic save to prevent corruption"""
        temp_medicines = self.medicines_file + '.tmp'
        temp_progress = self.progress_file + '.tmp'
        
        try:
            # Save medicines
            with open(temp_medicines, 'w', encoding='utf-8') as f:
                json.dump(self.medicines, f, indent=2, ensure_ascii=False)
            os.replace(temp_medicines, self.medicines_file)
            
            # Save progress
            progress_data = {
                'scraped_urls': list(self.scraped_urls),
                'total_scraped': len(self.medicines),
                'last_updated': datetime.now().isoformat()
            }
            with open(temp_progress, 'w', encoding='utf-8') as f:
                json.dump(progress_data, f, indent=2)
            os.replace(temp_progress, self.progress_file)
            
            print(f"  💾 Saved progress ({len(self.medicines)} total)")
        except Exception as e:
            print(f"Error saving: {e}")
    
    async def final_save(self):
        """Final save at the end"""
        async with self.lock:
            await self._save()

async def worker(worker_id, browser, url_queue, tracker, semaphore):
    """Worker that processes URLs from the queue"""
    context = await browser.new_context()
    page = await context.new_page()
    
    processed = 0
    
    try:
        while True:
            try:
                url = await asyncio.wait_for(url_queue.get(), timeout=1.0)
            except asyncio.TimeoutError:
                break
            
            async with semaphore:
                # Retry logic
                max_retries = 3
                details = None
                
                for attempt in range(max_retries):
                    try:
                        details = await scrape_medicine_details(page, url)
                        if details:
                            break
                    except Exception as e:
                        if attempt < max_retries - 1:
                            await asyncio.sleep(1 * (attempt + 1))
                        else:
                            print(f"[Worker {worker_id}] Failed after {max_retries} retries: {url}")
                
                if details:
                    await tracker.add_medicine(url, details)
                    processed += 1
                    if processed % 10 == 0:
                        print(f"[Worker {worker_id}] Processed {processed} medicines")
                
                await asyncio.sleep(0.5)  # Small delay
            
            url_queue.task_done()
    
    finally:
        await context.close()
        print(f"[Worker {worker_id}] Finished. Processed {processed} medicines")

async def collect_all_urls(page):
    """Collect all medicine URLs from A-Z"""
    all_urls = []
    
    for char in string.ascii_lowercase:
        listing_url = f"{BASE_URL}/all-medicines/{char}"
        print(f"Collecting URLs from {listing_url}...")
        
        try:
            await page.goto(listing_url, wait_until='networkidle', timeout=60000)
            await page.wait_for_timeout(2000)
            
            link_elements = await page.locator('a[href*="/medicine/"]').all()
            
            for link_elem in link_elements:
                href = await link_elem.get_attribute('href')
                if href and href not in all_urls:
                    all_urls.append(href)
            
            print(f"  Found {len(link_elements)} URLs for '{char}'")
        except Exception as e:
            print(f"Error collecting URLs for '{char}': {e}")
    
    # Remove duplicates
    all_urls = list(dict.fromkeys(all_urls))
    print(f"\nTotal unique URLs collected: {len(all_urls)}")
    return all_urls

async def main():
    tracker = ProgressTracker()
    tracker.load_existing_data()
    
    print(f"\n{'='*60}")
    print(f"Starting Parallel Scraper with {MAX_WORKERS} workers")
    print(f"Existing medicines: {len(tracker.medicines)}")
    print(f"Already scraped URLs: {len(tracker.scraped_urls)}")
    print(f"{'='*60}\n")
    
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        
        # Collect all URLs
        print("Phase 1: Collecting all medicine URLs...")
        page = await browser.new_page()
        all_urls = await collect_all_urls(page)
        await page.close()
        
        # Filter out already scraped URLs
        urls_to_scrape = [url for url in all_urls if url not in tracker.scraped_urls]
        print(f"\nURLs to scrape: {len(urls_to_scrape)}")
        print(f"Already scraped: {len(all_urls) - len(urls_to_scrape)}")
        
        if not urls_to_scrape:
            print("\n✅ All URLs already scraped!")
            await browser.close()
            return
        
        # Create queue and add URLs
        print(f"\nPhase 2: Scraping with {MAX_WORKERS} parallel workers...")
        url_queue = asyncio.Queue()
        for url in urls_to_scrape:
            await url_queue.put(url)
        
        # Semaphore to limit concurrent requests
        semaphore = asyncio.Semaphore(MAX_WORKERS)
        
        # Start workers
        start_time = time.time()
        workers = [
            asyncio.create_task(worker(i, browser, url_queue, tracker, semaphore))
            for i in range(MAX_WORKERS)
        ]
        
        # Wait for all workers to finish
        await asyncio.gather(*workers)
        
        # Final save
        await tracker.final_save()
        
        elapsed = time.time() - start_time
        print(f"\n{'='*60}")
        print(f"✅ Scraping Complete!")
        print(f"Total medicines: {len(tracker.medicines)}")
        print(f"Time elapsed: {elapsed/60:.1f} minutes")
        print(f"Average speed: {len(urls_to_scrape)/(elapsed/60):.1f} medicines/minute")
        print(f"{'='*60}\n")
        
        await browser.close()

if __name__ == "__main__":
    asyncio.run(main())
