from django.core.management.base import BaseCommand
from gadgets.models import Product
import requests
from bs4 import BeautifulSoup
import re
import time

class Command(BaseCommand):
    help = 'Scrapes Amazon URLs to update live prices using multiple fallback selectors'

    def handle(self, *args, **kwargs):
        self.stdout.write(self.style.NOTICE('Starting robust Amazon price tracker...'))
        
        products_to_check = Product.objects.exclude(gadget_link__isnull=True).exclude(gadget_link__exact='')

        # Added more headers to look as human as possible
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Accept-Language": "en-US, en;q=0.9",
            "Accept-Encoding": "gzip, deflate, br",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
            "Connection": "keep-alive",
        }

        for product in products_to_check:
            self.stdout.write(f'Checking {product.name}...')
            
            try:
                response = requests.get(product.gadget_link, headers=headers, timeout=15)
                
                # Check if Amazon blocked us with a CAPTCHA
                if "api/services/captcha" in response.text or "Enter the characters you see below" in response.text:
                    self.stdout.write(self.style.ERROR(f'  -> BLOCKED: Amazon served a CAPTCHA for {product.name}.'))
                    time.sleep(2) # Pause before trying the next one so we don't get IP banned
                    continue

                if response.status_code == 200:
                    soup = BeautifulSoup(response.content, "html.parser")
                    price_element = None
                    
                    # --- THE SHOTGUN APPROACH ---
                    # A list of dictionaries containing common Amazon price HTML tags
                    amazon_selectors = [
                        {"tag": "span", "class_name": "a-price-whole"},
                        {"tag": "span", "class_name": "a-color-price"},
                        {"tag": "span", "id_name": "priceblock_ourprice"},
                        {"tag": "span", "id_name": "priceblock_dealprice"},
                        {"tag": "div", "class_name": "a-section a-spacing-none aok-align-center"} # Sometimes hidden in a div
                    ]
                    
                    # Loop through our selectors and try to find the price
                    for selector in amazon_selectors:
                        if "class_name" in selector:
                            price_element = soup.find(selector["tag"], class_=selector["class_name"])
                        elif "id_name" in selector:
                            price_element = soup.find(selector["tag"], id=selector["id_name"])
                            
                        if price_element and price_element.text.strip():
                            break # We found it! Stop checking other selectors.
                    
                    # Process the price if we found the element
                    if price_element:
                        raw_price = price_element.text.strip()
                        # Clean the string: remove commas, ₹ symbols, and letters
                        clean_price_string = re.sub(r'[^\d.]', '', raw_price)
                        
                        if clean_price_string:
                            try:
                                new_price = float(clean_price_string)
                                product.price = new_price
                                product.save()
                                self.stdout.write(self.style.SUCCESS(f'  -> Updated {product.name} to ₹{new_price}'))
                            except ValueError:
                                self.stdout.write(self.style.WARNING(f'  -> Found text, but could not convert to number: "{raw_price}"'))
                        else:
                            self.stdout.write(self.style.WARNING(f'  -> Could not extract numbers from: "{raw_price}"'))
                    else:
                        self.stdout.write(self.style.WARNING(f'  -> Price element completely missing from HTML for {product.name}.'))
                else:
                    self.stdout.write(self.style.ERROR(f'  -> Failed to load page. Status Code: {response.status_code}'))
                    
            except Exception as e:
                self.stdout.write(self.style.ERROR(f'  -> Error tracking {product.name}: {str(e)}'))
            
            # Pause for 2 seconds between each product so Amazon doesn't block your IP address
            time.sleep(2) 

        self.stdout.write(self.style.SUCCESS('Finished price tracking cycle!'))