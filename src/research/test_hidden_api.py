"""
Deep Investigation: Testing the hidden API endpoint
"""

import asyncio
from playwright.async_api import async_playwright
import json

async def test_hidden_api():
    """Test the hidden API endpoint we discovered"""
    
    print("="*70)
    print("🎯 Testing Hidden API: /product/get_product")
    print("="*70)
    
    test_url = "https://dawaai.pk/medicine/panadol-5-24329.html"
    api_responses = []
    
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context()
        page = await context.new_page()
        
        # Capture API responses
        async def handle_response(response):
            if 'get_product' in response.url:
                try:
                    body = await response.json()
                    api_responses.append({
                        'url': response.url,
                        'status': response.status,
                        'body': body
                    })
                    print(f"\n✅ Captured API Response!")
                    print(f"   URL: {response.url}")
                    print(f"   Status: {response.status}")
                except Exception as e:
                    print(f"   Could not parse JSON: {e}")
        
        page.on('response', handle_response)
        
        print(f"\n📄 Loading page and monitoring API calls...")
        await page.goto(test_url, wait_until='networkidle', timeout=30000)
        await page.wait_for_timeout(2000)
        
        if api_responses:
            print(f"\n{'='*70}")
            print("📊 API RESPONSE ANALYSIS")
            print(f"{'='*70}")
            
            for i, resp in enumerate(api_responses, 1):
                print(f"\nResponse #{i}:")
                print(f"URL: {resp['url']}")
                print(f"Status: {resp['status']}")
                print(f"\nResponse Body (first 500 chars):")
                body_str = json.dumps(resp['body'], indent=2)
                print(body_str[:500] + "..." if len(body_str) > 500 else body_str)
                
                # Check for availability indicators
                body = resp['body']
                print(f"\n🔍 Looking for availability indicators...")
                
                # Common keys that might indicate availability
                availability_keys = ['available', 'stock', 'in_stock', 'out_of_stock', 
                                    'availability', 'quantity', 'is_available']
                
                def search_dict(d, keys, path=""):
                    """Recursively search for keys in nested dict"""
                    results = []
                    if isinstance(d, dict):
                        for k, v in d.items():
                            current_path = f"{path}.{k}" if path else k
                            if any(key.lower() in k.lower() for key in keys):
                                results.append((current_path, v))
                            if isinstance(v, (dict, list)):
                                results.extend(search_dict(v, keys, current_path))
                    elif isinstance(d, list):
                        for i, item in enumerate(d):
                            results.extend(search_dict(item, keys, f"{path}[{i}]"))
                    return results
                
                found_keys = search_dict(body, availability_keys)
                
                if found_keys:
                    print(f"   ✅ Found {len(found_keys)} potential availability indicators:")
                    for key_path, value in found_keys[:10]:  # Show first 10
                        print(f"      {key_path}: {value}")
                else:
                    print(f"   ⚠️  No obvious availability indicators found")
                    print(f"   Showing all top-level keys:")
                    if isinstance(body, dict):
                        for key in list(body.keys())[:20]:
                            print(f"      - {key}")
            
            # Save full response
            with open('api_response_analysis.json', 'w', encoding='utf-8') as f:
                json.dump(api_responses, f, indent=2, ensure_ascii=False)
            
            print(f"\n💾 Full API response saved to: api_response_analysis.json")
            
        else:
            print(f"\n❌ No API responses captured")
            print(f"   The API might not be called on every page load")
        
        await browser.close()
        
        print(f"\n{'='*70}")
        print("💡 CONCLUSION")
        print(f"{'='*70}")
        
        if api_responses:
            print("✅ Hidden API successfully captured!")
            print("   Next steps:")
            print("   1. Analyze the API response structure")
            print("   2. Identify the availability field")
            print("   3. Create a fast API-based checker")
        else:
            print("⚠️  API not captured in this test")
            print("   Will use HTML scraping approach instead")
        
        print(f"{'='*70}\n")

if __name__ == "__main__":
    asyncio.run(test_hidden_api())
