import requests
from bs4 import BeautifulSoup
import json
import time

BASE_URL = "https://dawaai.pk"
LISTING_URL = "https://dawaai.pk/all-medicines/a"
LIMIT = 20

def get_soup(url):
    try:
        response = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Remove script and style elements to avoid extracting JS code
        for script in soup(["script", "style"]):
            script.decompose()
            
        return soup
    except Exception as e:
        print(f"Error fetching {url}: {e}")
        return None

def scrape_medicine_details(url):
    soup = get_soup(url)
    if not soup:
        return None

    data = {}
    
    # Name
    name_tag = soup.select_one('h1')
    data['name'] = name_tag.get_text(strip=True) if name_tag else ""
    
    # Brand
    brand_tag = soup.select_one('a[href*="/brands/"]')
    data['brand'] = brand_tag.get_text(strip=True) if brand_tag else ""
    
    # Categories (Therapeutic Class etc)
    categories = []
    for cat in soup.select('a[href*="/medicine-category/"], a[href*="/disease/"]'):
        cat_text = cat.get_text(strip=True)
        if cat_text and cat_text not in categories:
            categories.append(cat_text)
    data['categories'] = categories
    
    # Composition (Generic)
    generic_tag = soup.select_one('a[href*="/generic/"]')
    data['composition'] = generic_tag.get_text(strip=True) if generic_tag else ""
    
    # Price - look for price in the inventory detail section
    price = "N/A"
    
    # Strategy 1: Look for "Rs. X.XX/unit" pattern (most common)
    price_elements = soup.find_all(string=lambda text: text and 'Rs.' in text and '/' in text)
    for elem in price_elements:
        elem_text = elem.strip()
        # Check if it contains a unit type after the slash
        if any(unit in elem_text.lower() for unit in ['/tablet', '/capsule', '/ml', '/g', '/ointment', 
                                                        '/injection', '/sachet', '/strip', '/pack', 
                                                        '/bottle', '/tube', '/vial', '/ampoule']):
            price = elem_text
            break
    
    # Strategy 2: If not found, look in inventory-detail div
    if price == "N/A":
        inventory_div = soup.select_one('.inventory-detail')
        if inventory_div:
            # Get all text and look for price pattern
            text = inventory_div.get_text()
            import re
            # Match "Rs. 123.45/unit"
            match = re.search(r'Rs\.\s*[\d,]+\.?\d*/\w+', text)
            if match:
                price = match.group(0)
    
    # Strategy 3: Look near the pack size text
    if price == "N/A":
        all_text = soup.get_text()
        import re
        # Find all Rs. X/unit patterns
        matches = re.findall(r'Rs\.\s*[\d,]+\.?\d*/\w+', all_text)
        if matches:
            price = matches[0]  # Take the first one found
    
    data['price'] = price
    
    # Pack Size - look for "Pack Size:" text
    pack_info = "N/A"
    
    # Strategy 1: Look for "Pack Size:" text
    pack_elements = soup.find_all(string=lambda text: text and 'Pack Size:' in text if text else False)
    if pack_elements:
        for elem in pack_elements:
            parent_text = elem.parent.get_text(strip=True) if elem.parent else elem.strip()
            if 'Pack Size:' in parent_text:
                pack_info = parent_text
                break
    
    # Strategy 2: Use regex to find pack size pattern
    if pack_info == "N/A":
        all_text = soup.get_text()
        import re
        match = re.search(r'Pack Size:\s*[^\n]+', all_text)
        if match:
            pack_info = match.group(0).strip()
    
    data['pack_info'] = pack_info

    # Image - look for product image
    img_tag = soup.select_one('.product-slider img, .product-image img, img[src*="product.dawaai.pk"]')
    if not img_tag:
        # Try to find any image near the top of the page
        img_tag = soup.select_one('img[src*="product"]')
    
    data['image_url'] = img_tag['src'] if img_tag and img_tag.get('src') else ""

    # Content Sections - use tab IDs
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
        data[key] = ""
        tab_div = soup.select_one(f'#{tab_id}')
        if tab_div:
            # Get all text content, excluding nested tabs
            content_parts = []
            for elem in tab_div.find_all(['p', 'ul', 'li', 'h3', 'h4']):
                text = elem.get_text(strip=True)
                if text and text not in content_parts:
                    content_parts.append(text)
            data[key] = "\n".join(content_parts)
    
    # Expert Advice - usually in tab-1 under h3
    expert_advice = ""
    intro_tab = soup.select_one('#tab-1')
    if intro_tab:
        expert_h3 = intro_tab.find('h3', string=lambda text: 'Expert Advice' in text if text else False)
        if expert_h3:
            advice_parts = []
            for sibling in expert_h3.find_next_siblings(['p', 'ul', 'li']):
                if sibling.name == 'h3':  # Stop at next header
                    break
                text = sibling.get_text(strip=True)
                if text:
                    advice_parts.append(text)
            expert_advice = "\n".join(advice_parts)
    
    data['expert_advice'] = expert_advice
    
    # Disclaimer - usually at the end of FAQs
    disclaimer = ""
    faqs_tab = soup.select_one('#tab-7')
    if faqs_tab:
        disclaimer_elem = faqs_tab.find(string=lambda text: 'Disclaimer' in text if text else False)
        if disclaimer_elem:
            # Get the parent and following content
            parent = disclaimer_elem.find_parent(['p', 'div', 'h3', 'h4'])
            if parent:
                disclaimer = parent.get_text(strip=True)
    
    data['disclaimer'] = disclaimer
    
    return data

def main():
    print(f"Fetching listing from {LISTING_URL}...")
    soup = get_soup(LISTING_URL)
    if not soup:
        print("Failed to fetch listing page.")
        return

    # Find medicine links
    links = []
    seen_urls = set()
    
    for a in soup.select('a[href*="/medicine/"]'):
        href = a['href']
        if href not in seen_urls:
            links.append(href)
            seen_urls.add(href)
            
    print(f"Found {len(links)} medicines. Processing first {LIMIT}...")
    
    medicines = []
    count = 0
    
    try:
        for link in links:
            if count >= LIMIT:
                break
                
            print(f"Scraping {link}...")
            details = scrape_medicine_details(link)
            if details:
                medicines.append(details)
                count += 1
            
            time.sleep(1) # Be polite
    except KeyboardInterrupt:
        print("\nScraping interrupted. Saving progress...")
    except Exception as e:
        print(f"\nAn error occurred: {e}. Saving progress...")
    finally:
        with open('medicines.json', 'w', encoding='utf-8') as f:
            json.dump(medicines, f, indent=2, ensure_ascii=False)
        
        print(f"Done. Saved {len(medicines)} medicines to medicines.json")

if __name__ == "__main__":
    main()
