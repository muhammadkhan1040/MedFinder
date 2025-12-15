"""
API Investigation Script for dawaai.pk

This script will:
1. Load a medicine page with network monitoring
2. Capture all network requests
3. Identify potential API endpoints
4. Check if there's a faster way to get availability data
"""

import asyncio
from playwright.async_api import async_playwright
import json

async def investigate_dawaai_api():
    """Investigate dawaai.pk for hidden APIs"""
    
    print("="*70)
    print("🔍 Investigating dawaai.pk for Hidden APIs")
    print("="*70)
    
    # Test URL - a known medicine
    test_url = "https://dawaai.pk/medicine/panadol-5-24329.html"
    
    network_requests = []
    api_endpoints = []
    
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context()
        page = await context.new_page()
        
        # Capture all network requests
        def handle_request(request):
            network_requests.append({
                'url': request.url,
                'method': request.method,
                'resource_type': request.resource_type
            })
        
        def handle_response(response):
            # Look for JSON responses (potential APIs)
            if 'json' in response.headers.get('content-type', '').lower():
                api_endpoints.append({
                    'url': response.url,
                    'status': response.status,
                    'content_type': response.headers.get('content-type', '')
                })
        
        page.on('request', handle_request)
        page.on('response', handle_response)
        
        print(f"\n📄 Loading: {test_url}")
        print("   Monitoring network traffic...\n")
        
        try:
            await page.goto(test_url, wait_until='networkidle', timeout=30000)
            await page.wait_for_timeout(3000)  # Wait a bit more for any lazy-loaded content
            
            print(f"✅ Page loaded successfully!")
            print(f"   Total network requests: {len(network_requests)}")
            print(f"   Potential API endpoints: {len(api_endpoints)}")
            
            # Analyze the page structure for availability indicators
            print(f"\n🔍 Analyzing page structure for availability indicators...")
            
            # Check for common availability selectors
            availability_selectors = [
                '.stock-status',
                '.availability',
                '.in-stock',
                '.out-of-stock',
                'button[disabled]',
                '.product-availability',
                '[class*="stock"]',
                '[class*="available"]'
            ]
            
            found_indicators = []
            for selector in availability_selectors:
                try:
                    elements = await page.locator(selector).all()
                    if elements:
                        for elem in elements:
                            text = await elem.text_content()
                            if text and text.strip():
                                found_indicators.append({
                                    'selector': selector,
                                    'text': text.strip()
                                })
                except:
                    pass
            
            # Get page content to analyze
            page_content = await page.content()
            
            # Look for JSON data embedded in the page
            if 'application/ld+json' in page_content or 'application/json' in page_content:
                print("   ✅ Found JSON data in page!")
            
            # Check for "Add to Cart" button
            try:
                add_to_cart = await page.locator('button:has-text("Add to Cart"), button:has-text("Buy Now")').first.is_enabled()
                print(f"   Add to Cart button enabled: {add_to_cart}")
            except:
                print("   No 'Add to Cart' button found")
            
            print(f"\n{'='*70}")
            print("📊 INVESTIGATION RESULTS")
            print(f"{'='*70}")
            
            # Show API endpoints found
            if api_endpoints:
                print(f"\n🎯 Potential API Endpoints Found ({len(api_endpoints)}):")
                for i, endpoint in enumerate(api_endpoints[:10], 1):  # Show first 10
                    print(f"   {i}. {endpoint['url']}")
                    print(f"      Status: {endpoint['status']}, Type: {endpoint['content_type']}")
            else:
                print("\n❌ No JSON API endpoints detected")
                print("   The site likely renders availability in HTML directly")
            
            # Show availability indicators
            if found_indicators:
                print(f"\n✅ Availability Indicators Found ({len(found_indicators)}):")
                for indicator in found_indicators[:5]:  # Show first 5
                    print(f"   Selector: {indicator['selector']}")
                    print(f"   Text: {indicator['text']}")
            else:
                print("\n⚠️  No standard availability indicators found")
                print("   Will need to analyze page structure manually")
            
            # Show interesting requests
            print(f"\n📡 Network Request Types:")
            request_types = {}
            for req in network_requests:
                rtype = req['resource_type']
                request_types[rtype] = request_types.get(rtype, 0) + 1
            
            for rtype, count in sorted(request_types.items(), key=lambda x: x[1], reverse=True):
                print(f"   {rtype}: {count}")
            
            # Save detailed results
            results = {
                'test_url': test_url,
                'total_requests': len(network_requests),
                'api_endpoints': api_endpoints,
                'availability_indicators': found_indicators,
                'request_types': request_types,
                'all_requests': network_requests[:50]  # Save first 50 requests
            }
            
            with open('api_investigation_results.json', 'w', encoding='utf-8') as f:
                json.dump(results, f, indent=2, ensure_ascii=False)
            
            print(f"\n💾 Detailed results saved to: api_investigation_results.json")
            
            # Recommendation
            print(f"\n{'='*70}")
            print("💡 RECOMMENDATION")
            print(f"{'='*70}")
            
            if api_endpoints:
                print("✅ Hidden APIs detected! This is the BEST approach:")
                print("   - Use direct API calls instead of full page scraping")
                print("   - 10-50x faster than loading full pages")
                print("   - More reliable and less resource-intensive")
            else:
                print("📄 No APIs detected. Recommended approach:")
                print("   - Use HTML scraping with Playwright")
                print("   - Implement smart caching (2-hour freshness)")
                print("   - Disable images/CSS for 3x speed improvement")
                print("   - Use parallel processing for batch checks")
            
            print(f"{'='*70}\n")
            
        except Exception as e:
            print(f"❌ Error during investigation: {e}")
        
        finally:
            await browser.close()

if __name__ == "__main__":
    asyncio.run(investigate_dawaai_api())
